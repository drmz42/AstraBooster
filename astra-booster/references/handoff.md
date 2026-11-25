# Agent-to-agent handoff

Load for interrupted, delegated or parallel work. Reuse the repository's existing task queue, file locks, branch rules and knowledge-base protocol; do not silently create a competing coordinator.

Before editing, inspect task ownership, active worktree, locks and current changes. Do not permit concurrent writers to corrupt the same file.

Write the acceptance condition (action, evidence, boundary) into the task note before the first long step, so the next agent verifies the same outcome.

A concise handoff contains:
1. Goal and observable acceptance condition.
2. Project/repo/branch, modified files and relevant decisions.
3. Checks actually executed, each with its evidence level and environment.
4. Important unfinished verification, authorization blockers or risks.
5. One recommended next step.

Write verified decisions to the project's approved knowledge-base location only when required by its actual instructions. Never record unverified guesses, credentials or full conversation dumps as project truth.
