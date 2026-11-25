---
name: astra-booster
description: Verify that a multi-step coding change delivers its real outcome when the result leaves the process (stored data, jobs, messages, external APIs, payments, rendered UI) or is handed to another agent; skip questions, copy or style edits and single local functions already covered by a unit test.
---

# AstraBooster: deliver the outcome

An acceptance protocol for an existing coding agent; it grants no tools, authority or model settings. Host and project rules win: where they already cover honesty, reporting, security or approvals, use this skill only for the evidence ladder and acceptance method, and put the evidence level into the project's report format.

## A. Define observable completion

Before editing, state concisely:
- **Action:** what a user or another system must be able to do.
- **Evidence:** where the outcome becomes visible or readable.
- **Boundary:** environment, data, budget and actions that need permission.

Record them in the task note if work may span sessions or agents. Inspect relevant code, configuration and current changes first. Prefer the current architecture; never present a mock or demo as the requested feature.

## B. Match checks to risk

| Risk | Change | Verification |
| --- | --- | --- |
| Low | Docs, wording, isolated styling | Inspect output; one cheap targeted check. |
| Medium | UI behavior, routine API, refactor | Targeted behavior test, a plausible failure state, changed-scope regression. |
| High | Identity, storage, transactions, concurrency, integration | Authorized end-to-end action, downstream evidence, negative/security checks, review if warranted. |
| Restricted | Production, outbound messages, payments, deletes, infrastructure | Read-only discovery; mutate only with explicit authorization. |

Open a reference only when its trigger applies:
- [acceptance](references/acceptance.md): data, jobs, messages, APIs, auth, bots, timers, no staging.
- [interface](references/interface.md): rendered pages, apps, responsive layout.
- [security](references/security.md): restricted actions where host policy is silent.
- [efficiency](references/efficiency.md): expensive checks, large contexts, tight budgets.
- [review](references/review.md): high risk worth a second reviewer.
- [handoff](references/handoff.md): interrupted, delegated or parallel work.
- [evaluation](references/evaluation.md): comparing workflow versions.

## C. Implement, falsify, correct

Make the smallest change that satisfies the outcome. Choose a check that could **disprove** success: a bug's check fails before the fix and passes after; a feature's check would fail without the change.

If the outcome leaves the process, follow the permitted path to its receiver: tag test input with a unique marker in an authorized test environment and find that marker there, read through a different path than the writer (the store or inbox, not the API that reported success).

Evidence ladder (report the highest level actually observed):
1. **Changed:** the artifact exists.
2. **Build-checked:** build, lint or type check ran.
3. **Behavior-checked:** a targeted assertion passed.
4. **Flow-checked:** a permitted user/API journey ran through the components.
5. **Effect-confirmed:** the marked result was read back independently at its destination.

Name the environment with the level (local, staging, production). A green build, mocked response, success toast or absence of errors is not delivery.

On failure, find a concrete cause, fix within scope and rerun the affected check. Defaults unless the host sets others: the same failing command at most twice without a new hypothesis; stop and report after three fix cycles without progress; expensive checks (browser, end-to-end, load) once per fix. Stop at real access or authorization boundaries.

## D. Review and hand off

Review the final diff and in-scope regressions. For high risk, use an existing authorized reviewer if the cost is justified; label self-review as such.

Report each outcome as `Evidence: <level> (<environment>): <where observed>; not confirmed: <what and why>`, then blockers or remaining risk. Never invent results, metrics, access or external effects; never expose secrets or customer data.
