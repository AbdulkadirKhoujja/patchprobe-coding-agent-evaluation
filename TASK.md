# Agent-facing engineering task: Repair event ingestion

Existing code: `candidate/event_inbox.py`. Implement `ingest(events)` as a pure, deterministic normalizer for a multi-tenant event stream. It must not use external services or third-party packages.

## Acceptance criteria

1. Accept a list of event dictionaries with exactly the required fields `tenant_id`, `event_id`, `occurred_at`, `payload` (additional fields permitted). `tenant_id` and `event_id` must be nonblank strings, `occurred_at` a nonnegative integer but not a boolean, and `payload` a dictionary. On malformed input, raise `ValueError` rather than quietly dropping an event.
2. Deduplicate using the **pair** (`tenant_id`, `event_id`). The same event ID from two different tenants describes distinct events and both must survive.
3. For repeated events in one tenant, keep the entry with the greatest `occurred_at`; ties prefer the last input occurrence.
4. Order returned events by each key's **first appearance** in the input, not the time of its latest payload.
5. Return fresh dictionaries containing exactly `tenant_id`, `event_id`, `occurred_at`, `payload`. Clone the top-level payload dict so changes to output do not change the input. Do not modify input records or lists.
6. Return `[]` for an empty input list. Non-list input raises `ValueError`.
7. Document any data limitations; no files, network, database or wall-clock dependencies.

**Evaluator method:** the agent sees this task plus the public test file. The evaluator independently runs held-out black-box tests against the proposed code and the reference solution, and records failures and a reproducible rationale.
