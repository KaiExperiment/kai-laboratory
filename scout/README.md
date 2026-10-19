# Open KI — KI-01: SCOUT

An operational, supervised **offline opportunity-research workbench**, Python 3.10+, standard library only. It ingests attributed local evidence, matches operator-authored opportunity rules, audits claims, ranks investigations, challenges leading candidates and writes reproducible JSON/Markdown. No paid API, inference service, account or network is needed.

SCOUT does not browse or autonomously invent hypotheses. Kai/Obe (or another operator) supply the question, source snapshots, rules, claims and initial assessments. The software performs the repeatable bookkeeping and checks. This is the first tool in Open KI, not a fictional team of independent agents. No website files or hosting configuration are changed.

## Run now

From the repository root:

```sh
python3 -m scout --help
python3 -m unittest discover -s scout/tests -v
python3 -m scout run --input scout/examples/dossier.json --output work/scout-demo --timestamp 2026-10-19T16:29:00Z
python3 -m scout verify scout/results/demo-001 work/scout-demo
```

Use a **new output directory** each time; existing directories are refused, including empty ones. Omit `--timestamp` for the current UTC time. The committed demo uses a pinned logical timestamp for exact reproduction, not a claim about the precise wall-clock start. Recorded runtime: Python 3.12.14. This run takes less than a second on the development environment.

Read `work/scout-demo/report.md` and `research.json`. The committed [report](results/demo-001/report.md) uses **entirely synthetic fixtures**: no real sources, customers, sales, interviews or scientific experiments are claimed. The scenario's CSV comparison gets 67.5/100 and `fixture_shortlist`; the unsupported research service and contradictory sensor proposal both get `abstain`. A source-removal audit weakens the leader under either removal. These are software outcomes, not findings of commercial or scientific promise.

## Use your own research

1. Copy `scout/examples/` into a new working directory, e.g. `work/my-question/`. Edit its `dossier.json` question and opportunity rules.
2. Place UTF-8 source snapshots beneath that directory's `evidence/`. For genuine material, supply the real author/publisher, URL or archival identifier, access date with timezone, independence group, quality assessment and rationale; set `fixture` to false only when appropriate. Do not change synthetic notes to look genuine. A locator is recorded, never fetched or authenticated.
3. For each opportunity, provide a category (`product`, `invention`, `service`, `experiment`), case-insensitive substring triggers and a hypothesis. Each rule is evaluated; a rule matching no available source is retained as an abstention. Generic/negated trigger mentions can match: inspect the passages.
4. Annotate claims as `observation`, `inference` or `speculation`, mark decision-critical claims, and attach source IDs, **exact nonempty quotes** and `supports`/`contradicts` stances. Read all sources for counterevidence before running. Include costs in time and cash, risks, uncertainties, falsification tests and a bounded next action with `local` or `consequential` scope.
5. Supply 0–4 assessments with rationales and claim IDs; run the CLI against the new dossier. Review semantic relevance, source quality, omitted alternatives and every flag before selecting anything.

The executable fixture is the complete input schema example. Paths must be relative and resolve inside the dossier's `evidence/` directory (symlink/path escapes are refused). Bad metadata, duplicate IDs and invalid scores fail before output creation. Missing/unreadable/empty sources and bad citations are recorded as missing/invalid evidence, rather than fabricated or silently ignored. A filesystem failure after output creation may leave partial files; retain them for diagnosis and choose a fresh directory. Keep sensitive or unlicensed material out of any branch you publish.

## Scoring and challenge

All scores are investigation priorities, **not calibrated confidence or probability of success**. Higher means better. Proposed dimension ratings are operator judgments; exact citation checks do not verify that the cited passage entails the rating. An assessment with no claim IDs, unknown claims or non-traceable claims gets effective score zero.

| Dimension | Weight | Rating anchors (0 → 4) |
| --- | --- | --- |
| Feasibility | 25 | infeasible/unknown → major gaps → plausible with gaps → small accessible prototype → directly demonstrated implementation |
| Novelty | 10 | unknown/duplicate → likely alternatives → differentiated hypothesis → documented gap after scoped search → strong corroborated gap; never proof of novelty |
| Cost | 20 | unknown/unaffordable → substantial unapproved resources → bounded resources → low cash/time → existing resources and bounded local first step |
| Risk | 15 | unknown/uncontrolled → major unresolved harms → mitigations proposed → bounded low-impact step → well-characterised minimal exposure |
| Evidence | 30 | computed from traceability, independence and declared source quality |

