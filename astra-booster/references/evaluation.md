# Reproducible evaluation

Prepare a small set of safe, representative tasks: isolated edit, UI workflow, API-to-store integration, authorization failure and multi-step agent handoff. Add one or two trivial control tasks to measure overhead when the skill is not needed.

Use a clean snapshot for each run with identical model, reasoning effort, permissions, fixtures, task phrasing and resource limits. Compare a normal agent run (A) to one using AstraBooster (B) in separate sessions and worktrees; never pass the output of one run to the other. Compare the same host and model only. Alternate the A/B order between pairs and repeat trials where the budget allows. For a clean baseline, keep the skill manual-only during the evaluation.

Before viewing outputs, fix the acceptance criteria, objective post-run checks, budget and iteration limit. Record per run (`N/A` when the host does not expose a value):

| Group | Fields |
| --- | --- |
| Run | task id, category, variant A/B, host and version, model, reasoning effort, start commit |
| Cost | input, output, reasoning, cache read and write tokens, API cost with caching |
| Time | wall time, time to accepted result, tool calls, repair cycles, repeated actions, human interventions |
| Quality | acceptance criteria passed, highest evidence level reached, defects found and missed, regressions, false success claims, unauthorized actions |

Primary measure: **cost to accepted result** = cost of the run + cost of every repair, rerun and review until the result passes the fixed criteria. Report absolute and relative differences.

Independent review: give a second agent the objective, criteria, diff and check output with variant labels removed, and ask for reproducible violations only (see [review](review.md)).

A mocked recipient must be labelled as mocked. Never use production data or real payments for the evaluation. Interpret small experiments as diagnostic rather than statistically definitive. Record evidence sources, not estimates disguised as measurements.
