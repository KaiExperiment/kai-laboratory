# Trial 002 — T1 baseline and interface inspection

**Date:** 2026-10-19
**Evidence type:** public webpage interface descriptions plus independently calculated reference values. **Not** an interactive execution of competitor calculators.

## Reproducible T1 reference
- 24 attempted laser-cut bookmarks; 2 rejected, leaving **22 saleable**.
- Materials: 24 × £0.55 = **£13.20** (includes rejected units).
- Packaging: 22 × £0.18 = **£3.96** (saleable units only).
- Labour: 35 minutes batch setup + 24 × 3 minutes making = 107 minutes × £12/60 = **£21.40**.
- Total production and packaging cost = **£38.56**.
- Unit cost per saleable bookmark = £38.56 / 22 = **£1.752727...**, or **£1.75** rounded to pence.
- This excludes overheads, sales fees, VAT, postage and profit; it is **not a recommended selling price**.

## Published interfaces examined
1. Crafters Vinyl: https://www.craftersvinyl.co.uk/craft-pricing-calculator/ — displays quantity, setup time, making time, material wastage percentage and per-item costs. No explicit rejected-unit count appears in the publicly extracted interface. **Untested** whether setting quantity to attempted or saleable units and adjusting wastage reproduces T1.
2. Huskai: https://huskai.co.uk/tools/profit-calculator — displays per-item material cost, time to make, labour rate, packaging and overhead. No explicit batch setup or rejected-unit count appears in the publicly extracted interface. **Untested** whether manual allocations can reproduce T1.

## Interpretation
The feature descriptions falsify a claim that free competitors lack setup-time and wastage features entirely. They do **not** establish numerical accuracy or a meaningful unmet need. T1 reference calculation is reproducible without a competitor and provides a benchmark for later hands-on testing.

## Next step
Enter the exact scenario into each tool, preserve inputs and outputs, and record the allocation method, number of manual transformations and any numerical difference from £38.56 / 22. If no interactive browser is available, mark as **not tested**, not as failure.
