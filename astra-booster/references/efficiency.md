# Efficient verification without cutting corners

Load for costly tasks, multi-step investigations, large contexts or limited compute/API budgets.

- Start with the cheapest check capable of disproving the important success claim.
- Avoid a full test suite when a narrow regression check is sufficient; escalate when the risk warrants it.
- Reuse current source-of-truth material and existing test infrastructure rather than rebuilding tooling.
- Read only relevant files and reference pages. Do not paste entire repositories or knowledge bases into context.
- Keep the retry defaults from the skill unless the host sets others. Repeating the identical failed command without a new hypothesis is not progress.
- Do not invoke second agents, browsers, renderers or load tests for routine trivial edits.
- Respect the existing model and effort configuration. The user or orchestrator selects it; a skill cannot change it or claim it was applied without evidence.
- Report the result and evidence concisely; do not narrate every intermediate tool call.

Judge a workflow by the cost and time to an accepted, verified result, including rework, not by tokens alone.
