# KI-02 — Evaluation gate and next experiment

## What is implemented
- `benchmark.py`: deliberately naive keyword baseline and scoring.
- `candidate_v0.py`: AI-authored heuristic tuned on six development examples.
- `scout_baseline.py`: deterministic regression against actual SCOUT engine fixture.
- `challenge_pack.py`: reproducible synthetic template-case generator.
- `evaluate.py`: compare frozen baseline and candidate on the same evaluator-supplied cases, report accuracies, abstentions, delta, and SHA-256 digests.
- `tests/`: regression, integration, adversarial and evaluator tests.
- GitHub Actions workflow: configured for push and pull requests, **not yet confirmed running successfully**.

## Verified narrow result
A local execution of the baseline and candidate decision logic against six development cases returned **4/6 vs 6/6**, respectively. This is a development-set improvement, not an independently held-out result.

## Evaluation protocol
1. Freeze source versions and commit SHAs. No edits to the candidate after evaluating the independent set.
2. Have an evaluator prepare new independently written cases with unambiguous, justified expected labels. Synthetic template cases alone are insufficient.
3. Keep the cases private to the evaluator until predictions are frozen. Do not commit them to public GitHub.
4. Run `python -m ki02.evaluate --cases /private/cases.json --output /private/results.json`. The report deliberately omits raw evidence text and per-case predictions, but a digest does not itself guarantee secrecy.
5. Record counts, accuracy, abstentions, per-class failures and whether the delta persists across independent case sets.
6. If the candidate underperforms or merely memorises cues, record the failure. Do not selectively publish only positive runs.
7. Independently execute the full unit and integration test suite; GitHub Actions currently has no verified pass in this session.

## Scientific scope
No LLM or local open-weight model has been connected to this evaluation yet. Neither SCOUT nor KI-02 is an autonomous AI Architect. We have built a testable engineering scaffold, not demonstrated autonomous AI self-improvement.

## Security and user approvals
No credentials, customer records or private conversations should be committed to the public repo. No spending, external outreach, or consequential action without explicit human approval.
