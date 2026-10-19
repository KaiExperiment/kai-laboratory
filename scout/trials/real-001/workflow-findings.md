# Maker workflow test findings and next research decision
Date: 2026-10-19
Status: Automated synthetic tests verified by GitHub Actions run 39311954956. External competitors **not yet tested**.

## What was verified
The shipped Maker Profit Calculator model passed six reproducible synthetic tests:
- W01: one-off bookmark with postage income/cost explicitly mapped
- W02: 20-item batch, 18 saleable units, manual allocation of setup time and wastage
- W03: marketplace scenario using *synthetic editable fee rates*, not asserted current Etsy fees
- W04: wholesale/direct calculations entered separately
- W05: pre-tax £25 calculation, without VAT status or tax calculation
- W06: manually varied material prices and resulting profit sensitivity

These are correctness checks for mapped arithmetic, **not** evidence of external usability, automatic workflow support, unmet need, or willingness to pay.

## Confirmed product boundaries from code inspection
1. **Batch production**: no native quantity, setup-time or wastage inputs. W02 passes only after a person computes per-saleable-item inputs manually.
2. **Comparisons**: no saved scenarios, side-by-side channel comparison or material-price change history. W04/W06 require manual re-entry.
3. **Fee bases**: both percentage fees apply to the full entered price. Actual marketplace fee bases and taxes may differ.
4. **VAT**: no VAT status question or VAT-on-sales model. The tool explicitly excludes VAT on sales and income tax.
5. **Demand**: none of these observations shows that users experience costly friction, or that they would pay to remove it.

## KI-01 research priority
**First:** investigate the batch setup + scrap/wastage workflow, because it is a specific reproducible manual step for small-batch laser and craft makers, and it can be tested without guessing tax or platform rules.

**Second:** investigate saved side-by-side price/channel comparisons, only if maker feedback identifies a meaningful repeated problem.

**Defer:** another generic Etsy fee calculator, and any tax-advice features without authoritative domain review.

## Next evidence gates
1. **Competitor capability check**: manually test W02 with the documented free alternatives where available; record actual input support, limitations, and calculation outputs. A marketing description is not a tested capability.
2. **Workflow evidence**: seek consent-based, attributable reports from real makers about frequency, time cost and mistakes in allocating setup/wastage. Do not treat a convenient hypothetical scenario as a user interview.
3. **Commercial signal**: test whether anyone chooses to pay for a demonstrated improvement, separately from free-use interest. No market-validation claim until this occurs.

**Decision:** continue research; no new product build and no demand or revenue claim. This document records a decision, not completed competitor testing.
