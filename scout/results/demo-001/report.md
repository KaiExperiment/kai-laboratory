# KI-01: SCOUT research report

Timestamp (UTC): 2026-10-19T16:29:00+00:00
Run: `450bcca8e97b5a79aba7ce4fa20b17e6f66757f0a837b8c9dd61d7b79761323e`

Question: Which zero-cash investigation should Kai consider next? (Synthetic fixture demonstration)

**OFFLINE RUN. Fixture-labelled material is synthetic example evidence, not real research.**

Scores rank investigation priorities, not probability of success. Shortlists remain provisional.

| Rank | Opportunity | Score / 100 | Decision |
| --- | --- | --- | --- |
| 1 | csv-comparison: Offline pricing assumption comparison | 67.5 | fixture_shortlist |
| 2 | research-service: Opportunity research service | 0 | abstain |
| 3 | sensor-experiment: Calibrated sensor experiment | 0 | abstain |

## csv-comparison: Offline pricing assumption comparison

Category: product; fixture: True.
Hypothesis (operator supplied): A local CSV comparison might help makers review inconsistent pricing assumptions.
Matched source IDs: workflow

### Claims and provenance

- need [observation; traceable; critical=True]: The fictional scenario describes comparing saved assumptions.
  - workflow (supports, quote verified=True, line=3): "Scenario A: a maker needs to compare saved pricing assumptions across products."
- implementation [inference; traceable; critical=True]: CSV export is plausible with a standard-library implementation.
  - workflow (supports, quote verified=True, line=4): "A local CSV export can be implemented using Python's standard library."
- offline [observation; traceable; critical=True]: The proposed comparison can use existing local files.
  - review (supports, quote verified=True, line=3): "The proposed comparison can run offline with files already on the user's computer."
- demand [speculation; unsupported; critical=False]: Real makers might value this workflow.

### Evaluation

Effective scores (0–4): {"cost": 4, "evidence": 2, "feasibility": 3, "novelty": 1, "risk": 3}.
- cost: proposed 4; Proposed first step uses existing local files and standard-library software; labour remains a cost.; claim IDs: ['implementation', 'offline']
- feasibility: proposed 3; Small local prototype seems feasible; implementation time remains unmeasured.; claim IDs: ['implementation', 'offline']
- novelty: proposed 1; Existing alternatives are plausible; no novelty search has occurred.; claim IDs: ['implementation', 'offline']
- risk: proposed 3; Local testing limits exposure; usefulness and incorrect interpretation remain risks.; claim IDs: ['implementation', 'offline']

### Challenge/review

provisional; semantic review still required
- flags: demand: unsupported speculation
- flags: Source-removal challenge: shortlist depends on individual sources; seek corroboration
- falsification_tests: Compare with a spreadsheet baseline; reject if the prototype adds no useful insight.
- Remove source review: score 7.5, abstain; ['Fewer than two independent, nonduplicate supporting sources', 'Critical claim unsupported or contradicted', 'Invalid reference on a critical claim', 'Weighted score below 60/100']
- Remove source workflow: score 7.5, abstain; ['No source matches the opportunity rule', 'Fewer than two independent, nonduplicate supporting sources', 'Critical claim unsupported or contradicted', 'Invalid reference on a critical claim', 'Weighted score below 60/100']
- Risk: Fixture assumptions may not generalise to real users.
- Uncertainty: Demand, novelty and effort have not been measured.

Proposed next action (local): Create a tiny CSV fixture and compare manual spreadsheet review with a local comparison script. No customer data or outreach.
Kai selection is pending; Obe approval is separate. No action has been executed.

## research-service: Opportunity research service

Category: service; fixture: True.
Hypothesis (operator supplied): A paid research service might find customers.
Matched source IDs: workflow

### Claims and provenance

- buyers [speculation; unsupported; critical=True]: Customers will pay for reports.

### Evaluation

Effective scores (0–4): {"cost": 0, "evidence": 0, "feasibility": 0, "novelty": 0, "risk": 0}.
- cost: proposed 4; Proposed first step uses existing local files and standard-library software; labour remains a cost.; claim IDs: ['buyers']
- feasibility: proposed 3; Small local prototype seems feasible; implementation time remains unmeasured.; claim IDs: ['buyers']
- novelty: proposed 1; Existing alternatives are plausible; no novelty search has occurred.; claim IDs: ['buyers']
- risk: proposed 3; Local testing limits exposure; usefulness and incorrect interpretation remain risks.; claim IDs: ['buyers']

### Challenge/review

weakened/abstain
- flags: buyers: unsupported speculation
- flags: feasibility: unsupported assessment; effective score 0
- flags: novelty: unsupported assessment; effective score 0
- flags: cost: unsupported assessment; effective score 0
- flags: risk: unsupported assessment; effective score 0
- blockers: Fewer than two independent, nonduplicate supporting sources
- blockers: Critical claim unsupported or contradicted
- blockers: Weighted score below 60/100
- falsification_tests: Compare with a spreadsheet baseline; reject if the prototype adds no useful insight.
- Risk: Fixture assumptions may not generalise to real users.
- Uncertainty: Demand, novelty and effort have not been measured.

