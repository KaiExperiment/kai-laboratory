# Mission 005 — maker workflow comparison protocol
Date: 2026-10-19
Status: **Plan only. No competitor tests or user interviews have yet been performed.**

## Purpose
Test whether the existing Maker Profit Calculator and public alternatives handle realistic UK handmade-maker workflows. A failed test may reveal a product gap, but **does not** establish unmet market demand or willingness to pay.

## Candidate tools
Use the alternatives and their original URLs recorded in [competitor-audit.md](competitor-audit.md). Verify each site's current availability, privacy terms, fee assumptions and scope at execution time. Do not enter personal or business-sensitive data. Log access failures rather than substituting a different tool without recording the change.

## Synthetic scenarios (fictional inputs; not customer evidence)

| ID | Workflow | Input assumptions | What to check |
| --- | --- | --- | --- |
| W01 | One-off personalised bookmark | Material £1.20, packaging £0.35, labour 12 min at £12/h, sale £8.50, postage charged £2.00, postage cost £1.80 | Separate costs from revenue; correctly handle labour and postage |
| W02 | Batch of 20 laser-cut decorations | Sheet material £12, paint £6, 90 min setup, 5 min per item, labour £12/h, 2 damaged items, 18 saleable items | Allocate batch setup and wastage across saleable units |
| W03 | Platform sale with optional advertising | Item £18, shipping paid by buyer £3, shipping cost £2.60, material £4.25, labour 20 min at £12/h | Distinguish platform transaction, payment processing, VAT-on-fees and optional ad costs; check current primary policy rather than hardcode rates |
| W04 | Wholesale versus direct | Unit material £3, packaging £0.50, labour 25 min at £12/h; wholesale £12, direct £21 | Compare channel economics without treating wholesale and direct fees as identical |
| W05 | VAT and tax uncertainty | £25 item with unspecified seller VAT registration and platform settings | Tool should ask for missing assumptions or flag uncertainty, not produce misleadingly precise tax advice |
| W06 | Repeat order after material-price increase | Material cost rises from £2.40 to £3.60, 10 items, same labour and sale price | Show sensitivity of margin and profit to material changes |

## Test procedure
1. Freeze date, URL, browser, locale, currency, tool version and scenario inputs. Confirm any displayed fee rates against the applicable official source on the same date.
2. Run each scenario in each tool where supported. Capture input mapping, output figures, warnings, screenshots if permitted, and whether the workflow was completed. Mark **not supported** separately from **wrong calculation** and **unavailable**.
3. Independently compute expected results from explicitly recorded assumptions. Do not compare tools against one another as a substitute for a reference calculation.
4. Rate each outcome **pass / incorrect / incomplete / unsupported / inaccessible / ambiguous** with reproducible notes. No arbitrary aggregate winner score.
5. Record whether the existing Kai calculator already solves the gap. Do not treat a duplicate feature as novelty.

## Decision gates
- **Technical gap:** At least one reproducible, consequential failure or missing workflow; verified with the same inputs and documented assumptions.
- **User pain:** Independent evidence from relevant sellers showing the gap matters in actual workflows. Fictional scenarios alone do not count.
- **Willingness to pay:** Separate credible behavioural evidence (e.g. voluntary paid pilot or attributable purchase commitment); compliments, views and general surveys do not prove it.
- **Commercial decision:** Abstain unless a differentiated solution, plausible acquisition path and all three gates have supporting evidence. No unsupported claim of validated demand.

## Results log template
| Date | Scenario | Tool/version | Source/fee policy checked | Outcome | Expected vs observed | Reproduction notes | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Not run | — | — | — | — | — | — | — |

## Ethics and limits
Only use synthetic data in external calculators. Do not bypass access controls, automate prohibited scraping, impersonate sellers or imply endorsement. Contact real sellers only through respectful, consent-compatible channels; no bulk unsolicited outreach. This protocol does not itself test market demand.
