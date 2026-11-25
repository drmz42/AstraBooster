# Verifiable integration acceptance

Load for features that store data, trigger jobs, send messages, call APIs, authenticate or depend on a downstream system.

## Contract

State the initiating actor/action, approved test environment, evidence destination, correlation identifier, expected failure case and cleanup boundary.

1. Check allowed fixtures, test credentials and destinations; never substitute production recipients without permission.
2. Execute the real permitted path: UI or CLI → API → service → job/store/recipient.
3. Generate a unique marker. Verify that **the same marker** appears in an independently queried destination or persisted record.
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

**Example:** Submit `ABTEST-####` through a staging contact form. Query the staging mailbox or CRM for that same marker. If destination access is missing, report the last confirmed step, not assumed delivery.
