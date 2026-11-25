---
name: astra-booster
description: Outcome-based quality workflow for multi-step coding tasks, UI, API integrations, data persistence and agent handoffs. Use for work requiring real verification; skip simple Q&A or copy edits.
---

# AstraBooster: deliver the outcome

This skill is a practical acceptance protocol for an existing coding agent. It does not expand tool access, user authority or available model settings. Follow existing repository policies and explicit user constraints.

## A. Define observable completion

Before implementing, identify privately and concisely:
- **Action:** what the user or another system must be able to do.
- **Evidence:** where the outcome should be visible or readable.
- **Boundary:** allowed environment, dependencies, data, budget and actions requiring permission.

Inspect the relevant code, configuration, repository instructions and current work before editing. Prefer the current architecture to a speculative rewrite. Do not replace a requested functioning feature with a mock or visual demonstration without saying so.

## B. Match checks to risk

| Risk | Typical change | Appropriate verification |
| --- | --- | --- |
| Low | Documentation, isolated wording or styling | Inspect output and run one cheap targeted check. |
| Medium | UI behavior, routine API or refactor | Targeted behavioral test, plausible failure state, changed-scope regression. |
| High | Identity, storage, transactions, concurrency, integration | Authorized end-to-end action, downstream evidence, targeted negative/security checks and review if warranted. |
| Restricted | Production, external communication, payments, deletes or infrastructure | Read-only discovery first. Mutate only with explicit authorization. |

Read the relevant references **on demand**, never all by default: [acceptance](references/acceptance.md), [interface](references/interface.md), [security](references/security.md), [efficiency](references/efficiency.md), [review](references/review.md), [handoff](references/handoff.md), [evaluation](references/evaluation.md).

## C. Implement, falsify, correct

Make the smallest change that can satisfy the observable outcome. Use existing tools and fixtures. Select a test capable of **disproving** success, not only demonstrating code execution.

If the outcome leaves the process (form, API, queue, database, notification), follow the approved path to its receiving end or verify by independent read-back. Correlate test input with downstream output using a unique marker in an authorized test environment.

Use these reporting levels accurately:

1. **Changed:** the artifact exists.
2. **Build-checked:** the relevant build, lint or type check ran.
3. **Behavior-checked:** an actual targeted assertion passed.
4. **Flow-checked:** a permitted user/API journey exercised the relevant components.
5. **Effect-confirmed:** the expected destination or persisted result was observed independently.

A green build, a mocked API response, a success toast, or the absence of errors is not evidence of delivery.

When a check fails, locate a concrete cause, make a scoped correction and rerun the affected check. Avoid repeating expensive attempts without a new hypothesis. Respect resource and iteration budgets; stop when there is a real access or authorization boundary.

## D. Inspect and hand off

Review the final diff and regressions within its scope. For high-risk work, use an existing authorized second reviewer if its cost is justified; do not equate self-review with independent review.

Provide a short handoff: **outcome, environment, highest observed evidence, actionable blockers or remaining risk**. Never invent execution results, metrics, tool access or external effects. Never expose secrets or customer data.

This skill supplements rather than replaces specialized testing, security, product-design and deployment skills.
