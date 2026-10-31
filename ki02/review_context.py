"""Bind review approvals to a canonical assessment context (KI-02 prototype).

A context digest is only a cryptographic binding, not a reviewer's identity
or proof of evidence quality. Review authority and checkpoints remain external.
"""
from __future__ import annotations
import hashlib
import json
from .review_log import verify
from .review_audited import evaluate_with_audit_log

CONTEXT_FIELDS = ("id", "claim_id", "source_id", "independence_group",
                  "stance", "source_path", "quote")

def context_digest(observation):
    if not isinstance(observation, dict):
        raise ValueError("invalid observation")
    context = {}
    for field in CONTEXT_FIELDS:
        value = observation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError("missing context field: " + field)
        context[field] = value
    canonical = json.dumps(context, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def evaluate_with_context_binding(case, prepared, decisions, source_root, events,
                                  *, context_approvals, expected_head=None,
                                  minimum_sequence=0):
    """Fail closed unless externally supplied context approvals bind each event.

    context_approvals maps observation ID to {entry_hash, context_sha256}.
    Caller must retain these approvals in a trusted, separately protected
    channel. They are not authenticated merely by appearing in a dictionary.
    """
    verify(events)
    observations = case.get("observations")
    if not isinstance(observations, list) or not isinstance(context_approvals, dict):
        raise ValueError("invalid context approvals")
    if len({o.get("id") for o in observations if isinstance(o, dict)}) != len(observations):
        raise ValueError("duplicate observation")
    if set(context_approvals) != {o["id"] for o in observations}:
        raise ValueError("context approval coverage mismatch")
    latest = {e["payload"]["observation_id"]: e for e in events}
    for observation in observations:
        identifier = observation["id"]
        event = latest.get(identifier)
        approval = context_approvals[identifier]
        if event is None or not isinstance(approval, dict):
            raise ValueError("missing context-bound event")
        if set(approval) != {"entry_hash", "context_sha256"}:
            raise ValueError("invalid context approval")
        if approval["entry_hash"] != event["entry_hash"]:
            raise ValueError("review event replay or mismatch")
        if approval["context_sha256"] != context_digest(observation):
            raise ValueError("review context changed")
    return evaluate_with_audit_log(
        case, prepared, decisions, source_root, events,
        expected_head=expected_head, minimum_sequence=minimum_sequence)
