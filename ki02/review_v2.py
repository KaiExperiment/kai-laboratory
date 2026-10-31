"""KI-02 versioned audit events with explicit evidence-context binding.

V1 events remain readable for historical verification, but cannot authorise
v2 context-bound decisions. This is tamper-evident, not authenticated.
"""
import hashlib
import json
from datetime import datetime, timezone
from .review_log import verify as verify_v1, GENESIS
from .review_bound import context_digest
from .review_recheck import evaluate_with_source_recheck

FIELDS = frozenset(("schema_version", "timestamp_utc", "reviewer_id",
                    "observation_id", "source_sha256", "context_sha256",
                    "relevance_reviewed", "provenance_reviewed", "rationale"))

def _hash(previous, payload):
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(previous.encode("ascii") + b"\n" + encoded).hexdigest()

def verify_v2(events):
    previous = GENESIS
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    for n, event in enumerate(events, 1):
        if not isinstance(event, dict) or set(event) != {"sequence", "previous_hash", "payload", "entry_hash"}:
            raise ValueError("invalid event shape")
        payload = event["payload"]
        if not isinstance(payload, dict) or set(payload) != FIELDS or type(payload["schema_version"]) is not int or payload["schema_version"] != 2:
            raise ValueError("invalid audit schema version")
        for key in ("timestamp_utc", "reviewer_id", "observation_id", "rationale"):
            if not isinstance(payload[key], str) or not payload[key].strip():
                raise ValueError("invalid review field")
        for key in ("source_sha256", "context_sha256"):
            value = payload[key]
            if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                raise ValueError("invalid digest")
        for key in ("relevance_reviewed", "provenance_reviewed"):
            if type(payload[key]) is not bool:
                raise ValueError("invalid review flag")
        if type(event["sequence"]) is not int or event["sequence"] != n or event["previous_hash"] != previous:
            raise ValueError("broken audit chain")
        digest = _hash(previous, payload)
        if event["entry_hash"] != digest:
            raise ValueError("altered audit event")
        previous = digest
    return previous

def add_v2_event(events, *, observation, source_sha256, reviewer_id,
                 relevance_reviewed, provenance_reviewed, rationale):
    previous = verify_v2(events)
    payload = {
        "schema_version": 2,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "reviewer_id": reviewer_id,
        "observation_id": observation["id"],
        "source_sha256": source_sha256,
        "context_sha256": context_digest(observation, source_sha256),
        "relevance_reviewed": relevance_reviewed,
        "provenance_reviewed": provenance_reviewed,
        "rationale": rationale,
    }
    event = {"sequence": len(events) + 1, "previous_hash": previous,
             "payload": payload, "entry_hash": _hash(previous, payload)}
    result = [*events, event]
    verify_v2(result)
    return result

def evaluate_v2(case, prepared, decisions, source_root, events,
                *, expected_head=None, minimum_sequence=0):
    head = verify_v2(events)
    if expected_head is not None and expected_head != head:
        raise ValueError("audit checkpoint mismatch")
    if type(minimum_sequence) is not int or minimum_sequence < 0 or len(events) < minimum_sequence:
        raise ValueError("audit rollback")
    observations = case.get("observations")
    items = prepared.get("review_items")
    if not isinstance(observations, list) or not isinstance(items, list) or not isinstance(decisions, dict):
        raise ValueError("invalid review input")
    by_item = {item["id"]: item for item in items}
    by_obs = {obs["id"]: obs for obs in observations}
    if len(by_item) != len(items) or len(by_obs) != len(observations) or set(by_item) != set(by_obs) or set(decisions) != set(by_obs):
        raise ValueError("observation coverage mismatch")
    latest = {event["payload"]["observation_id"]: event["payload"] for event in events}
    for identifier, observation in by_obs.items():
        event = latest.get(identifier)
        item = by_item[identifier]
        verdict = decisions[identifier]
        if event is None or not isinstance(verdict, dict):
            raise ValueError("missing audit approval")
        if event["context_sha256"] != context_digest(observation, item["source_sha256"]):
            raise ValueError("review context mismatch")
        if event["source_sha256"] != item["source_sha256"] or verdict.get("source_sha256") != item["source_sha256"]:
            raise ValueError("source mismatch")
        for field in ("relevance_reviewed", "provenance_reviewed"):
            if type(verdict.get(field)) is not bool or event[field] != verdict[field]:
                raise ValueError("review decision mismatch")
    return evaluate_with_source_recheck(case, prepared, decisions, source_root)

def verify_historical_v1(events):
    """Historical verification only. Never treat v1 events as v2 approval."""
    return verify_v1(events)
