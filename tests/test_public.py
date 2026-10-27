import unittest
from event_inbox import ingest


def ev(tenant='acme', eid='e1', at=10, payload=None):
    return {'tenant_id': tenant, 'event_id': eid, 'occurred_at': at, 'payload': {'x': 1} if payload is None else payload}


class PublicTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(ingest([]), [])

    def test_single_event(self):
        self.assertEqual(ingest([ev()]), [ev()])

    def test_two_distinct_ids(self):
        self.assertEqual(ingest([ev(eid='a'), ev(eid='b')]), [ev(eid='a'), ev(eid='b')])

    def test_identical_duplicate(self):
        self.assertEqual(ingest([ev(), ev()]), [ev()])
