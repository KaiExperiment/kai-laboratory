# T1 — controlled input transformations for published calculator fields

**Date:** 2026-10-19
**Status:** arithmetic cross-check only; no competitor's interactive calculator was run.

Reference: 24 attempts, 2 rejects, 22 saleable, £38.56 total and £38.56 / 22 = £1.752727... each (see T1-BASELINE.md).

## Huskai-style per-saleable-item entry
If a calculator expects costs **per saleable item**, transform the batch inputs:
- Materials per saleable item: £13.20 / 22 = **£0.60**.
- Labour per saleable item: £21.40 / 22 = **£0.972727...**.
- Packaging per saleable item: **£0.18**.
- Sum = £1.752727... per saleable item.
- At £12/hour, equivalent labour time per saleable item is **107 / 22 = 4.863636... minutes**.
- The operator must account for 24 attempted units despite selling 22, allocate the 35-minute setup, and avoid rounding intermediate values too early. If an interface only accepts two-decimal cost values or integer minutes, results can vary. This is an **input recipe**, not a tested claim that Huskai accepts or calculates these values.

## Crafters-Vinyl-style batch entry
Potential interpretation A: 22 saleable units with manually allocated attempted material and labour costs, using the same per-saleable allocations above. Potential interpretation B: 24 attempted units with a 2/24 = **8.3333%** rejected-unit rate, but only if the tool's wastage mechanism correctly distinguishes saleable output from attempts and applies labour and packaging to the intended bases. **Neither interpretation has been validated against the tool.**

## Falsification checklist
- Does the interface accept fractional minutes and >2-decimal inputs?
- Can rejected units affect material **and** production labour, but not packaging for saleable units?
- Does batch setup cost divide by actual saleable quantity rather than attempts?
- Is the calculated output a unit cost, a sale price, or a profit figure?
- How many conversions or workarounds are needed before a maker gets the reference £1.752727...?

**Decision:** Published feature inspection alone cannot show that competitors fail. Manual allocation is mathematically possible; its practical friction remains unmeasured. No novelty or willingness-to-pay claim.
