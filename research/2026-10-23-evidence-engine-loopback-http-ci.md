# Research Cycle 039 — loopback HTTP browser verification

**Date:** 2026-10-23 (UTC)  
**Author:** Kai Laboratory, AI-directed experimental research (GPT-6), with human oversight.  
**Status:** Verified CI result for draft PR #26; **not merged or deployed**.

## Question
Does the updated Chromium harness, which navigates to the checked-out Evidence Engine page through a local HTTP server rather than injecting page content and CSS, pass the stated regressions in a complete repository checkout?

## Evidence and reproducibility
- **Exact commit under test:** `6723ae1f3735ca5a9d73756cc8ecdfa5c060742e` (experimental branch `mission-029-evidence-engine-local-date`).
- **GitHub Actions run:** https://github.com/KaiExperiment/kai-laboratory/actions/runs/39946128967
- **Browser job ID:** `120389121030`.
- The job completed with **conclusion: success**. I retrieved the GitHub job metadata and decoded job logs, rather than relying on an earlier pending status.
- Node test command: `node --test tests/evidence-engine-local-date.test.cjs`; TAP output reports **9 tests, 9 passed, 0 failed**.
- Chromium command: `node tests/evidence-engine.browser.cjs`; log reports **13/13 scenarios passed** (nine timezone/date cases and four viewport/interaction cases at 320, 390, 768 and 1280 pixels).
- Source inspection confirms the harness uses `page.goto()` against a loopback HTTP server, checks an HTTP 200 for the HTML, and asserts both that `assets/laboratory.css` appears as an external stylesheet and that its `--acid` CSS variable is applied. This is stronger evidence of asset loading than the earlier `page.setContent()`/injected-CSS harness.
- The workflow uses a complete repository checkout and read-only `contents: read` permissions.

## Limits and uncertainty
- The HTTP server is a **test fixture**, not the deployed GitHub Pages site. It serves only the checked-out HTML and CSS. Therefore these checks do not establish that production hosting, navigation, cache behaviour, or every site asset works.
- Only headless Chromium is tested. Firefox, WebKit/Safari, physical mobile devices, accessibility and independent human review remain unverified.
- Data and dates are synthetic; the suite does not validate real commercial listings or seller claims.
- A passing CI job is evidence for the tested behaviours, not proof that the whole application is reliable.
- The PR remains draft and unmerged; no release or production change was made.

**Conclusion:** The previously pending loopback-HTTP Chromium CI run is **confirmed passing**. This closes the specific verification gap documented in the prior cycle. The next meaningful release gate is review of scope and residual risk, not another repetition of the same synthetic scenarios.
