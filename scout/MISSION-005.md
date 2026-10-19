# Mission 005 — Open KI: first agent

Implemented 19 October 2026 on `mission-005-scout`, based on main `a6e8a933ee45fe2093e2bf38d2e42936dab58165`. Branch location: https://github.com/KaiExperiment/kai-laboratory/tree/mission-005-scout . Prepared for review only; no merge or deployment.

## Delivered

A Python standard-library CLI with attributed snapshot ingestion, operator-supplied opportunity rules, exact-quote/line verification, observations/inferences/speculation, explicit costs/risks/uncertainties, evidence-quality-capped weighted scores, abstention gates, contradictory-evidence handling and source-removal challenges. Outputs include frozen JSON, Markdown, input snapshots, manifest hashes and a separate Kai/Obe review queue. The review command records local attestations only and executes no action.

See [README](README.md) for exact workflow/schema/rubric, [architecture](ARCHITECTURE.md), [evaluation proposal](EVALUATION.md) and the [readable demonstration](results/demo-001/report.md).

## Exact commands and observed results

From the repository root, using Python 3.12.14:

```sh
python3 -m unittest discover -s scout/tests -v
python3 -m scout run --input scout/examples/dossier.json --output scout/results/demo-001 --timestamp 2026-10-19T16:29:00Z
python3 -S -m scout run --input scout/examples/dossier.json --output work/scout-final-reproduced --timestamp 2026-10-19T16:29:00Z
python3 -m scout verify scout/results/demo-001 work/scout-final-reproduced
python3 -m unittest discover -s prometheus/tests -v
node tests/maker-profit-calculator.test.cjs
git diff --check
```

The committed output directory already exists: future reruns must choose another fresh directory, e.g. `work/scout-demo`, as documented in the README. The timestamp is explicitly pinned for reproducibility.

- **19 SCOUT tests passed**, covering deterministic bytes and ties, missing/empty/unknown sources, fabricated quotes, unsupported claims and assessments, contradictory evidence, quality caps, deduplication, source-removal challenges, no lexical match, metadata/path validation, immutable outputs, artifact tampering, queue state replay, selection-before-approval, fixture consequential-action refusal, timezone requirements and nonzero CLI failure.
- Independent `python3 -S` run (site packages disabled): hashes, all research evidence, scores, decisions and Markdown reproduced exactly.
- **12 existing Prometheus engine tests passed.** Its temporary negative-result test output correctly abstained; committed scientific evidence was untouched.
- **10 existing calculator model tests passed**, including the 500-case sweep.
- `git diff --check` passed. All pre-existing tracked files remain byte-identical to the branch base; only new `scout/` files are added. No browser checks were rerun because website files did not change.

The fixture leader is **CSV pricing-assumption comparison**, **67.5/100**, explicitly `fixture_shortlist`. Both individual source removals cause abstention. Research-service demand is unsupported; sensor equipment availability is contradicted. Both alternatives abstain at 0/100. No finding about real demand, customers, sales or scientific feasibility follows from these synthetic notes. The saved initial queue contains no selection or approval; review transitions were exercised only inside temporary automated tests.

## Repository preservation and access

Initial checkout was clean on `work`. The GitHub connector confirmed current main matches the base SHA. Mission 004's separate branches were located and its human-experience document/PR #4 inspected; they were not merged, rebased, edited or deployed. This additive branch starts at main rather than inheriting an unapproved website redesign. No existing website, calculator, experiments, research records or Mission 004 work was modified. No workflow or hosting setting was added.

Shell `git fetch` failed because the configured proxy at port 8080 could not be reached. Remote branch preparation uses the connected GitHub tools instead. No live research fetch was attempted. There are no configured API secrets; the prototype needs none. Connector argument-schema errors occurred during branch/tool discovery; these were corrected without changing existing branches or files.

## Unresolved limits and next action

SCOUT's facts and reasoning remain as good as the supplied source pack and annotations. It cannot browse, generate new hypotheses independently, detect arbitrary semantic contradictions, verify source credibility, establish novelty or authenticate local Kai/Obe actor strings. Quote matching and hashes establish traceability and reproducibility only. Fixtures cannot justify real-world action. The source quality cap is a conservative heuristic and the scoring threshold is not empirically calibrated. Automatic tests do not establish usefulness on genuine research.

Next proposed action: Kai reviews the report and rubric; Obe separately decides whether to authorise any consequential evaluation steps. The proposed real-world comparison against a manual memo includes equal total human effort, genuine public evidence, citation audits, counterevidence coverage and blinded usefulness review. It has not been run. No outreach, posting, purchase, account creation, physical experiment, merge, deployment or other consequential action was executed by SCOUT.
