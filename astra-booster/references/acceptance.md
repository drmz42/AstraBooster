# Verifiable integration acceptance

Load for features that store data, trigger jobs, send messages, call APIs, authenticate, run on a schedule or depend on a downstream system.

## Contract

State the initiating actor/action, approved test environment, evidence destination, correlation identifier, expected failure case and cleanup boundary.

1. Check allowed fixtures, test credentials and destinations; never substitute production recipients without permission.
2. Execute the real permitted path: UI or CLI → API → service → job/store/recipient.
3. Generate a unique marker. Verify that **the same marker** appears in an independently queried destination or persisted record, read through a different path than the one that wrote it.
4. Check a representative failure: bad input, authorization rejected, unavailable dependency, timeout, duplicate or concurrency conflict as risk warrants.
5. Recheck affected existing behavior. Remove only own test records, with explicit authorization and reliable identification.

## Evidence interpretation

| Evidence | Supports |
| --- | --- |
| File diff | Changed |
| Command output from lint/build | Build-checked |
| Assertions that actually executed | Behavior-checked |
| Authorized full component journey | Flow-checked |
| Correlated destination/read-back | Effect-confirmed |

Mimicked UIs, spies, test doubles and local mocks are useful for isolated tests but do not prove that a real recipient received anything. Do not publish personal data, raw logs or secrets as evidence.

## Without a staging environment

Use what the project already has: a local fixture or container, a dry-run mode, a sandbox or test account offered by the provider, or a read-only probe of the real dependency. Label the level with its environment, for example `flow-checked (local fixture)`. Never point a test at production recipients or data to make up for a missing staging environment; report the boundary instead.

## Bots, workers and scheduled jobs

- **Chat bots:** send the marker from a test account to a test chat; confirm the reply and any stored effect. Deliver the same update twice and check the action happens once.
- **Queues and workers:** enqueue a marked job; confirm completion through the store or result channel, and one failure path (retry, dead letter or timeout).
- **Timers and cron:** trigger one run manually with the same environment and user as the schedule; confirm the marked effect and that a second run is safe.
- Find the marker in the logs or store with a bounded query; do not paste raw logs into the report.

**Example:** Submit `ABTEST-####` through a staging contact form. Query the staging mailbox or CRM for that same marker. If destination access is missing, report the last confirmed step, not assumed delivery.
