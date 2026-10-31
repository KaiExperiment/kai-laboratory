# KI-02 integration audit — 2026-10-26

## Confirmed engineering status
GitHub Actions workflow for PR #34 head `aa5757c8be347b0c8afdcac9ba5829af44c60656`: completed, conclusion **success** (workflow run 40422210349). The PR remains a **draft** and has not been merged.

## What the integration test proves
The offline synthetic fixture exercises source-file reading, quotation matching, SHA-256 fingerprint generation, an abstention before review, and acceptance after *simulated* explicit approvals. It does not establish source truth, genuine human review, or real-world evidential accuracy.

## Critical limitations and bypasses
1. **Review decisions are not authenticated.** Any caller can supply a dictionary claiming flags are true. The code cannot distinguish a reviewer from an automated process.
2. **Source freshness is not rechecked at decision time.** `evaluate_reviewed_case` compares a supplied hash to a previously prepared hash; it does not reopen the original file. A source may change after queue preparation.
3. **The review queue checks substring presence, not citation context or relevance.** A quote can exist in a source while being negated, hypothetical, or about a different claim.
4. **Independence is operator-declared.** Two records may share a real underlying source despite different declared independence groups.
5. **Review provenance and source provenance are distinct.** Boolean fields only indicate that someone asserted a review occurred; they do not prove its quality.
6. **Policy is deliberately simplistic.** Two supporting groups with no counter groups cause acceptance regardless of study quality; any mixture causes abstention. This is a fixture policy, not a scientific inference engine.
7. **No end-to-end immutable audit trail yet.** The integration fixture does not persist signed reviewer identities, source snapshot, decision rationale or timestamps.
8. **The diagnostic classifier failed paraphrase generalisation.** Proposal 002 achieved 4/12 on additional synthetic cases, so it is not promoted.
9. **Public holdout is not secret.** The repository's original holdout cases are visible; do not present them as blind validation.

## Decision
Keep PR #34 **draft**, do not promote the classifier or treat synthetic approvals as real. Next work should harden source snapshot binding and reviewer provenance, then introduce independent case labels and a reproducible evaluation protocol. No spending or external communications authorised by this audit.
