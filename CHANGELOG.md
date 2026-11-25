# Changelog

## 2.2.0 — 2026-11-25

- `tools/token_profile.py`: token and prompt-cache profile of Claude Code sessions from local logs (cost by category at API list prices, cache hit share, context size, single-call tool turns, full cache rebuilds by cause, most expensive sessions; `--session` for evaluation runs, `--json`, `--prices`). Reads only usage counters and timestamps; standard library only.
- Efficiency reference: batch independent calls, keep check output small without losing the exit code, start a fresh session at a task boundary.
- Evaluation reference: fill the Cost fields with `tools/token_profile.py`.
- Validator runs the profiler on a synthetic fixture and checks its totals and rebuild labels.

## 2.1.0 — 2026-11-25

- One-sentence description with concrete triggers (data, jobs, messages, external APIs, payments, rendered UI, handoffs) and explicit exclusions, for reliable automatic activation.
- Host and project rules take precedence; the skill adds the evidence ladder and acceptance method and reports inside the project's format.
- Reference index with a one-line trigger per file, so an agent opens only what applies.
- Red-to-green rule: a bug's check fails before the fix and passes after; a feature's check would fail without the change.
- Independent read-back defined as a different path than the writer; evidence level reported with its environment and a one-line evidence template.
- Default repair limits: the same failing command at most twice without a new hypothesis, stop after three fix cycles without progress, expensive checks once per fix.
- Acceptance guidance without staging and for bots, workers and scheduled jobs; acceptance criteria recorded in the task note for multi-session work.
- Model-specific reasoning-effort advice removed from the skill files (kept in the README).
- Evaluation: run record fields, cost to accepted result, blind review, control tasks and A/B order alternation.
- Validator: `SKILL.md` size budget, one-sentence description, reference index check, no model names inside the skill; new trigger cases and scenarios F and G.

## 2.0.1 — 2026-11-25

- Documented recommended GPT-6.2 Astra reasoning settings (`xhigh` for complex quality-first tasks; `max` where supported and justified) in both READMEs and the efficiency reference.

## 2.0.0 — 2026-11-25

- Independent AstraBooster skill and Agent Skills-compatible manifest.
- Five-level observable outcome verification.
- Risk-sensitive acceptance, UI, integration and security guidance.
- Modular references for bounded retries, independent review, multi-agent handoff and evaluation.
- Bilingual documentation, product strategy, examples and repository validation.
