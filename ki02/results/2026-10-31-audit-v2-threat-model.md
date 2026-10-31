# KI-02 — Audit schema v2 validation and threat model (2026-10-31)

## Scope
The version-2 audit event stores a dedicated `context_sha256` binding the
observation identifier, claim identifier, source identifier, independence group,
stance, source path, quoted passage, and source-byte SHA-256. A decision
rechecks source bytes and requires matching review flags and latest event.

## CI incident
Run #93 failed with two errors in inherited regression tests. Both invoked the
v1 `add_event`/`verify` functions against v2 records. The tests have been
updated to use v2 functions. CI success for the repair must be verified; do not
treat a successful commit as a passing test.

## Threat model and limitations
1. **Unverified identity:** `reviewer_id` is an unauthenticated string. A
   fabricated identity can be placed in a syntactically valid event.
2. **Whole-chain rewriting:** Hash chaining detects tampering only relative to
   a trusted independently stored head digest. The system does not protect or
   publish that digest itself.
3. **Rollback/replay:** A separately trusted head and sequence can reject
   older chains; absent a trusted checkpoint, a previously valid chain can
   still be replayed.
4. **Truth:** Quote presence, review flags and context binding do not establish
   source truth, relevance, or genuine independence.
5. **Race:** Source bytes are checked at decision time but not pinned as a
   single immutable snapshot for downstream consumers.
6. **Versioning:** Historical v1 events remain verifiable but must not be
   treated as v2 authorisation. The v1-compatible rationale-prefix approach
   is experimental and superseded by v2 for new review workflows.
7. **Reviewer withdrawal:** The most recent event for an observation wins.
   Earlier approvals must not override a later disapproval.

## Next experiments
- Independently retained checkpoints with atomic publication and verification.
- Authentication of reviewers or signed events, with a threat model for
  compromised signing keys.
- Distinct assessment identifiers and expiry/freshness constraints to avoid
  reusing an approval in an unintended evaluation session.
- Blind holdout cases and independent evaluation beyond synthetic fixtures.

No real-world evidence or reviewer identity has been authenticated by these tests.
PR #34 must remain draft and unmerged pending review.
