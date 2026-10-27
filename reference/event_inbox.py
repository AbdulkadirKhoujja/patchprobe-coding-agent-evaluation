"""Reference implementation for tenant-safe, deterministic event ingestion."""


def ingest(events):
    if not isinstance(events, list):
        raise ValueError("events must be a list")

    by_key = {}
    first_seen_order = []
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("each event must be a dict")
        required = ("tenant_id", "event_id", "occurred_at", "payload")
        if any(k not in event for k in required):
            raise ValueError("an event is missing a required field")

        tenant_id, event_id = event["tenant_id"], event["event_id"]
        occurred_at, payload = event["occurred_at"], event["payload"]
        if not isinstance(tenant_id, str) or not tenant_id.strip():
            raise ValueError("tenant_id must be a nonblank string")
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError("event_id must be a nonblank string")
        if isinstance(occurred_at, bool) or not isinstance(occurred_at, int) or occurred_at < 0:
            raise ValueError("occurred_at must be a nonnegative integer")
        if not isinstance(payload, dict):
            raise ValueError("payload must be a dict")

        key = (tenant_id, event_id)
        normalized = {
            "tenant_id": tenant_id,
            "event_id": event_id,
            "occurred_at": occurred_at,
            "payload": dict(payload),
        }
        if key not in by_key:
            first_seen_order.append(key)
            by_key[key] = normalized
        elif occurred_at >= by_key[key]["occurred_at"]:
            by_key[key] = normalized

    return [by_key[key] for key in first_seen_order]
