"""Construct hash-linked review history events; validation remains in engine.ingest.

This detects accidental or unsophisticated alteration, not a fully rewritten chain.
There is no authentication or external checkpoint.
"""
from .engine import encoded, sha, timestamp, nonempty, require

GENESIS = '0' * 64


def append_event(history, verdict, reviewer, rationale, reviewed_at):
    require(isinstance(history, list), 'History must be a list')
    require(verdict in ('approved', 'rejected', 'reopened'), 'Invalid review verdict')
    require(nonempty(reviewer) and nonempty(rationale), 'Reviewer and rationale required')
    when = timestamp(reviewed_at)
    if history:
        last = history[-1]
        require(timestamp(last['reviewed_at']) <= when, 'Review events must be chronological')
        require(nonempty(last.get('event_hash')), 'Previous event must have a hash')
        predecessor = last['event_hash']
    else:
        predecessor = GENESIS
    event = dict(verdict=verdict, reviewer=reviewer, rationale=rationale,
                 reviewed_at=when, previous_hash=predecessor)
    event['event_hash'] = sha(encoded(event))
    return [*history, event]
