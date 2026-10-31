# KI-02 — Checkpoint extension experiment (2026-10-31)

## Objective
Prevent a valid-looking rewritten audit chain from silently replacing the
history previously witnessed by an independent checkpoint holder.

## Protocol
1. Independently retain a checkpoint with a stream identifier, sequence and
   head SHA-256. Keep it **outside** the review log's trust boundary.
2. When receiving an extended chain, verify the prefix of exactly the
   checkpointed length against the trusted checkpoint.
3. Verify the entire extended chain is internally consistent.
4. Produce a *candidate* new checkpoint. Promotion of that candidate to
   trusted status is an explicit external operation; never automatic.

## Adversarial test matrix
- Valid extension → candidate checkpoint, eligible for external approval.
- Rehashed replacement of old events → reject against original checkpoint.
- Truncated prefix → reject.
- Wrong stream → reject.
- Attacker-controlled replacement checkpoint → undetectable within this
  protocol; demonstrates necessity of independent trust.

## What this does NOT prove
- Reviewers are authenticated.
- A checkpoint file cannot be overwritten or rolled back by an attacker.
- The appended events are trustworthy or independently corroborated.
- A review is truthful or its independence group is genuinely independent.
- A decision is safe in a consequential setting.

## Engineering notes
`review_checkpoint.py` checks exact checkpoint-to-chain equality.
`review_extension.py` separately checks prefix continuity and emits a
candidate new checkpoint. This distinction prevents an accidental acceptance
of a rewritten prefix when a new head is proposed.

The current tests are synthetic. Check GitHub Actions before calling the
new implementation verified. Keep PR #34 draft and unmerged.
