#!/usr/bin/env python3
"""Dependency-free static checks for the public AstraBooster package."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "astra-booster"
SKILL = SKILL_DIR / "SKILL.md"
MAX_SKILL_BYTES = 4400        # SKILL.md loads into every invoking session; growth needs a reason
MAX_DESCRIPTION_CHARS = 400
MODEL_NAMES = re.compile(r"\b(GPT-\d|Claude \d|Gemini \d|o\d-)", re.I)
ERRORS = []

if not SKILL.is_file():
    ERRORS.append("Missing SKILL.md")
else:
    data = SKILL.read_text(encoding="utf-8")
    front = re.match(r"\A---\n(.*?)\n---\n", data, re.S)
    if not front:
        ERRORS.append("Missing YAML frontmatter")
    else:
        if not re.search(r"^name:\s*astra-booster\s*$", front.group(1), re.M):
            ERRORS.append("Frontmatter name must be astra-booster")
        desc = re.search(r"^description:\s*(.+)$", front.group(1), re.M)
        if not desc:
            ERRORS.append("Missing description")
        else:
            text = desc.group(1).strip().strip('"')
            if len(text) > MAX_DESCRIPTION_CHARS:
                ERRORS.append(f"Description longer than {MAX_DESCRIPTION_CHARS} characters")
            if re.search(r"[.!?]\s+\S", text):
                ERRORS.append("Description must be one sentence")
    if len(data.encode("utf-8")) > MAX_SKILL_BYTES:
        ERRORS.append(f"SKILL.md exceeds {MAX_SKILL_BYTES} bytes")
    linked = set(re.findall(r"^- \[[^\]]+\]\((references/[^)#]+)\): \S", data, re.M))
    for link in re.findall(r"\]\((references/[^)#]+)\)", data):
        if not (SKILL_DIR / link).is_file():
            ERRORS.append(f"Broken skill reference: {link}")
    for ref in sorted((SKILL_DIR / "references").glob("*.md")):
        if f"references/{ref.name}" not in linked:
            ERRORS.append(f"Reference without an index line and trigger in SKILL.md: {ref.name}")

for p in SKILL_DIR.rglob("*"):
    if p.is_file() and MODEL_NAMES.search(p.read_text(encoding="utf-8")):
        ERRORS.append(f"Model-specific name inside the skill (keep it in README): {p.relative_to(ROOT)}")

for required in (
    "README.md", "README.ru.md", "LICENSE", "NOTICE.md",
    "docs/STRATEGY.md", "docs/STRATEGY.ru.md",
    "astra-booster/agents/openai.yaml", "tests/scenarios.md", "tests/triggers.md",
):
    if not (ROOT / required).is_file():
        ERRORS.append(f"Missing {required}")

for p in ROOT.rglob("*.md"):
    if ".git" in p.parts:
        continue
    for link in re.findall(r"(?<!!)\]\(([^)]+)\)", p.read_text(encoding="utf-8")):
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = link.split("#", 1)[0]
        if path and not (p.parent / path).exists():
            ERRORS.append(f"Broken link: {p.relative_to(ROOT)} -> {link}")

TOOL = ROOT / "tools" / "token_profile.py"
FIXTURE = ROOT / "tests" / "fixtures" / "claude-code"
if not TOOL.is_file():
    ERRORS.append("Missing tools/token_profile.py")
else:
    import json
    import subprocess
    run = subprocess.run([sys.executable, "-I", str(TOOL), "--json", str(FIXTURE)], capture_output=True, text=True)
    try:
        report = json.loads(run.stdout)
    except ValueError:
        report = None
    expected = {"session_start": 2, "compaction": 1, "expired": 2, "model_switch": 1, "unexplained": 1}
    if run.returncode or not report:
        ERRORS.append(f"token_profile.py failed on the fixture: {run.stderr.strip()[-300:]}")
    elif (report["requests"], report["cost_usd"]["total"], report["unpriced_requests"], report["tool_turns"],
            report["single_call_tool_turn_share"]) != (9, 1.046, {"claude-unknown-9": 1}, 1, 0.0) \
            or {k: v["count"] for k, v in report["rebuilds"].items()} != expected:
        ERRORS.append("token_profile.py fixture totals or rebuild labels changed")

if ERRORS:
    print("FAILED:\n" + "\n".join("- " + e for e in ERRORS))
    sys.exit(1)
print("OK: AstraBooster manifest, size budget, reference index, triggers, docs, links and token profiler")
