"""KI-02 externally retained checkpoint protocol (experimental).

A checkpoint is only trusted when retained independently of the log and
supplied by a trusted caller. This module does not implement secure storage,
identity verification, signing, or atomic multi-system publication.
"""
import hashlib
import json
from .review_v2 import verify_v2, evaluate_v2

CHECKPOINT_VERSION = 1

def _digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def make_checkpoint(events, *, stream_id):
    if not isinstance(stream_id, str) or not stream_id.strip():
        raise ValueError("stream identifier required")
    return {"checkpoint_version": CHECKPOINT_VERSION, "stream_id": stream_id,
            "sequence": len(events), "head_sha256": verify_v2(events)}

def verify_checkpoint(events, checkpoint, *, stream_id, minimum_sequence=0):
    if not isinstance(checkpoint, dict) or set(checkpoint) != {
        "checkpoint_version", "stream_id", "sequence", "head_sha256"
    }:
        raise ValueError("invalid checkpoint")
    if type(checkpoint["checkpoint_version"]) is not int or checkpoint["checkpoint_version"] != CHECKPOINT_VERSION:
        raise ValueError("unsupported checkpoint version")
    if not isinstance(stream_id, str) or not stream_id.strip() or checkpoint["stream_id"] != stream_id:
        raise ValueError("checkpoint stream mismatch")
    if type(checkpoint["sequence"]) is not int or checkpoint["sequence"] < 0:
        raise ValueError("invalid checkpoint sequence")
    if type(minimum_sequence) is not int or minimum_sequence < 0:
        raise ValueError("invalid minimum sequence")
    if checkpoint["sequence"] < minimum_sequence or len(events) != checkpoint["sequence"]:
        raise ValueError("audit sequence mismatch")
    if checkpoint["head_sha256"] != verify_v2(events):
        raise ValueError("audit head mismatch")
    return checkpoint["head_sha256"]

def evaluate_with_checkpoint(case, prepared, decisions, source_root, events,
                             checkpoint, *, stream_id, minimum_sequence=0):
    verified_head = verify_checkpoint(events, checkpoint, stream_id=stream_id,
                                      minimum_sequence=minimum_sequence)
    return evaluate_v2(case, prepared, decisions, source_root, events,
                       expected_head=verified_head, minimum_sequence=minimum_sequence)
