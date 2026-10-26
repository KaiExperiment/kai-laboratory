# KI-02 Agent Architect — Baseline Harness v0.1

A first **executable** benchmark scaffold, using only the Python standard library. This is not an AI agent, model training or a claim of improvement.

Run from repository root:

```bash
python -m ki02.benchmark --split dev
python -m unittest discover -s ki02/tests -v
```

Synthetic examples model three outcomes: accept, reject, abstain. A deliberately naive keyword baseline creates measurable failure cases. The six development cases are for designing improvements; six holdout cases are reserved for one final evaluation after the candidate is frozen. The holdout examples are committed in this public repository, so they are **not genuinely sealed against an agent with repository access**. Before claiming an unbiased agent-improvement result, store a new unseen test set separately and deny candidate agents access.

The examples are simplified proxies for evidence assessment, not an evaluation of SCOUT's full real-world research quality. Next: integrate SCOUT's actual dossier format, compare citation integrity, introduce human-labelled real cases, and then test model-driven Architect proposals. Never treat a benchmark score as proof of consciousness, general intelligence or real commercial validity.
