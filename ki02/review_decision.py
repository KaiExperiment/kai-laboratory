"""KI-02: strict handoff from offline source review to decision policy.

Review records must be supplied by an authorised reviewer; this module cannot
authenticate the reviewer. It never promotes draft review flags into approval.
"""
from __future__ import annotations
from .evidence_schema import assess

def evaluate_reviewed_case(case, prepared, decisions):
    if case.get("claim_id") != prepared.get("claim_id"):
        raise ValueError("claim mismatch")
    observations = case.get("observations")
    items = prepared.get("review_items")
    if not isinstance(observations, list) or not isinstance(items, list):
        raise ValueError("missing observations or review items")
    by_id = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("invalid review item")
        if item["id"] in by_id:
            raise ValueError("duplicate review item")
        by_id[item["id"]] = item
    if set(by_id) != {o.get("id") for o in observations} or len(by_id) != len(observations):
        raise ValueError("review item mismatch")
    if not isinstance(decisions, dict) or set(decisions) != set(by_id):
        raise ValueError("decisions must cover every observation")
    updated = []
    for observation in observations:
        item = by_id[observation["id"]]
        verdict = decisions[observation["id"]]
        if not isinstance(verdict, dict):
            raise ValueError("invalid reviewer decision")
        if set(verdict) != {"relevance_reviewed", "provenance_reviewed", "source_sha256"}:
            raise ValueError("unexpected reviewer decision fields")
        for field in ("relevance_reviewed", "provenance_reviewed"):
            if type(verdict[field]) is not bool:
                raise ValueError("review flags must be boolean")
        if item.get("status") != "ready_for_human_review":
            if verdict["relevance_reviewed"] or verdict["provenance_reviewed"]:
                raise ValueError("cannot approve unavailable or mismatched source")
        if not isinstance(item.get("source_sha256"), str) or verdict["source_sha256"] != item["source_sha256"]:
            raise ValueError("source fingerprint mismatch")
        updated.append({**observation,
                        "relevance_reviewed": verdict["relevance_reviewed"],
                        "provenance_reviewed": verdict["provenance_reviewed"]})
    return assess({"claim_id": case["claim_id"], "observations": updated})
