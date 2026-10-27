import unittest
from event_inbox import ingest


def ev(tenant='acme', eid='e1', at=10, payload=None):
    return {'tenant_id': tenant, 'event_id': eid, 'occurred_at': at, 'payload': {'x': 1} if payload is None else payload}


class HoldoutTests(unittest.TestCase):
    def test_same_id_different_tenants_must_survive(self):
        a, b = ev(tenant='a'), ev(tenant='b')
        self.assertEqual(ingest([a, b]), [a, b])

    def test_newest_update_wins(self):
        a, newer = ev(at=4), ev(at=9, payload={'x': 2})
        self.assertEqual(ingest([a, newer]), [newer])

    def test_equal_timestamp_uses_later_occurrence(self):
        a, latter = ev(at=4), ev(at=4, payload={'x': 2})
        self.assertEqual(ingest([a, latter]), [latter])

    def test_first_seen_key_order_stable_after_updates(self):
        a, b, newest_a = ev(eid='a', at=1), ev(eid='b', at=2), ev(eid='a', at=9)
        self.assertEqual(ingest([a, b, newest_a]), [newest_a, b])

    def test_payload_is_copied(self):
        a = ev()
        result = ingest([a])
        result[0]['payload']['x'] = 999
        self.assertEqual(a['payload']['x'], 1)

    def test_non_dict_rejected(self):
        with self.assertRaises(ValueError):
            ingest([None])

    def test_missing_required_field_rejected(self):
        with self.assertRaises(ValueError):
            ingest([{'tenant_id': 'a', 'event_id': 'x', 'occurred_at': 1}])

    def test_boolean_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            ingest([ev(at=True)])

    def test_blank_tenant_rejected(self):
        with self.assertRaises(ValueError):
            ingest([ev(tenant='  ')])

    def test_negative_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            ingest([ev(at=-1)])

    def test_non_list_rejected(self):
        with self.assertRaises(ValueError):
            ingest((ev(),))

    def test_extra_fields_are_not_leaked(self):
        original = ev()
        original['secret_unused_extra'] = 'opaque'
        self.assertEqual(ingest([original]), [ev()])
