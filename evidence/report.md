# Executed evidence — synthetic coding-agent evaluation

Run with `python evaluate.py`. `candidate` is a **deliberately flawed synthetic patch**, not a claim about real LLM performance.

| Implementation | Suite | Tests | Outcome |
|---|---|---:|---|
| candidate | public | 4 | PASS |
| candidate | holdout | 12 | FAIL (expected for seeded candidate) |
| reference | public | 4 | PASS |
| reference | holdout | 12 | PASS |

## Seeded candidate failures (observed)

- test_missing_required_field_rejected (test_holdout.HoldoutTests.test_missing_required_field_rejected)
- test_non_dict_rejected (test_holdout.HoldoutTests.test_non_dict_rejected)
- test_blank_tenant_rejected (test_holdout.HoldoutTests.test_blank_tenant_rejected)
- test_boolean_timestamp_rejected (test_holdout.HoldoutTests.test_boolean_timestamp_rejected)
- test_equal_timestamp_uses_later_occurrence (test_holdout.HoldoutTests.test_equal_timestamp_uses_later_occurrence)
- test_first_seen_key_order_stable_after_updates (test_holdout.HoldoutTests.test_first_seen_key_order_stable_after_updates)
- test_negative_timestamp_rejected (test_holdout.HoldoutTests.test_negative_timestamp_rejected)
- test_newest_update_wins (test_holdout.HoldoutTests.test_newest_update_wins)
- test_payload_is_copied (test_holdout.HoldoutTests.test_payload_is_copied)
- test_same_id_different_tenants_must_survive (test_holdout.HoldoutTests.test_same_id_different_tenants_must_survive)

## Interpretation
The public suite alone does not establish correctness. Held-out checks expose global-event-ID deduplication, stale-event selection, unsafe input handling and mutable payload sharing. The reference implementation passes the same checks. These are local test observations about two given Python files, not empirical AI model benchmark scores.

See `REVIEW.md` for PR-style review and remedial acceptance criteria.
