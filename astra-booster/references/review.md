# Independent review on meaningful risk

Load for auth, money, production, storage migrations, shared state, high-impact multi-file refactors or external integrations.

Invoke a second review **only if** there is an authorized agent or independent context already available and the risk justifies its expense.

Give the reviewer the original user objective, acceptance criteria, scoped diff, environment and factual check results. Exclude credentials, customer information and irrelevant transcript material.

Ask for **reproducible violations**, not aesthetic preferences: broken requirements, hidden mocks, access-control flaws, silent failures, concurrency errors, regression and unsafe recovery.

Report findings as:
- Confirmed: severity, file/component, violated criterion, reproduction, proposed remedy.
- Hypothesis: what remains unobserved and a concrete safe check.
- No finding: exact scope inspected, not a blanket security guarantee.

Resolve significant confirmed findings and rerun affected tests. If only self-review is available, label it self-review.
