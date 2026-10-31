"""Fail-closed audited decision path for synthetic KI-02 review experiments.

A valid hash chain is not authentication. The caller must protect its log,
checkpoint and review authority outside this module.
"""
from __future__ import annotations
from .review_log import verify
from .review_recheck import evaluate_with_source_recheck

def evaluate_with_audit_log(case, prepared, decisions, source_root, events,
                            *, expected_head=None, minimum_sequence=0):
    """Require a matching latest event for every observation before evaluation.

    expected_head is an independently retained digest when provided.
    minimum_sequence rejects older event chains if the caller persists a
    trusted monotonic sequence externally. Neither is trustworthy if supplied
    by the same untrusted party as the log.
    """
    head = verify(events)
    if expected_head is not None and head != expected_head:
        raise ValueError("audit checkpoint mismatch")
    if type(minimum_sequence) is not int or minimum_sequence < 0 or len(events) < minimum_sequence:
        raise ValueError("audit sequence rollback")
    items = prepared.get("review_items")
    if not isinstance(items, list) or not isinstance(decisions, dict):
        raise ValueError("invalid review input")
    if len({i.get("id") for i in items if isinstance(i, dict)}) != len(items):
        raise ValueError("duplicate review item")
    latest = {}
    for event in events:
        payload = event["payload"]
        latest[payload["observation_id"]] = payload
    if set(decisions) != {i["id"] for i in items}:
        raise ValueError("decision coverage mismatch")
    for item in items:
        identifier = item["id"]
        verdict = decisions[identifier]
        record = latest.get(identifier)
        if record is None:
            raise ValueError("missing audit review event")
        if not isinstance(verdict, dict) or record["source_sha256"] != item.get("source_sha256"):
            raise ValueError("audit source mismatch")
        if verdict.get("source_sha256") != record["source_sha256"]:
            raise ValueError("decision source mismatch")
        for field in ("relevance_reviewed", "provenance_reviewed"):
            if type(verdict.get(field)) is not bool or verdict[field] != record[field]:
                raise ValueError("audit decision mismatch")
    return evaluate_with_source_recheck(case, prepared, decisions, source_root)
