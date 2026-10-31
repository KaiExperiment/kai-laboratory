"""KI-02 checkpoint evolution: verify an append-only audit extension.

A trusted checkpoint must come from independent storage. This module checks
that an extended log retains the complete checkpointed prefix; it cannot
authenticate the origin of the supplied checkpoint or protect its storage.
"""
from .review_v2 import verify_v2
from .review_checkpoint import verify_checkpoint, make_checkpoint

def verify_extension(events, trusted_checkpoint, *, stream_id):
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    if not isinstance(trusted_checkpoint, dict):
        raise ValueError("trusted checkpoint required")
    sequence = trusted_checkpoint.get("sequence")
    if type(sequence) is not int or sequence < 0 or sequence > len(events):
        raise ValueError("invalid checkpoint sequence")
    # Verify both the checkpointed prefix and the full extended chain.
    verify_checkpoint(events[:sequence], trusted_checkpoint, stream_id=stream_id)
    verify_v2(events)
    return make_checkpoint(events, stream_id=stream_id)

def evaluate_extension(case, prepared, decisions, source_root, events,
                       trusted_checkpoint, *, stream_id):
    from .review_checkpoint import evaluate_with_checkpoint
    candidate = verify_extension(events, trusted_checkpoint, stream_id=stream_id)
    # The candidate is valid relative to the old checkpoint, but its new
    # events are NOT independently authenticated. Do not automatically promote
    # candidate to a trusted external checkpoint.
    result = evaluate_with_checkpoint(
        case, prepared, decisions, source_root, events,
        candidate, stream_id=stream_id,
        minimum_sequence=trusted_checkpoint["sequence"])
    return result, candidate
