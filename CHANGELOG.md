# Changelog

## 2.1.0 — unreleased

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
