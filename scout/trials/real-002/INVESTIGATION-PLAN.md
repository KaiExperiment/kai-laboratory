# SCOUT real-world investigation 002 — batch costing gaps

**Opened:** 2026-10-19
**Status:** Protocol only; no competitor calculations or seller interviews have been conducted.
**Question:** Can a UK small-batch maker complete realistic costing tasks accurately and with less manual work using existing free tools, or is there a demonstrable unmet workflow?

## Hypotheses to attempt to falsify
- H1: Free calculators already handle batch setup, wastage and fee scenarios adequately; a new generic calculator adds no value.
- H2: A distinct workflow gap exists for small makers producing mixed-size batches with defective units and channel-specific costs.
- H3: Even if a gap exists, makers may not want to pay to solve it.

## Controlled tasks (do not imply competitors have been tested)
- T1: 24 laser-cut bookmarks; 2 rejected units; materials £0.55 per attempted unit; packaging £0.18 per saleable unit; 35 minutes batch setup; 3 minutes per attempted unit; labour £12/hour. Record whether tool allocates rejected-unit and setup costs automatically.
- T2: Compare 10 vs 50 decorations with £9 setup materials, 40 minutes setup labour, 5% material wastage; inspect whether tool handles fractional expected wastage or requires explicit rounding.
- T3: One item across direct and marketplace channels, with distinct processing fee bases, conditional ad charges and VAT treatment. **Do not use hypothetical fees as current Etsy policy**; verify primary source before numerical claims.
- T4: Ask maker to find break-even price for wholesale vs direct sale while preserving their stated labour rate.

## Measurement sheet (one row per tool and task)
Record: tool URL, tested_at UTC, input assumptions, output and screenshots or locally archived notes where allowed, exact numerical expected result with independently checked formula, discrepancy, steps, manual workarounds, completion status, and source limitations. Treat published features as leads, not test outcomes.

## Candidate tools (discovery leads, not endorsements)
- Kai Maker Profit Calculator (our own baseline)
- https://www.craftersvinyl.co.uk/craft-pricing-calculator/
- https://huskai.co.uk/tools/profit-calculator
- https://profithatch.co.uk/etsy-fee-calculator/
- https://www.specifek.co.uk/etsy-calculator/

## Seller feedback protocol
Recruit a few consenting UK makers through permitted, respectful channels. Ask what their actual costing workflow is, show a neutral task without leading them, note their current workaround and how much time it costs, and ask separately whether they have ever paid for such a solution. No invented interview results. Avoid collecting unnecessary personal data.

## Decision thresholds (precommitted)
- **Abstain:** no hands-on competitor comparisons, or no authentic user feedback.
- **Explore narrow prototype:** at least two independently observed task failures or costly workarounds plus corroborating maker feedback; label as provisional.
- **Commercial validation:** require evidence of genuine payment intent or transactions, not compliments, before claiming a viable paid product.
- If free tools perform the tasks adequately, explicitly reject generic calculator differentiation.

## Immediate next action
Perform a reproducible, manual competitor walkthrough, starting with T1; save observed outputs and verify calculations. If direct access is blocked, record it as untested rather than failure. Keep this trial separate from synthetic SCOUT fixture results.
