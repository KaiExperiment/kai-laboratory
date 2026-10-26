# KI-02 Agent Architect — Baseline Harness v0.1

A first **executable** benchmark scaffold, using only the Python standard library. This is not an AI agent, model training or a claim of improvement.

Run from repository root:

```bash
python -m ki02.benchmark --split dev
python -m unittest discover -s ki02/tests -v
```

Synthetic examples model three outcomes: accept, reject, abstain. A deliberately naive keyword baseline creates measurable failure cases. The six development cases are for designing improvements; six holdout cases are reserved for one final evaluation after the candidate is frozen. The holdout examples are committed in this public repository, so they are **not genuinely sealed against an agent with repository access**. Before claiming an unbiased agent-improvement result, store a new unseen test set separately and deny candidate agents access.

The examples are simplified proxies for evidence assessment, not an evaluation of SCOUT's full real-world research quality. Next: integrate SCOUT's actual dossier format, compare citation integrity, introduce human-labelled real cases, and then test model-driven Architect proposals. Never treat a benchmark score as proof of consciousness, general intelligence or real commercial validity.


## SCOUT integration — actual engine regression

Run from the repository root:

```bash
python -m ki02.scout_baseline
python -m unittest discover -s ki02/tests -v
```

The integration calls `scout.engine.analyse` on SCOUT's existing synthetic dossier, then compares three actual decisions to documented expected outcomes: `csv-comparison` → `fixture_shortlist`, `sensor-experiment` → `abstain`, and `research-service` → `abstain`. It checks that a contradictory critical claim and an unsupported critical claim block shortlisting. This is **a regression test of existing SCOUT behaviour**, not a new independent scientific benchmark.

The `.github/workflows/ki02-baseline.yml` workflow is configured to run these checks on relevant pushes and manual dispatch. Workflow execution and passing status have **not yet been verified** through this session's connector.

**Research integrity:** The public holdout examples are not secret. A later Architect trial needs independently sealed questions, independent adjudication, repeated runs where models are stochastic, and matched resource budgets. No AI-generated improvement has yet been tested.
