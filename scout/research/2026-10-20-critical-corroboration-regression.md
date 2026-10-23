# Mission 017 — Critical-claim corroboration regression

**20 October 2026. AI-authored experimental research. Not a validated product release.**

The existing `scout/engine.py` computes a proposal-wide count of independent sources, then uses it to gate shortlisting. This may permit a critical claim supported by only one source to benefit from evidence attached to an unrelated claim. Exact-quote matching does not establish semantic support.

A new test file, `scout/tests/test_critical_claim_corroboration.py`, has been committed to this branch. It contains three adversarial cases that are **expected to fail against the current main implementation**, plus one positive control. These expectations derive from source inspection and prior local reproduction; **these newly committed tests have not been run in GitHub Actions**.

The attempted change to `scout/engine.py` was blocked by tool safety checks. A new GitHub Actions regression workflow and draft PR creation were also blocked. **Do not merge this branch as a green fix.** Main remains unmodified.

Acceptance gate: add a claim-specific check requiring at least two nonduplicate sources in distinct declared independence groups for every traceable critical claim in a real-source shortlist; retain fixture-only test behavior; run the four tests red-before and green-after; run the existing Python and Node suites in CI; review outcomes before merging.

Limitations: independence groups are operator-supplied, two quotes are not proof of truth, and semantic review is an unauthenticated assertion.
