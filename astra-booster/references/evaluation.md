# Reproducible evaluation

Prepare a small set of safe, representative tasks: isolated edit, UI workflow, API-to-store integration, authorization failure and multi-step agent handoff.

Use a clean snapshot for each run with identical model, reasoning effort, permissions, fixtures, task phrasing and resource limits. Compare a normal agent run to one using AstraBooster; where available, use repeated trials and a separate reviewer.

Before viewing outputs, define acceptance criteria and objective post-run checks. Record:
- acceptance criteria passed and end-to-end outcomes confirmed;
- independently found defects and regressions;
- false success claims or unauthorized actions;
- number of repair cycles and human interventions;
- actual token/API cost and elapsed time, when the host exposes them.

A mocked recipient must be labelled as mocked. Never use production data or real payments for the evaluation. Interpret small experiments as diagnostic rather than statistically definitive. Record evidence sources, not estimates disguised as measurements.
