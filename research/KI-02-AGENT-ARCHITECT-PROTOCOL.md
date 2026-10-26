# KI-02 — Agent Architect: Experiment Protocol
Status: proposed implementation; benchmark not yet run. 2026-10-26.

## Question
Can an AI-assisted architect improve a supervised agent's performance on unseen tasks through prompt, tool, or workflow changes, while holding model and resource budgets constant?

## Baseline
Use KI-01 SCOUT as an existing reproducible evidence-checking tool, **not** as an LLM agent. First inspect its tests, fixtures and limitations. Create an independent agent wrapper only if it adds meaningful model-driven decisions; label deterministic checks separately.

## Protocol
1. Construct a task corpus with training/development and sealed held-out test splits; include source contradictions, irrelevant passages, missing evidence, adversarial instructions embedded in sources, and abstention cases.
2. Record baseline exact citation validity, evidence-supported decisions (human adjudicated), abstention calibration, task success, elapsed time and token/API costs where applicable.
3. Let Architect propose bounded changes to instructions, tool sequence or agent orchestration using only development examples and failure summaries. No access to held-out inputs or expected answers.
4. Run candidate and baseline on identical held-out tasks with matched tools/model/budgets. Log paired results and regressions. Do not accept a change merely because the agent claims improvement.
5. Preserve versions, seeds where supported, model IDs, input hashes, and full results; publish only synthetic/public test data.

## Constraints
No local AI model installed yet. No inference or autonomous improvement claims until working code and evaluations exist. No real external messages, payments, private-file access or unsupervised repository changes. £0 software budget. Human approval for consequential actions.

## Next executable work
Inventory SCOUT test suite and CLI. Build a small synthetic task set and baseline harness; run it before introducing an Architect model. Then test a first architect-generated candidate.

## Why now
This advances Open KI and Kai Laboratory without prematurely requiring a local model. Kai Enterprises £100 validation and Mission 007 private memory remain parallel tracks.
