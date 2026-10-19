# Mission 004 — The Human Experience

Prepared 19 October 2026 for founder review. Do not merge or publish until the founder has approved the experience on a physical iPhone. No deployment, hosting settings or workflows were changed.

## Structure and changed files

- `index.html`: concise introduction, three exploration destinations, bounded PROMETHEUS result and introduction to the collaborators.
- `experiments.html`: coin-toss and route-search stories, each covering question, attempt, result, learning and next step.
- `inventions.html`: working calculator entrance with an explicitly illustrative example.
- `mission.html`: founder/Kai roles, recorded progress, £0 starting budget, revenue aspiration versus evidence, and future ideas.
- `prometheus/index.html`: relatable delivery-route introduction and short explanation ahead of the preserved technical presentation, measured plots and evidence links in a native expandable notebook.
- `maker-profit-calculator.html`: shared navigation, back links, dark styling and top control. Calculation JavaScript unchanged.
- `assets/laboratory.css`: shared responsive design, native mobile menu, focus indicators and reduced-motion support. System fonts; no external assets or runtime dependencies.
- `tests/experience.browser.cjs`: end-to-end navigation, link, keyboard, top control and layout checks across six pages.
- `tests/headquarters.browser.cjs`, `tests/prometheus.browser.cjs`: existing assertions retained with selectors updated for separate destinations and the native mobile menu.
- `docs/review/`: proposed homepage screenshots at 390px and 1440px.
- This document records design and validation.

Scientific records, Python source, frozen protocols and result JSON remain unchanged. The ornamental homepage graphic is decorative, hidden from assistive technology and does not represent data. PROMETHEUS retains its labelled measured plots. Navigation and presentation work without JavaScript. Only the existing calculator needs JavaScript.

## Review locally

From the repository root, run `python3 -m http.server 8000` and open `http://localhost:8000/`. For iPhone review, serve this development checkout on a trusted local network and use the computer’s local address. This is a local review route, not a deployed preview. Do not merge merely to obtain a preview: the existing GitHub Pages source may publish automatically on merge.

## Validation

- Calculator mathematical suite: 10 passed, including the deterministic 500-case price sweep.
- PROMETHEUS engine suite: 12 passed.
- Existing calculator browser suite: six viewport scenarios (320, 375, 390, 430, 768, 1280px) and JavaScript-disabled explanation passed.
- New experience browser suite: six pages at 320, 390, 768 and 1440px. Checks HTTP responses for local links, absence of horizontal overflow, one h1, keyboard skip links, native mobile menu keyboard operation, minimum 44px menu links, back-to-top scroll position, reduced-motion scrolling, actual navigation across five destinations and navigation with JavaScript disabled.
- Existing headquarters and PROMETHEUS browser suites run using the updated navigation selectors; seven widths each (320, 375, 390, 430, 768, 1024, 1440px), all passed.
- Screenshots captured from a local HTTP server. Homepage mobile/desktop designs visually inspected.
- Full PROMETHEUS reproduction passed: protocol, source hashes, tours, metrics, reviews and decisions matched exactly (timings and host metadata excluded).
- `git diff --check` passed.

Browser QA uses development-only Playwright and Chromium. None is shipped to visitors. Local evidence links were requested and returned successfully; external GitHub/X destinations were not exhaustively tested. No physical iPhone, Safari/WebKit, VoiceOver or other screen reader was available. No full accessibility conformance audit is claimed. Mobile browser chrome, focus zoom, decimal keyboard, safe areas, landscape rotation and actual touch comfort require founder review on her iPhone. No live hosting or CI result is claimed.

## Founder iPhone review before publication

Review the five destinations and calculator at normal text size and with enlarged text. Open and close the menu, follow experiment/evidence links, scroll back to top, change calculator inputs and check the decimal keyboard. Confirm that the first screen explains the project and the three destinations feel obvious. Record approval in the PR before anyone merges.
