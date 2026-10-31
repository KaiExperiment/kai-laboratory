"""KI-02 context-bound review events (synthetic research implementation).

Binding is not authentication: reviewers and trusted checkpoints remain external.
"""
import hashlib
import json
from .review_log import add_event, verify
from .review_audited import evaluate_with_audit_log

FIELDS = ("id", "claim_id", "source_id", "independence_group",
          "stance", "source_path", "quote")

def context_digest(observation, source_sha256):
    context = {key: observation[key] for key in FIELDS}
    context["source_sha256"] = source_sha256
    if any(not isinstance(value, str) or not value.strip() for value in context.values()):
        raise ValueError("invalid review context")
    encoded = json.dumps(context, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def add_bound_event(events, *, observation, source_sha256, reviewer_id,
                    relevance_reviewed, provenance_reviewed, rationale):
    digest = context_digest(observation, source_sha256)
    # Interim v1-compatible format; future schema should have a dedicated field.
    return add_event(events, reviewer_id=reviewer_id,
                     observation_id=observation["id"],
                     source_sha256=source_sha256,
                     relevance_reviewed=relevance_reviewed,
                     provenance_reviewed=provenance_reviewed,
                     rationale="context-sha256:" + digest + "|" + rationale)

def evaluate_bound_case(case, prepared, decisions, source_root, events,
                        *, expected_head=None, minimum_sequence=0):
    verify(events)
    observations = case.get("observations")
    items = prepared.get("review_items")
    if not isinstance(observations, list) or not isinstance(items, list):
        raise ValueError("missing observations")
    if len({o.get("id") for o in observations if isinstance(o, dict)}) != len(observations):
        raise ValueError("duplicate observations")
    by_item = {item["id"]: item for item in items}
    if len(by_item) != len(items):
        raise ValueError("duplicate review items")
    latest = {event["payload"]["observation_id"]: event["payload"] for event in events}
    for observation in observations:
        identifier = observation["id"]
        if identifier not in by_item or identifier not in latest:
            raise ValueError("missing context review")
        digest = context_digest(observation, by_item[identifier]["source_sha256"])
        if not latest[identifier]["rationale"].startswith("context-sha256:" + digest + "|"):
            raise ValueError("review context changed or unbound")
    return evaluate_with_audit_log(
        case, prepared, decisions, source_root, events,
        expected_head=expected_head, minimum_sequence=minimum_sequence)
