# PROMETHEUS — Ignition 001

A supervised, executable experimental-discovery prototype. Investigator, Skeptic and Experimenter are **deterministic software stages**, not independently running AI agents. The fixed hypotheses were authored with AI assistance during development. No inference, network, account, API key or third-party dependency is required.

Python **3.10+** is required; the recorded execution used Python 3.12.14. Run commands from the repository root, with a new or empty output directory:

```sh
python3 -m unittest discover -s prometheus/tests -v
python3 -m prometheus --output work/reproduced
python3 -m prometheus.verify prometheus/results/ignition-001 work/reproduced
```

The full protocol takes seconds to a few minutes on a typical laptop and generates roughly 0.4 MB of evidence. The verifier checks source hashes, protocol, proposals, every final tour and scientific result, excluding elapsed seconds and runtime host metadata. Use the recorded Python version for strongest reproducibility; Python's random implementation or floating-point behavior can vary across versions/platforms. Never overwrite the committed evidence. To rerun again, choose another empty output directory.

## Research design

[Protocol](protocol.json) fixes the city count, budgets, seed lists, annealing schedule, bootstrap seed, selection rule and validation criterion before execution. The main challenge is closed Euclidean travelling-salesperson search over 48 independent uniform unit-square points. Tour length includes the return edge.

All strategies use the same deterministic nearest-neighbor initialization and exactly 2,000 full objective evaluations, counting the initial tour and every proposal, even unchanged tours. All score calculations use the complete tour: no candidate gets a cheaper delta-scoring shortcut. Matrix construction and nearest-neighbor initialization are common preprocessing outside that budget. Wall-time measurements include initialization and search, exclude instance generation, and are descriptive, not an equal-CPU claim.

- **Baseline — greedy swaps:** swap two random cities; accept only strictly shorter tours.
- **2-opt:** reverse a random contiguous segment; accept only shorter tours.
- **Relocation:** remove a random city and insert at another position; accept only shorter tours.
- **Annealing:** segment reversal with geometric cooling and probabilistic acceptance of worsening moves; return the best observed tour.

The actual last evaluated annealing temperature is slightly above the configured final schedule endpoint because the initial score consumes one evaluation. Proposal null moves count toward the budget. Each method has its own seeded RNG; paired seed labels do not imply identical random draws once methods consume different numbers of draws.

20 exploration instances × 3 search seeds × 4 methods establish the baseline before candidate testing. Select the eligible candidate with highest exploration mean paired percentage reduction, requiring ≥1%; lexical strategy name breaks ties. Selection is saved before generating validation data. Only the frozen candidate and baseline run on 40 held-out instances × 3 seeds. Report the mean of within-instance mean paired percentage reductions. Validation success requires ≥1% mean reduction, a positive lower endpoint of a 95% percentile bootstrap interval (10,000 instance resamples), and zero failed runs. No candidate switching or tuning follows validation.

The protocol was internally fixed before execution, not externally preregistered. Public deterministic holdout seeds are for reproduction, not proof of blinding. Future investigations must use new confirmatory seeds.

## Code and artifacts

- `strategies.py`: instance generation, baseline, proposal operators and controlled search loop.
- `roles.py`: fixed falsifiable proposals, rule-based rejection and explicit methodological controls.
- `experiment.py`: Experimenter, baseline-first execution, selection, clustered bootstrap and report.
- `__main__.py`: command-line entry; `--help` documents options.
- `verify.py`: compare independent runs, excluding timing and host metadata.
- `tests/test_engine.py`: correctness, exact small-instance bounds, budget, leakage, selection, failure and negative-result tests.
- `results/ignition-001/`: full measured evidence and [research report](results/ignition-001/report.md).
- `index.html`: buildless public research page linked from headquarters, with measured results and an explicitly first-in-order example tour pair.

An alternative protocol can be supplied with `--protocol PATH` for exploratory research; it must use the same protocol schema and supported methods. Changing its parameters creates a different experiment and does not update the static public research page. The fixed acceptance/selection rules remain implemented in code; the prose rule fields describe those rules. Keep versioned bundles when changing a protocol and use a fresh holdout.

The run writes a manifest before measurements, then reviews, exploration, selection, validation, summary and Markdown report. A run-level exception may leave partial evidence: retain it for diagnosis and rerun into a fresh directory. Per-run search exceptions are recorded and exclude a candidate from a valid paired estimate. Raw rows retain full tours, verified scores, initial scores, seeds, accepted moves, exact score count and elapsed time. Bootstrap intervals on exploration are descriptive because of winner selection.

## Observed outcome and limitations

Greedy 2-opt was selected. Held-out mean reduction: **8.332%**; 95% instance-bootstrap interval **7.282%–9.493%**; instance SD **3.619%**; wins/ties/losses **40/0/0**; **zero failures across 480 runs**. The predefined validation criterion passed.

This is evidence of an established heuristic's advantage over a greedy-swap baseline under this protocol. It is not a new scientific discovery, evidence of autonomous AI research, proof of optimal solutions, or a comparison with state-of-the-art TSP solvers. Uniform synthetic instances, one size and budget, approximate uncertainty and unequal proposal overhead limit generalization. See the report for all exploratory outcomes, limitations and the next proposed experiment.

## Local website review

Serve the repository root using `python3 -m http.server 8000 --bind 127.0.0.1`, then visit `http://127.0.0.1:8000/prometheus/`. No build step is required. Optional development-only browser checks use the existing Playwright pattern:

```sh
CHROMIUM_PATH=/usr/bin/chromium node tests/prometheus.browser.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/headquarters.browser.cjs
node tests/maker-profit-calculator.test.cjs
```

Playwright/Chromium are optional QA tools, not prototype or website dependencies. Review notes and actual QA outcomes are in `QA.md`. No merge, deployment, publication workflow or live-site setting is part of this mission.
