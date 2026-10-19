# T1 usability audit — Kai's own calculator

**Date:** 2026-10-19
**Method:** static inspection of the shipped HTML interface plus automated model tests. Not a timed participant study, browser interaction, or external competitor test.

## Observed interface constraints (corrected)
- The form asks for materials **per item**, packaging **per item**, and making time **per item**. There is no input for attempted batch quantity, saleable quantity, rejected count, or setup minutes.
- **Correction:** Although the static HTML marks making time with `step="1"`, the running JavaScript sets all numeric fields to `step="any"`. Fractional making time is accepted; the existing browser test checks `1.5` minutes is valid. The earlier statement that this was blocked by the interface was incorrect.
- The model tests prove the arithmetic with operator-prepared fractional inputs, **not** that users can derive those allocations easily.

## T1 workaround
To obtain the benchmark through the form, a user would need to convert 24 attempts and 2 rejects to 22 saleable units, distribute material costs across those units, include setup time in labour, and enter the resulting fractional minutes. The interface accepts fractional minutes, but does not calculate the allocation. This is an inferred manual-work friction finding for **our own tool**, not an observed participant difficulty, independent of competitor claims.

## Implications
A useful next iteration may be a separate batch-cost helper with attempted count, rejects, setup minutes, and saleable-unit outputs, rather than claiming an invented advantage over existing free tools. But do not implement it as a commercial product until actual maker workflows and competing tools have been tested. The current calculator remains a simple per-item estimator.

## Next verification
The existing optional Playwright browser test confirms fractional minutes are accepted. Next observe a consenting maker attempt T1 without coaching. Document their steps and confusion separately from our inferred friction.