Proposed next action (consequential): Proposed customer outreach; requires genuine demand evidence, Kai selection and explicit Obe authorisation.
Kai selection is blocked by abstention. No action has been executed.

## sensor-experiment: Calibrated sensor experiment

Category: experiment; fixture: True.
Hypothesis (operator supplied): A sensor experiment might be feasible with available calibrated equipment.
Matched source IDs: review, sensor

### Claims and provenance

- equipment [observation; contradicted; critical=True]: Calibrated equipment is available.
  - sensor (supports, quote verified=True, line=3): "The planning author assumes calibrated equipment is available."
  - review (contradicts, quote verified=True, line=5): "For the hypothetical sensor experiment, the required calibrated equipment is unavailable."

### Evaluation

Effective scores (0–4): {"cost": 0, "evidence": 0, "feasibility": 0, "novelty": 0, "risk": 0}.
- cost: proposed 4; Proposed first step uses existing local files and standard-library software; labour remains a cost.; claim IDs: ['equipment']
- feasibility: proposed 3; Small local prototype seems feasible; implementation time remains unmeasured.; claim IDs: ['equipment']
- novelty: proposed 1; Existing alternatives are plausible; no novelty search has occurred.; claim IDs: ['equipment']
- risk: proposed 3; Local testing limits exposure; usefulness and incorrect interpretation remain risks.; claim IDs: ['equipment']

### Challenge/review

weakened/abstain
- flags: equipment: contradicted observation
- flags: feasibility: unsupported assessment; effective score 0
- flags: novelty: unsupported assessment; effective score 0
- flags: cost: unsupported assessment; effective score 0
- flags: risk: unsupported assessment; effective score 0
- blockers: Fewer than two independent, nonduplicate supporting sources
- blockers: Critical claim unsupported or contradicted
- blockers: Unresolved contradictory evidence
- blockers: Weighted score below 60/100
- falsification_tests: Compare with a spreadsheet baseline; reject if the prototype adds no useful insight.
- Risk: Fixture assumptions may not generalise to real users.
- Uncertainty: Demand, novelty and effort have not been measured.

Proposed next action (consequential): Obtain equipment and perform a physical experiment only after a separate safety plan and Obe approval.
Kai selection is blocked by abstention. No action has been executed.

## Source register

- **workflow**: Synthetic workflow note; publisher: Mission 005 fixture author; independence group: fictional-perspective-workflow;
  locator: fixture:workflow; snapshot: `evidence/workflow.txt`; accessed: 2026-10-19T16:00:00+00:00;
  fixture=True; status=ok; quality=2/4 (Synthetic scenario material: traceable for software testing only, no real-world evidential value.); SHA-256: `6e228f0d28dfb42dee69f42ded62c3e69499a2d66d7f661acf15334e3c689ed4`.
- **review**: Synthetic review note; publisher: Mission 005 fixture author; independence group: fictional-perspective-review;
  locator: fixture:review; snapshot: `evidence/review.txt`; accessed: 2026-10-19T16:00:00+00:00;
  fixture=True; status=ok; quality=2/4 (Synthetic scenario material: traceable for software testing only, no real-world evidential value.); SHA-256: `ff3fedf4efd766c753f50f5202dac8a987dec3ae8edf2a8c7d83288c878fe6eb`.
- **sensor**: Synthetic sensor note; publisher: Mission 005 fixture author; independence group: fictional-perspective-sensor;
  locator: fixture:sensor; snapshot: `evidence/sensor.txt`; accessed: 2026-10-19T16:00:00+00:00;
  fixture=True; status=ok; quality=2/4 (Synthetic scenario material: traceable for software testing only, no real-world evidential value.); SHA-256: `1fb5f2f70f4ed805a4f5c938dbb62f07379dfaec581d98b36683e561ca653184`.

## Limitations

- Offline ingestion only: no web search, live research, language model or external actions.
- Opportunity rules, claims and assessments are supplied by the operator; matching is lexical.
- Exact quotes prove traceability, not truth, relevance or logical entailment.
- Contradictions require operator annotations; unannotated semantic conflicts may be missed.
- Source independence and fixture labels are operator declarations, not independently verified.
- Novelty scores do not establish market novelty, patentability, demand or scientific discovery.
- Review identities are local attestations, not authenticated access control.

## Reproduce

Use the dossier and source snapshots in inputs/ with the same SCOUT version.
```sh
python3 -m scout run --input PATH_TO_RUN/inputs/dossier.json --output work/scout-reproduced --timestamp 2026-10-19T16:29:00+00:00
python3 -m scout verify PATH_TO_RUN work/scout-reproduced
```
