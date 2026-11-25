#!/usr/bin/env python3
"""Token and prompt-cache profile of Claude Code sessions, read from local session logs.

Reads only usage counters, model names, timestamps and tool-call counts from
~/.claude/projects/**/*.jsonl. It never prints prompts, code or tool output, and
nothing leaves the machine. Standard library only.

Examples:
  python tools/token_profile.py                     # every session under ~/.claude/projects
  python tools/token_profile.py --since 2026-11-01  # requests on or after a UTC date
  python tools/token_profile.py --session 4f975da5  # one run, e.g. variant A or B of an evaluation
  python tools/token_profile.py --json PATH...      # machine-readable; files or directories
"""
import argparse
import collections
import datetime as dt
import json
import statistics
import sys
from pathlib import Path

# USD per million tokens: input, 5-minute cache write, 1-hour cache write, cache read, output.
# Source: platform.claude.com/docs/en/about-claude/pricing, checked 2026-11-25.
# Other models are counted in tokens only unless --prices supplies them.
PRICES = {
    "claude-opus-5-5": (4.0, 5.0, 8.0, 0.20, 20.0),
    "claude-sonnet-5-5": (2.0, 2.5, 4.0, 0.10, 10.0),
    "claude-haiku-5-5": (0.10, 0.125, 0.20, 0.01, 0.50),
}
REBUILD_MIN_CONTEXT = 20_000   # smaller prompts are not worth classifying
REBUILD_SHARE = 0.5            # cache write above this share of the context = full rebuild
BIG_CONTEXT = 200_000
COMPACTION_WINDOW = 5          # seconds a compaction summary may trail the next request
REBUILD_KINDS = ("session_start", "compaction", "expired", "model_switch", "unexplained")


def timestamp(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def iter_logs(paths):
    for raw in paths:
        path = Path(raw).expanduser()
        if path.is_dir():
            yield from sorted(path.rglob("*.jsonl"))
        elif path.is_file():
            yield path


def identity(path):
    """(project, session, is_subagent) for <project>/<session>.jsonl or <project>/<session>/subagents/*.jsonl."""
    if path.parent.name == "subagents":
        return path.parent.parent.parent.name, path.parent.parent.name, True
    return path.parent.name, path.stem, False


def read_log(path):
    """Requests (one per API response) and compaction times of one conversation file."""
    requests, compactions = {}, []
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if '"usage"' not in line and '"isCompactSummary"' not in line:
                continue
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if record.get("isCompactSummary") and record.get("timestamp"):
                compactions.append(timestamp(record["timestamp"]))
                continue
            message = record.get("message")
            if record.get("type") != "assistant" or not isinstance(message, dict):
                continue
            usage, model = message.get("usage"), message.get("model") or "?"
            if not isinstance(usage, dict) or not record.get("timestamp") or model.startswith("<"):
                continue
            key = message.get("id") or record.get("uuid")
            tools = sum(1 for block in message.get("content") or []
                        if isinstance(block, dict) and block.get("type") == "tool_use")
            if key in requests:  # Claude Code writes one line per content block of a response
                requests[key]["tools"] += tools
                requests[key]["usage"] = usage
                continue
            requests[key] = {"t": timestamp(record["timestamp"]), "model": model, "usage": usage, "tools": tools}
    result = []
    for item in sorted(requests.values(), key=lambda r: r["t"]):
        usage = item["usage"]
        split = usage.get("cache_creation") or {}
        w1 = split.get("ephemeral_1h_input_tokens") or 0
        w5 = split.get("ephemeral_5m_input_tokens")
        if w5 is None:
            w5 = max((usage.get("cache_creation_input_tokens") or 0) - w1, 0)
        inp, read, out = (usage.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens", "output_tokens"))
        result.append({"t": item["t"], "model": item["model"], "tools": item["tools"],
                       "inp": inp, "w5": w5, "w1": w1, "read": read, "out": out, "ctx": inp + read + w5 + w1})
    return result, sorted(compactions)


def price_of(model, prices):
    for key in sorted(prices, key=len, reverse=True):
        if model.startswith(key):
            return prices[key]
    return None


def classify(requests, compactions):
    """Label each full cache rebuild with its most likely cause."""
    labels, ttl = {}, 300
    for i, req in enumerate(requests):
        written = req["w5"] + req["w1"]
        if req["ctx"] >= REBUILD_MIN_CONTEXT and written > REBUILD_SHARE * req["ctx"]:
            if i == 0:
                kind = "session_start"
            else:
                prev = requests[i - 1]
                if req["model"] != prev["model"]:
                    kind = "model_switch"
                elif any(prev["t"] < c <= req["t"] + COMPACTION_WINDOW for c in compactions):
                    kind = "compaction"
                elif req["t"] - prev["t"] > ttl:
                    kind = "expired"
                else:
                    kind = "unexplained"
            labels[i] = kind
        if written:
            ttl = 3600 if req["w1"] else 300  # lifetime of the newest cache entry
    return labels


def percentile(values, share):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(share * len(ordered)))] if ordered else 0


