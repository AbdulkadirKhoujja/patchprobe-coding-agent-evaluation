# PR-style review — synthetic candidate

**Verdict: REQUEST CHANGES.** Review applies only to the intentionally flawed local example. This is not a real agent's work.

## Evidence and root causes

1. **Cross-tenant data loss (correctness: critical).** `candidate/event_inbox.py` uses the bare `event_id` as its deduplication key. Tenant A and B can each legitimately emit `e1`; the second is silently dropped. Reproduction: `tests/test_holdout.py::test_same_id_different_tenants_must_survive`.
2. **Incorrect revision selection (correctness: major).** The first duplicate always wins, even when an updated record has a greater timestamp or a later equal timestamp. Reproduction: `test_newest_update_wins` and `test_equal_timestamp_uses_later_occurrence`.
3. **Input validation defects (robustness: major).** Missing fields, invalid IDs/timestamps and a non-dictionary input must raise `ValueError`. The candidate either leaks `KeyError`/`TypeError` or accepts malformed inputs. Reproduction: the corresponding held-out tests.
4. **Mutable payload leak (maintainability: moderate).** The candidate shares the input payload dict with the output. Reproduction: `test_payload_is_copied`.

## Fix recommendation and acceptance

- Use `(tenant_id, event_id)` keys, validate every record, and retain the greatest timestamp (last occurrence on ties).
- Track the first occurrence order separately from the selected latest event.
- Copy the top-level payload dict and never modify caller inputs.
- Gate acceptance on **all public and held-out tests** passing against the submitted implementation, not merely a passing demonstration screenshot.

## Example grading rubric (10 points)

- Tenant isolation and dedupe semantics — 3
- Latest update and tie handling — 2
- Deterministic output order — 1
- Input validation and failure behavior — 2
- No input mutation and repeatable tests — 2

**Demonstration limitations:** This only shows how one engineered candidate can pass superficial public tests and fail stronger independent checks. There are no measured AI model pass rates or actual model comparisons in this package. To evaluate a real model, run the same task with an agent, preserve its source patch and execution trace, then score it using the withheld tests.
