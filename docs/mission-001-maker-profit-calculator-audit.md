# Mission 001 — Maker Profit Calculator Audit

Date: 18 October 2026. Baseline: `7de4307a103b57da245a6e2982fdadc04282c818`.
Scope: `maker-profit-calculator.html`. Changes are for review on a separate branch; no merge or live deployment is part of this mission.

## Findings and fixes

The original ordinary-case formulas were correct. Materials, packaging, other costs and overheads are per item; labour is minutes / 60 × hourly target; fees are selling price × combined percentage + fixed fee. Total includes labour and fees. Profit is revenue minus total; margin is profit / revenue, not markup. The revised calculator preserves this model.

| Finding | Evidence / consequence | Change |
| --- | --- | --- |
| Recommended prices rounded to nearest penny | With £1 cost and 10% fees, £1 / .9 displays £1.11 but loses £0.001. The 20% target £1 / .7 displays £1.43 (valid); with £1 cost and no fees, the old £1.25 target is exact. Other targets can round down: the default target previously displayed £17.88, below the needed £17.884160… | Round suggested selling prices upward to whole pennies; tolerate machine rounding noise at exact pennies. Default target now £17.89. Ordinary displayed totals still round normally. |
| Zero-cost boundary cases misclassified | At zero costs and 100% fees the original said break-even impossible, although £0 has zero profit. At zero costs and 80% fees a positive price has 20% margin, although the original said impossible | Zero-cost break-even is £0 at all rates. Minimum positive penny price for the margin target is £0.01 when fees ≤80%; above that no positive price attains 20%. |
| Unbounded finite inputs can overflow | A finite but enormous minutes/hourly value can overflow labour; tiny positive revenue can overflow the percentage margin | Bound money/time inputs to 1,000,000, each percentage to 100%, and nonzero inputs to at least 0.000001. Combined rates above 100% remain testable. Limits are explained. |
| Errors were generic and easy to miss | An empty price was described as a problem in a cost field; no field was marked | Individual messages linked with `aria-describedby`, `aria-invalid`, range checks, a summary, and cleared results/styles until valid. Zero remains valid. Fractional minutes/rates are explicitly supported with `step=any`. |
| iPhone focus zoom risk and narrow layout | Inherited input font was .9rem (normally 14.4px), below the common iOS 16px focus-zoom threshold; 210px grid minimum could overflow smaller containers | 16px input text, decimal input mode, ≥44px input/button height, shrinking grid minimum, single-column results below 350px, visible keyboard focus, darker hints. Pinch zoom remains enabled. |
| Assumptions insufficiently explained | Fixed fee applies per sale while product costs are per item; shipping and fee bases could be misunderstood | Explicit one item per sale assumption, delivery handling, additive percentage bases, fee tax, excluded taxes, full-precision calculation versus platform rounding, and no persistence. Added fees and non-labour cost subtotal for checking results. |

## Reproducible mathematics

Let `C` be materials + packaging + other + overheads + labour + fixed fee, and `r` the sum of percentage fees / 100.

- Profit = price × (1 − r) − C.
- Break-even = C / (1 − r) for positive C and r < 1.
- Price for 20% margin = C / (.8 − r) for positive C and r < .8.
- Suggested prices round upward to pennies; zero costs use the special cases above.
- Before-labour profit is revenue less non-labour costs and fees, calculated directly to avoid cancellation from adding back large labour values.

Default example: cost subtotal £7.20; labour £5.208333…; fees £2.57405; total £14.982383…; profit £10.007616…; margin 40.046485…%; before-labour profit £15.21595. Display: £5.21 labour, £2.57 fees, £14.98 total, £10.01 profit, 40.0% margin, £15.22 before labour, £13.94 break-even, £17.89 target. Displayed components can differ by a penny from displayed totals because only display is rounded.

## Tests and observed results

Run the dependency-free tests with Node 18 or newer:

```sh
node tests/maker-profit-calculator.test.cjs
```

Observed with Node v24.19.0: **10 tests passed, 0 failed**. The tests execute the pure model extracted from the shipped HTML, with independently calculated expected values. Coverage includes all cost components, direct sales, additive and fixed fees, fractional minutes, losses, £0 price, zero costs, 79.9/80/80.1/99.9/100/150/200% combined fees, empty/negative/nonfinite/extreme inputs, exact-penny and upward rounding, and large supported values. A deterministic 500-case sweep verifies each recommended price meets its goal and the previous penny does not (floating-point tolerance 1e-9 or tighter).

Optional browser suite (Playwright is a development-only requirement; nothing is loaded by the calculator):

```sh
CHROMIUM_PATH=/usr/bin/chromium node tests/maker-profit-calculator.browser.cjs
```

Observed with Playwright 1.62.1 and Chromium 154.0.8037.57: **six viewport scenarios passed**, at widths 320, 375, 390, 430, 768 and 1280px, height 844px. Checks cover no horizontal overflow, computed input font ≥16px and height ≥44px, default results, field validation and correction, reset, keyboard activation, loss/zero-price/impossible-fee states, fractional input validity, product text treated as text, no page errors and no external requests. JavaScript-disabled explanation also passed. A full-page 390px screenshot was visually inspected for layout and legibility.

`git diff --check` passed. No runtime libraries, network resources, accounts, subscriptions, analytics or storage were added. The page remains a single HTML file usable offline with JavaScript enabled.

## Limitations and remaining manual checks

- No physical iPhone or Safari/WebKit runtime was available. Chromium mobile viewport tests do **not** establish iOS Safari compatibility, on-screen decimal keyboard behavior, focus zoom behavior, browser chrome/safe areas or VoiceOver announcements. Verify those on a real iPhone before release. No screen reader or full accessibility conformance audit was performed.
- Browser checks inject the actual HTML using Playwright `setContent`: the managed browser blocked `file://` navigation. This verifies DOM/CSS/JS interactions, not hosting, HTTP headers or deployment. Chromium also needed execution outside the restricted process sandbox. No live website was touched.
- Shell Git fetch failed because its configured proxy was unreachable; GitHub connector operations are used for the review branch and PR.
- Fees are a linear estimate on one price, not a live marketplace integration. Marketplace per-component penny rounding, tiers, fee caps, multiple items, VAT accounting and different fee bases remain outside the model and are disclosed to users.
- Limits intentionally reject implausible inputs and sub-millionth values. Floating-point arithmetic is retained for estimates rather than introducing a decimal library. Suggested prices are tested with small tolerances; exceptionally close fee thresholds can yield very large prices.
- No Firefox, actual Safari, landscape device rotation, assistive technology, or live deployment testing was performed. No CI run is claimed; tests were run in this environment.