def profile(paths, prices, since=None, until=None, session=None, project=None, top=5):
    totals = collections.Counter()
    cost = collections.Counter()
    rebuild_count, rebuild_extra = collections.Counter(), collections.Counter()
    models, sessions, unpriced = collections.Counter(), collections.defaultdict(collections.Counter), collections.Counter()
    contexts, big_cost, sub_cost, priced_cost = [], 0.0, 0.0, 0.0
    tool_turns = single_call = conversations = subagents = 0
    first = last = None
    for path in iter_logs(paths):
        proj, sess, is_sub = identity(path)
        if (session and session not in sess) or (project and project not in proj):
            continue
        requests, compactions = read_log(path)
        labels = classify(requests, compactions)
        kept = 0
        for i, req in enumerate(requests):
            if (since and req["t"] < since) or (until and req["t"] >= until):
                continue
            kept += 1
            first = req["t"] if first is None else min(first, req["t"])
            last = req["t"] if last is None else max(last, req["t"])
            for k in ("inp", "w5", "w1", "read", "out"):
                totals[k] += req[k]
            contexts.append(req["ctx"])
            if req["tools"]:
                tool_turns += 1
                single_call += req["tools"] == 1
            price = price_of(req["model"], prices)
            models[req["model"]] += 1
            sessions[(proj, sess)]["requests"] += 1
            if price is None:
                unpriced[req["model"]] += 1
            else:
                parts = {"input": req["inp"] * price[0], "cache_write": req["w5"] * price[1] + req["w1"] * price[2],
                         "cache_read": req["read"] * price[3], "output": req["out"] * price[4]}
                usd = sum(parts.values()) / 1e6
                for k, v in parts.items():
                    cost[k] += v / 1e6
                priced_cost += usd
                sessions[(proj, sess)]["usd"] += usd
                big_cost += usd if req["ctx"] > BIG_CONTEXT else 0.0
                sub_cost += usd if is_sub else 0.0
            if i in labels:
                kind = labels[i]
                rebuild_count[kind] += 1
                if price is not None:
                    rebuild_extra[kind] += (req["w5"] * (price[1] - price[3]) + req["w1"] * (price[2] - price[3])) / 1e6
        if kept:
            conversations += 1
            subagents += is_sub
    input_side = totals["inp"] + totals["w5"] + totals["w1"] + totals["read"]
    iso = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%d %H:%M") if t else None
    return {
        "period_utc": [iso(first), iso(last)],
        "requests": len(contexts),
        "conversations": conversations,
        "subagent_conversations": subagents,
        "tokens": {"input": totals["inp"], "cache_write_5m": totals["w5"], "cache_write_1h": totals["w1"],
                   "cache_read": totals["read"], "output": totals["out"]},
        "cost_usd": {"total": round(priced_cost, 4), **{k: round(v, 4) for k, v in cost.items()}},
        "unpriced_requests": dict(unpriced),
        "cache_hit_share": round(totals["read"] / input_side, 4) if input_side else None,
        "context_median": int(statistics.median(contexts)) if contexts else 0,
        "context_p90": percentile(contexts, 0.9),
        "big_context_cost_share": round(big_cost / priced_cost, 4) if priced_cost else None,
        "subagent_cost_share": round(sub_cost / priced_cost, 4) if priced_cost else None,
        "tool_turns": tool_turns,
        "single_call_tool_turn_share": round(single_call / tool_turns, 4) if tool_turns else None,
        "rebuilds": {k: {"count": rebuild_count[k], "extra_usd": round(rebuild_extra[k], 4)} for k in REBUILD_KINDS},
        "models": dict(models),
        "top_sessions": [{"project": p, "session": s, "requests": c["requests"], "usd": round(c["usd"], 4)}
                         for (p, s), c in sorted(sessions.items(), key=lambda x: -x[1]["usd"])[:top]],
    }


