# Mission 002 — Operation Headquarters

Status: prepared for design review; not merged or published by this mission.

## What changed

- `index.html`: root-level, buildless public headquarters for the existing GitHub Pages site. Includes the laboratory introduction, four divisions, complete supplied milestone log, calculator feature and research principles.
- `tests/headquarters.browser.cjs`: optional development-only Playwright checks against a local HTTP server.
- `docs/mission-002-headquarters.md`: design, maintenance, validation and review notes.

All pre-existing files are preserved, including the audited v1.1 calculator, experiment record, README and Mission 001 tests/documentation. The branch starts from main after the Mission 001 merge (`3eda036`).

## Design and implementation

Ink-green surfaces, acid-green accents, editorial typography and an abstract orbital instrument give the page an experimental laboratory identity. The illustration is explicitly decorative, not research data. The mission log separates recorded results from current work; divisions describe areas of inquiry, not established accomplishments. No extra experiments, discoveries or researchers were invented. Only the supplied Mission 001 release date is shown in the log.

The page is approximately 18 KB uncompressed, with inline CSS, SVG and favicon, system fonts, and no JavaScript, remote fonts, packages, analytics, storage or external resource requests. All core content is available without JavaScript. Native `details` provides expandable principles. The only motion is anchor scrolling, disabled for reduced-motion preferences. Semantic landmarks, a skip link, visible focus indicators, wrapped navigation and minimum 44px navigation/primary-link heights support keyboard and touch use. Links to the calculator and experiment are relative, compatible with a GitHub Pages project subdirectory. The experiment link opens the existing raw Markdown resource; browser rendering/download behaviour depends on hosting.

No GitHub Pages settings, workflows, domains or publishing branches were changed. The GitHub Pages settings API could not be read from this environment (CLI returned Forbidden), so the exact current Pages branch/directory configuration has not been independently verified. This change follows the requested existing root `index.html` convention. Before merging, confirm the existing Pages source serves repository root and understand that merging to its source branch may publish the page automatically.

## Local review

From repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/`. No build or installation is required to view the site. To run browser checks, install Playwright in a development environment and provide a Chromium executable (neither is a website dependency):

```sh
CHROMIUM_PATH=/usr/bin/chromium node tests/headquarters.browser.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/maker-profit-calculator.browser.cjs
node tests/maker-profit-calculator.test.cjs
```

The headquarters test accepts `BASE_URL` for another local server URL. Do not point it at a production system: it is intended for local review. Update copy in the HTML and keep milestone statuses and dates grounded in verified records. No live experiment feed or automated status is implied.

## Observed QA — 18 October 2026

- Chromium, locally served over HTTP: **7 homepage viewport scenarios passed**, at 320, 375, 390, 430, 768, 1024 and 1440 CSS pixels. Mobile scenarios enable touch/mobile emulation. No horizontal overflow at those widths.
- Each scenario checked in-page anchor targets/navigation, keyboard skip link, mouse and keyboard operation of native details, reduced-motion scroll behaviour, local experiment/calculator HTTP responses, successful calculator navigation/default output, no homepage console errors or uncaught exceptions, and no external homepage network requests.
- Homepage navigation passed with JavaScript disabled.
- Existing calculator model suite: **10 tests passed, 0 failed**, including its deterministic 500-case price sweep. Existing calculator browser suite: **6 viewport scenarios passed**, plus its JavaScript-disabled explanation.
- Axe-core WCAG 2 A/AA and 2.1 A/AA checks at 390 and 1440px: **0 violations**, 22 rules passed at each width. Axe marked colour contrast and prohibited ARIA attributes for manual review. The redundant brand accessible label found during initial QA was removed and both sizes passed on rerun. Manual inspection found valid native disclosures and a labelled decorative graphic; text palette contrast was checked separately. This is not a full accessibility audit.
- Full-page Chromium captures visually inspected at 390px and 1440px. `git diff --check` passed. Existing calculator and other baseline files have no diff from current main.
- The homepage's initial missing favicon was corrected with an inline SVG favicon. No homepage browser errors remained after rerun.

## Still needs human review

- No real iPhone, iOS Safari or WebKit runtime was tested. Check Safari text sizing, glyph rendering, touch links, focus indicators, native disclosures, orientation changes, zoom, browser chrome and safe-area behaviour on a physical iPhone.
- No VoiceOver or other screen reader testing, full accessibility conformance audit, Firefox testing or live GitHub Pages deployment verification was performed. Browser automation and axe cannot establish those outcomes.
- Verify the repository link and Markdown resource presentation in the eventual Pages environment; the remote repository URL was verified through the GitHub connector, not browser navigation.
- Review the visual design and wording. Mission 002 intentionally remains “in progress” pending review. Do not merge or publish until approved.
