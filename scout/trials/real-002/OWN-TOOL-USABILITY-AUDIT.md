# T1 usability audit — Kai's own calculator

**Date:** 2026-10-19
**Method:** static inspection of the shipped HTML interface plus automated model tests. Not a timed participant study, browser interaction, or external competitor test.

## Observed interface constraints
- The form asks for materials **per item**, packaging **per item**, and making time **per item**. There is no input for attempted batch quantity, saleable quantity, rejected count, or setup minutes.
- The making-time input has HTML `step="1"`; a fractional allocation such as 107/22 = 4.863636... minutes cannot be entered as a step-aligned number without a validation issue. The underlying compute function can accept a fraction, but the displayed form is more restrictive.
- Materials and packaging inputs have `step="0.01"`, and T1's £0.60 materials and £0.18 packaging happen to align with that precision. Labour allocation does not.
- The model tests prove the arithmetic with prepared fractional inputs, **not** that a user can enter the exact scenario without a workaround.

## T1 workaround
To obtain the benchmark through the form, a user would need to convert 24 attempts and 2 rejects to 22 saleable units, distribute material costs across those units, include setup time in labour, and deal with fractional minutes (or put the labour allocation into a monetary cost field, changing the breakdown). This is a genuine interface friction finding for **our own tool**, independent of competitor claims.

## Implications
A useful next iteration may be a separate batch-cost helper with attempted count, rejects, setup minutes, and saleable-unit outputs, rather than claiming an invented advantage over existing free tools. But do not implement it as a commercial product until actual maker workflows and competing tools have been tested. The current calculator remains a simple per-item estimator.

## Next verification
A browser-level validation test should confirm how the form handles non-integer making minutes; then observe a consenting maker attempt T1 without coaching. Document their steps and confusion separately from our inferred friction.