Weighted total = `sum(weight * effective_rating / 4)` out of 100. Evidence starts at 0 with no traceable claims; 1 with fewer than two independent/nonduplicate supporting sources; 3 with two such sources; 4 additionally requires at least three traceable claims. This is capped by the **lowest declared quality** of supporting sources. Source quality anchors: 0 unusable/unknown, 1 weak unverified assertions, 2 limited material with explicit limitations, 3 strong relevant primary material, 4 independently corroborated strong evidence. Fixtures have quality 2 **within their synthetic scenario only**; their real-world evidence value is zero. Independence is conservatively limited by distinct content hashes and declared independence groups. It is not independently established.

A shortlist requires a trigger match, at least two independent/nonduplicate supporting sources, a declared critical claim, all critical claims traceable without invalid references, no annotated contradiction, and total ≥60. Any failed gate causes **abstention regardless of rank**. Every speculation is flagged as unsupported, even with a quote; a critical speculation blocks selection. Contradictions take precedence over supporting quotes. Ties sort by stable opportunity ID. Fixture-dependent shortlists are labelled `fixture_shortlist`.

The deterministic challenge pass examines all claims for unsupported assertions, bad references and contradictions, zeroes unsupported assessments, and tries removing each supporting source from each provisional leader. It recomputes the decision and score under each removal. Falsification tests are operator-supplied proposals and are **not executed**. This pass is not an independent intellectual reviewer and cannot find arbitrary semantic contradictions, hidden confounders or missing sources. Treat brittle shortlists as requests for corroboration.

## Kai review and Obe approval

Each run freezes `queue.json`, initially pending for shortlisted candidates and blocked for abstentions. Record review into new files outside the frozen run:

```sh
python3 -m scout review --run work/scout-demo --queue work/scout-demo/queue.json --output work/kai-selection.json --candidate csv-comparison --actor Kai --decision select --note 'Example only: select a local fixture comparison for review.'
python3 -m scout review --run work/scout-demo --queue work/kai-selection.json --output work/obe-review.json --candidate csv-comparison --actor Obe --decision approve --note 'Example only: approve the described local fixture test, no external action.'
```

These are example commands, **not recorded approvals from Kai or Obe**. No actual selection or approval was made during development. Kai can `select` or `reject`; Obe can `approve` or `reject` after selection. Actor and note are mandatory. A decision cannot be overwritten; revise the dossier and create a new run for reconsideration. Queue history is replayed against its verified run to reject accidental edits or cross-run substitution. It is local attestation, not authentication or tamperproof storage; someone able to edit all files can forge it.

**Every consequential action requires Obe's separate explicit authorisation.** Labelling an action `local` does not authorise outreach, posting, purchases, account creation or other external actions. The CLI executes none of these, even after approval. Fixture evidence cannot approve a consequential action. A future executor must authenticate Obe, check the exact action scope and resource limits, and fail closed; a queue flag alone is insufficient permission.

## Artifacts and verification

- `inputs/dossier.json` plus `inputs/evidence/`: frozen inputs, retaining raw dossier hash and source hashes.
- `research.json`: question, pinned/current timestamp, run ID, software hashes, source register/full text, claims, effective scores, challenge, recommendations and limitations.
- `report.md`: readable research, source IDs/locators/quote line numbers, challenge and next actions.
- `queue.json`: initial review state, separate from research conclusions.
- `manifest.json`: SHA-256 hashes of the frozen bundle. Review commands create new files.

`verify` checks the manifest, reanalyses the frozen inputs using the recorded timestamp and current code, compares all research fields (including software hashes), and rerenders Markdown. With two directories it compares their research exactly. Both runs must use identical raw dossier bytes, sources, code and timestamp. This is integrity/reproducibility checking, not factual validation or cryptographic authorship. No execution of supplied source text occurs.

See [architecture](ARCHITECTURE.md), [proposed evaluation](EVALUATION.md), and [Mission 005 record](MISSION-005.md) for limitations and actual verification results.