def share(part, whole):
    return f"{100 * part / whole:.0f}%" if whole else "n/a"


def render(r):
    c, t = r["cost_usd"], r["tokens"]
    lines = [
        f"Claude Code profile {r['period_utc'][0]} .. {r['period_utc'][1]} UTC: {r['requests']} requests, "
        f"{r['conversations']} conversations ({r['subagent_conversations']} subagent)",
        f"Cost at API list prices: ${c['total']:.2f}"
        + (f"; no price for {sum(r['unpriced_requests'].values())} requests ({', '.join(r['unpriced_requests'])}), "
           "pass --prices" if r["unpriced_requests"] else ""),
    ]
    for key, label in (("cache_read", "cache read"), ("cache_write", "cache write"), ("output", "output"), ("input", "uncached input")):
        lines.append(f"  {label:<15}{share(c.get(key, 0), c['total']):>5}")
    hit = r["cache_hit_share"]
    lines += [
        f"Cache hit (input tokens read from cache): {100 * hit:.1f}%" if hit is not None else "Cache hit: n/a",
        f"Context per request: median {r['context_median'] // 1000}k, p90 {r['context_p90'] // 1000}k; "
        f"requests over {BIG_CONTEXT // 1000}k: {share(r['big_context_cost_share'] or 0, 1)} of cost",
        f"Subagents: {share(r['subagent_cost_share'] or 0, 1)} of cost",
    ]
    if r["tool_turns"]:
        lines.append(f"Tool turns with a single call: {share(r['single_call_tool_turn_share'], 1)} "
                     "(each extra turn rereads the whole context; batch independent calls)")
    lines.append("Full cache rebuilds (write > half the context), extra cost vs a cache hit:")
    for kind in REBUILD_KINDS:
        item = r["rebuilds"][kind]
        lines.append(f"  {kind:<15}{item['count']:>5}  ${item['extra_usd']:.2f}")
    if r["top_sessions"]:
        lines.append("Most expensive sessions (subagents included):")
        for s in r["top_sessions"]:
            lines.append(f"  ${s['usd']:>8.2f} {s['requests']:>6} req  {s['project']}/{s['session'][:8]}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="*", default=[str(Path.home() / ".claude" / "projects")],
                        help="session log files or directories (default: ~/.claude/projects)")
    parser.add_argument("--since", help="first UTC date, YYYY-MM-DD")
    parser.add_argument("--until", help="UTC date to stop before, YYYY-MM-DD")
    parser.add_argument("--session", help="only sessions whose id contains this text (subagents included)")
    parser.add_argument("--project", help="only project folders whose name contains this text")
    parser.add_argument("--prices", help='JSON file {"model-id-prefix": [input, write_5m, write_1h, read, output]} in USD per million tokens')
    parser.add_argument("--top", type=int, default=5, help="number of most expensive sessions to list")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = parser.parse_args(argv)
    day = lambda s: dt.datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc).timestamp() if s else None
    prices = dict(PRICES)
    if args.prices:
        prices.update({k: tuple(float(x) for x in v) for k, v in json.loads(Path(args.prices).read_text()).items()})
    result = profile(args.paths, prices, day(args.since), day(args.until), args.session, args.project, args.top)
    if not result["requests"]:
        print("No Claude Code requests found in: " + ", ".join(args.paths), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2) if args.json else render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
