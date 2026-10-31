# KI-02 — Verified local development comparison (2026-10-26)

## Result
A local Python execution of the baseline and candidate decision logic on the six development examples returned:

- Naive baseline: **4/6 correct (66.7%)**.
- Candidate v0: **6/6 correct (100%)**.
- Absolute difference: **+2 correct / +33.3 percentage points**.

The comparison was performed by reconstructing the two functions and the six cases from the repository text in a local Python script because direct network access to GitHub was unavailable in the execution container. This verifies the six-case decision logic, **not** the full repository test suite, integration tests, GitHub Actions, or independent generalisation.

### Per-case predictions
| ID | Baseline | Candidate | Expected |
|---|---|---|---|
| dev-01 | accept | accept | accept |
| dev-02 | reject | reject | reject |
| dev-03 | abstain | abstain | abstain |
| dev-04 | abstain | abstain | abstain |
| dev-05 | abstain | reject | reject |
| dev-06 | accept | abstain | abstain |

The candidate was designed after examining development examples. Therefore these are **training/development-set results** susceptible to overfitting. No model was trained and no autonomous improvement loop was demonstrated. Public holdout labels are visible in the repository and do not constitute a genuinely blind independent evaluation.

## Follow-up
- Obtain passing full repository CI run, particularly SCOUT integration and adversarial tests.
- Freeze candidate before independent evaluator generates and adjudicates unseen problems.
- Compare against identical cases and budgets; report accuracy, abstention and errors, not just a headline score.
