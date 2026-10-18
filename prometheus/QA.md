# Ignition 001 — observed validation and review notes

Executed 18 October 2026. This document records actual checks of the proposed branch; it does not claim deployment or production verification.

## Computational experiment

- Full default protocol executed: **480 runs, zero failed runs**. 240 exploration runs, followed by 240 validation runs for the frozen winner and baseline. Raw final tours and metrics are retained.
- Frozen candidate: **two_opt**. Exploration mean paired tour-length reductions: 2-opt **9.6995%**, relocation **2.9778%**, annealing **8.6317%**. Relocation lost on two exploratory instance averages; all results remain in the record.
- Held-out result: **8.3322%** mean reduction, **3.6192%** instance SD, bootstrap 95% interval **7.2818%–9.4935%**, instance wins/ties/losses **40/0/0**. The predefined success criterion passed.
- An independent full run matched protocol, source hashes, all 480 final tours, scientific metrics, reviews and decisions exactly. Timing/host fields were deliberately excluded.
- A fresh copied source/evidence directory was also run with `python3 -S` (site packages disabled); the documented pipeline and verifier passed. No downloaded dependencies were used by the prototype.
- **12 Python engine tests passed**: deterministic instances/search, closed-tour scoring, square optimum, exhaustive seven-city lower bounds, permutation preservation, actual objective-call budgets, invalid input, Skeptic rejection, split leakage, selection thresholds/ties, failure recording, instance-level analysis and a complete negative-result pipeline. Test count is 12; several test cases cover multiple conditions.
- Manifest hashes were checked against the final Python source and tests. The protocol and search algorithms were fixed before the first real run. Later edits clarified reporting, provenance and strategy-specific Skeptic risks; full regenerated evidence and independent reproduction retained identical scientific outcomes. This was not externally preregistered or independently blinded.

## Website and preservation

- New `prometheus/index.html` is reachable from headquarters navigation and a new Mission 003 log entry. Existing log entries, inventions and records remain intact. The existing homepage CSS was retained; the research page uses its palette and typography.
- New Playwright/Chromium checks passed **7 widths: 320, 375, 390, 430, 768, 1024 and 1440px**. Mobile widths use mobile/touch emulation; JavaScript is disabled throughout. Checks cover horizontal overflow, one H1, language, keyboard skip link, anchors, every local evidence link, displayed result versus JSON, scoped table headers, labelled plots, reduced-motion behavior, headquarters navigation round trip and no external page requests or page exceptions.
- Full-page screenshots were visually inspected at **390px and 1440px**. No horizontal overflow was observed. The two plotted tours are the first predefined validation instance/search seed, not a performance-selected illustration.
- Existing headquarters browser suite passed all **7 viewport scenarios** and JavaScript-disabled navigation.
- Existing calculator: **10 model tests passed**, including the deterministic 500-case price sweep; **6 browser viewport scenarios passed**, plus the JavaScript-disabled explanation.
- `git diff --check` passed. Maker Profit Calculator and all pre-existing records/tests are byte-identical to the current main snapshot used as this branch's base (`2d0e94d912d06dc111f8423e2f6c1b5d326807e7`). Only headquarters navigation and the additional Mission 003 entry change an existing tracked file.

## Failures and verification limits

- The supplied local checkout was older than current main. Shell Git access failed because the proxy was unavailable, and `gh auth status` reported an invalid CLI token. The authorized GitHub connector supplied the exact latest main snapshot and is used for the review branch/PR. Existing files were checked against that snapshot, not the stale checkout.
- The sandbox initially blocked the local HTTP server. The localhost-only server and browser checks were then run through the approved execution path.
- The first new browser suite passed 320/375/390px, then timed out waiting for a headquarters navigation link to stabilize after smooth scrolling. Its rerun enables reduced motion before navigation, and all seven scenarios pass. Website behavior was not changed to hide the failure.
- Axe-core was unavailable; no axe conformance result is claimed. The cloud Sites preview reference also became unavailable during the task; browser QA used the repository's existing local Playwright/Chromium pattern. No Sites hosting operations were performed.
- No physical phone, Safari/WebKit, Firefox, screen reader, high-zoom manual audit or complete WCAG assessment was performed. Chromium emulation and semantic checks establish accessibility basics only.
- No production deployment, live GitHub Pages behavior or rendered Markdown behavior was tested. Local Markdown evidence returns HTTP 200 but may display as text/download depending on hosting. Review the final GitHub-rendered report and confirm existing hosting behavior before any future approved merge.

## Scope and next review

The branch is prepared for review only. No merge, deploy, publish, live-site configuration change, workflow addition or auto-merge is part of this mission. A future merge into the repository's existing Pages source may publish automatically; that is outside the authorization for this task.

The strongest research limitations and the recommended fresh-seed, multi-distribution, multi-size comparison against best-improvement 2-opt are in the research report. Treat this held-out set as spent for future confirmatory work.
