"""Intentionally flawed simulated candidate patch. Not produced by a real AI model."""


def ingest(events):
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    seen = set()
    output = []
    for event in events:
        # BUG: event IDs are only unique within a tenant, not globally.
        event_id = event["event_id"]
        if event_id in seen:
            continue
        seen.add(event_id)
        # BUG: duplicates with a newer occurred_at are not considered.
        output.append({
            "tenant_id": event["tenant_id"],
            "event_id": event_id,
            "occurred_at": event["occurred_at"],
            "payload": event["payload"],  # BUG: shared mutable payload
        })
    return output
