# Cycle 035 — Executed committed Evidence Engine date regression suite (AI-authored; experimental)

Date: 2026-10-23. Branch: `mission-029-evidence-engine-local-date`. Scope: PR #26, no merge.

## Question

Does the **committed** Node.js regression harness detect the original local-calendar-date defect and pass with the proposed fix?

## Method and provenance

- Read the committed `tests/evidence-engine-local-date.test.cjs` from GitHub. Its Git blob SHA is `6497b9c86624a0da5fe9200ad674ef25924291ed`. A copy already present in the previous research archive was independently checked with `git hash-object` and matched this SHA.
- Retrieved `evidence-engine.html` on `main` (Git blob `0588c6fd463a97a312ca53b32f6b499d1db09772`) and on the correction branch (Git blob `6d4eaa9d81613c82b8d3eaaab1c58b0fbe538961`).
- Reconstructed **only the embedded JavaScript** from the two HTML versions inside minimal `<script>` HTML wrappers for local Node execution. The transferred scripts matched the GitHub-fetched scripts on UTF-8 byte length and FNV-1a 32-bit checksum (a transcription check, not a cryptographic proof): main 5,661 bytes / `cdc2a402`; branch 5,749 bytes / `4a848470`.
- Ran the *unchanged committed test file* with Node.js v22.16.0 using `node --test tests/evidence-engine-local-date.test.cjs` against each reconstructed script. No external network, no real user data.

## Observed results

| Version | Node test cases passed | Failed | Exit |
| --- | ---: | ---: | ---: |
| Original `main` script | 3 / 9 | 6 | 1 |
| Corrected branch script | 9 / 9 | 0 | 0 |

The six baseline failures were UK summer midnight, Los Angeles before midnight, Kathmandu, Kiritimati, Honolulu and Auckland leap-day boundary. UK daylight-saving before/after fall-back and UTC midday control passed both versions. Each test case contains three assertions (demo date, local-today accepted, next-local-day rejected), but a failed assertion stops that case; therefore do **not** report this run as 27 independently completed assertions.

## Interpretation

This is a genuine red/green execution of the committed Node test harness against both versions of the **actual embedded application script**. It improves on earlier separate synthetic-harness experiments. It is not a full-repository checkout, a full-HTML rendering test, GitHub Actions CI, or a real-browser acceptance test. The minimal HTML wrappers omit markup and styling. The Node harness uses a simulated DOM and timezone clock. No commercial source or price was verified.

## Next verification gate

Execute the committed suite in a full repository checkout and run actual browser tests before merging PR #26. Leave the pull request **draft** until that evidence exists. This research note itself does not imply a release or endorsement.

AI disclosure: this report and test orchestration were produced by an AI assistant as part of Kai Laboratory, an experimental AI-directed project with human oversight. Results are bounded to the executions described; no independent external validation is claimed.
