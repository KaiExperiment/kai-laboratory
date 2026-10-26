# KI-02 — Development candidate v0

**Status:** Code and tests committed; execution results not yet verified.

An AI-authored, manually designed conservative keyword heuristic (`candidate_v0.py`) is compared against the naive keyword baseline on the six **development** examples. The candidate detects some missing-evidence and source-context phrases before looking for generic support/contradiction words.

The expected baseline development predictions are 3/6 correct (dev-01, dev-02, dev-03). Candidate predictions by code inspection are 6/6 correct. **These are anticipated outcomes, not a verified test run.** They are also vulnerable to overfitting, because the candidate was designed after inspecting the development cases. Improvement on development examples is not evidence of generalisation.

Do **not** evaluate the public `holdout` split to claim a valid blind test: its examples and labels were already visible to the developer and are committed publicly. Instead, generate an independent sealed corpus and have a separate evaluator control access. Next, verify CI execution, then integrate the more realistic SCOUT evidence schema and adjudicated semantic evidence.

The candidate is not an autonomous agent, is not trained, and makes no claims about general research accuracy.
