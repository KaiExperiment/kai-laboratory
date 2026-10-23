# Evidence Engine 0.4 — real Chromium and CI verification

**Date:** 2026-10-23 (UTC). **Author:** AI-directed Kai Laboratory experiment (GPT-6); human-supervised project. **Status:** experimental draft PR #26; not released.

## Hypothesis
The local-calendar-date correction in `evidence-engine.html` prevents incorrect rejection of today's date near timezone boundaries, without breaking core browser interactions.

## Method and reproducibility
- Independently fetched original and corrected embedded application scripts from GitHub. FNV-1a byte checks on both matched the earlier local reconstruction (original `cdc2a402`; corrected `4a848470`). FNV is a transcription check, **not** a cryptographic proof.
- Executed `tests/evidence-engine.browser.cjs` with headless Chromium 144 and Playwright locally, using a reconstructed HTML shell containing the actual corrected application script and real DOM elements.
- Nine browser-clock/timezone cases checked demo date, acceptance of local today, and rejection of local tomorrow: UK midnight, Los Angeles, Kathmandu, Kiritimati, Honolulu, both sides of the UK DST fall-back, UTC control and Auckland leap day.
- Four additional viewport scenarios (320, 390, 768, 1280 px) exercised add/remove, synthetic demo, HTML-escaping of entered text, CSV download and clearing.
- Local original-script browser run **failed at the first UK midnight assertion** (UTC demo date 2026-10-22 vs expected local 2026-10-23). Local corrected-script run **passed 13/13 scenarios**. The original-script browser run was fail-fast, so it does not establish a full baseline failure count.
- Published the browser test and a read-only GitHub Actions workflow. The workflow checked out the **complete repository**, executed `node --test tests/evidence-engine-local-date.test.cjs`, installed Playwright/Chromium, and executed `node tests/evidence-engine.browser.cjs` against the checked-out `evidence-engine.html`.

## Independently verified CI outcome
**GitHub Actions run:** https://github.com/KaiExperiment/kai-laboratory/actions/runs/39932914891

**Commit under test:** `7e4543e3e948f93f2fc1bbd911d7eecb99aa9450`

**Result:** completed / success (2026-10-23 09:35 UTC).
- Node regression suite: **9 tests, 9 passed, 0 failed**.
- Real Chromium suite: **13/13 browser scenarios passed**, including nine timezone cases and four interaction/viewport cases.
- Verified by reading GitHub's workflow-run metadata, job steps and job logs after completion.

## Limitations
- All listings and dates were synthetic; no commercial evidence or third-party sources were validated.
- Chromium only; Firefox, WebKit, physical devices and accessibility audits are untested.
- Browser scenarios check the stated interactions and overflow but do **not** constitute exhaustive product or site-wide regression testing.
- The local reconstructed HTML was not a complete checkout; the subsequent **CI run did use a complete checkout**.
- No independent human code review or production monitoring. PR #26 should remain draft pending review and a deliberate release decision.

**Scientific conclusion:** the original timezone-boundary defect is reproducible in Chromium and the proposed correction passes the stated automated tests in a complete repository checkout. This is evidence for this bounded fix, not proof of general reliability.
