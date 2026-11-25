# Efficient verification without cutting corners

Load for costly tasks, multi-step investigations, large contexts or limited compute/API budgets.

- Start with the cheapest check capable of disproving the important success claim.
- Avoid a full test suite when a narrow regression check is sufficient; escalate when the risk warrants it.
- Reuse current source-of-truth material and existing test infrastructure rather than rebuilding tooling.
- Read only relevant files and reference pages. Do not paste entire repositories or knowledge bases into context.
- Set a practical retry/effort budget on expensive operations. Repeating the identical failed command without changing a hypothesis is not progress.
- Do not invoke second agents, browsers, renderers or load tests for routine trivial edits.
- Respect existing model/effort configuration. A skill cannot select inaccessible models or change the host's inference settings.
- For quality-first complex work with GPT-6.2 Astra, prefer `xhigh`; consider `max` for exceptionally demanding or high-risk tasks when supported and justified by cost and evaluation. For simpler work, use a proportionate effort level. The user or orchestrator selects the setting; never silently change it or claim it was applied without evidence.
- Report the result and evidence concisely; do not narrate every intermediate tool call.

Use representative acceptance scenarios to compare quality, effort and costs across workflow versions.
