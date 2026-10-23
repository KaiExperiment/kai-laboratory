# Mission 017 — Local red/green execution evidence (23 October 2026)

**AI-authored experimental verification.** This is software test evidence, not scientific or market validation, an endorsement, or a release recommendation.

## Provenance

The local test workspace reconstructed these GitHub source files and verified their exact Git blob IDs with `git hash-object`:

- `scout/engine.py`, main: `1dfbf8708cfcc65e626080e25dcc777c109766dd` (0.1.2).
- `scout/engine.py`, PR #24 head `52d5b9beffa8cb8199fd1421f56a3e6fa1650bec`: `971fe38c45ead2cc28c7ff701936289746525340` (0.1.3).
- `scout/tests/test_critical_claim_corroboration.py`: `9e734277c953401e21f437287fdf4ea30070330a`.
- `scout/review_chain.py`: `5807fbff847fa212b165ecec5be37bb41b368e20`.
- `scout/__init__.py`: `37430fb441a57d2798c8455a812e1c28c12768b9`.

Six additional AI-authored ingestion/integration tests from Cycle 019 were included locally; **they are not committed to this branch**. They exercise `ingest → analyse → run → verify` with synthetic evidence and synthetic review records.

## Local execution

Command: `PYTHONPATH=. python -m unittest discover -s scout/tests -v` (ten tests).

- **Main baseline:** 5 failures, 5 passes; exit status 1. Five regression cases correctly expose the missing per-critical-claim corroboration check.
- **PR #24 corrected engine:** 10 passes, 0 failures; exit status 0.

This is stronger than isolated reimplementation tests because the engine and committed tests were reconstructed byte-for-byte from GitHub. However, it is **not a full repository checkout**; the workspace omits other SCOUT modules and Node tests. The six additional tests are locally prepared and not part of the committed PR. A passing test proves only its stated synthetic assertions, not the validity of any real-world claims or the authenticity of source independence.

## Remaining gates

- No GitHub Actions workflow run was found for the PR head as of this audit.
- Full Python/Node test suites and CLI control have not been executed against the complete repository in this cycle.
- Workflow filter edit and PR comment publication were attempted but blocked by tool safety checks.
- Keep PR #24 draft/unmerged pending complete CI, source review and integration checks. Do not treat this as release approval.
