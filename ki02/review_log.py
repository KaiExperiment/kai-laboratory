"""KI-02 append-only *tamper-evident* review event log.

Hash chaining detects accidental or unsanctioned edits if a trusted copy of
the final digest is retained separately. It does not authenticate reviewer
identity, prevent truncation, or protect against an attacker rewriting all
entries and their hashes. Do not store personal identifiers or secrets here.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

GENESIS = "0" * 64
FIELDS = ("timestamp_utc", "reviewer_id", "observation_id", "source_sha256",
          "relevance_reviewed", "provenance_reviewed", "rationale")

def _canonical(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def _hash(previous, payload):
    return hashlib.sha256(previous.encode("ascii") + b"\n" + _canonical(payload)).hexdigest()

def verify(events):
    previous = GENESIS
    for number, event in enumerate(events, 1):
        if not isinstance(event, dict) or set(event) != {"sequence", "previous_hash", "payload", "entry_hash"}:
            raise ValueError("invalid event shape")
        if event["sequence"] != number or event["previous_hash"] != previous:
            raise ValueError("broken sequence or chain")
        payload = event["payload"]
        if not isinstance(payload, dict) or set(payload) != set(FIELDS):
            raise ValueError("invalid payload shape")
        for key in ("timestamp_utc", "reviewer_id", "observation_id", "source_sha256", "rationale"):
            if not isinstance(payload[key], str) or not payload[key].strip():
                raise ValueError("invalid payload field")
        for key in ("relevance_reviewed", "provenance_reviewed"):
            if type(payload[key]) is not bool:
                raise ValueError("review flags must be boolean")
        if len(payload["source_sha256"]) != 64 or any(c not in "0123456789abcdef" for c in payload["source_sha256"]):
            raise ValueError("invalid SHA-256 fingerprint")
        if _hash(previous, payload) != event["entry_hash"]:
            raise ValueError("tampered event")
        previous = event["entry_hash"]
    return previous

def add_event(events, *, reviewer_id, observation_id, source_sha256,
              relevance_reviewed, provenance_reviewed, rationale, timestamp_utc=None):
    previous = verify(events)
    payload = {
        "timestamp_utc": timestamp_utc or datetime.now(timezone.utc).isoformat(),
        "reviewer_id": reviewer_id, "observation_id": observation_id,
        "source_sha256": source_sha256,
        "relevance_reviewed": relevance_reviewed,
        "provenance_reviewed": provenance_reviewed, "rationale": rationale,
    }
    entry = {"sequence": len(events) + 1, "previous_hash": previous,
             "payload": payload, "entry_hash": _hash(previous, payload)}
    verify([*events, entry])
    return [*events, entry]

def load(path):
    path = Path(path)
    if not path.exists():
        return []
    events = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(events, list):
        raise ValueError("log must be a list")
    verify(events)
    return events

def save_new(path, events):
    """Create a log only if absent; never silently overwrite an existing log."""
    verify(events)
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(events, handle, indent=2)
        handle.write("\n")
