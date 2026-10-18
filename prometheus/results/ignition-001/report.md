# PROMETHEUS — Ignition 001

Observed computational evidence from deterministic supervised software stages. No live AI agents or new scientific discovery are claimed.

## Research question and protocol

Can a fixed structured search process identify a strategy that improves tour length over a reproducible greedy-swap baseline?

Closed Euclidean travelling-salesperson search is combinatorial, offline and nontrivial. Each instance has 48 independent uniform unit-square cities. Every run starts from the same deterministic nearest-neighbor tour (start city 0, city-index tie break), then uses exactly 2,000 full objective evaluations including the initial score. Distance matrix and nearest-neighbor initialization are identical preprocessing and excluded from the evaluation budget; recorded time includes initialization. Baseline: strictly improving random city swaps. Candidates: greedy segment reversal (2-opt), greedy single-city relocation, and geometric simulated annealing with segment reversals (temperature 0.02 to 0.0001, best-so-far output). Null and full-tour reversal proposals still consume an evaluation.

20 exploration and 40 disjoint held-out instance seeds, each with 3 search seeds. Mean paired percentage reduction is computed per run, then averaged within instance. Selection requires exploration mean ≥1%; maximum mean wins, lexical tie break. Held-out success requires mean ≥1%, positive lower 95% percentile bootstrap endpoint and zero paired failures. 10,000 resamples use instances as independent units. This is an internal protocol fixed before the first execution, not external preregistration. The seed lists are public for reproduction, not a blind third-party holdout.

## Exploration — all implemented candidates

| Candidate | Mean reduction | Instance SD | 95% bootstrap interval | W / T / L |
|---|---:|---:|---|---|
| two_opt | 9.700% | 4.633% | [7.664, 11.653]% | 20 / 0 / 0 |
| relocate | 2.978% | 2.165% | [2.062, 3.916]% | 18 / 0 / 2 |
| anneal | 8.632% | 4.236% | [6.856, 10.475]% | 20 / 0 / 0 |

Exploration intervals are descriptive; selecting a winner makes them unsuitable as confirmatory evidence.

## Held-out validation

Frozen candidate: **two_opt**. Mean reduction **8.332%**, instance SD 3.619%, 95% interval [7.282, 9.493]%. Instance wins / ties / losses: 40 / 0 / 0.

Predefined success criterion met: **True**. Failed runs: **0**.

Total recorded runs: 480; total measured elapsed search time: 4.816 seconds (hardware-dependent).

## Integrity, limitations and follow-up

Hypotheses were proposed with AI assistance during development and implemented as the fixed Investigator catalog. The Skeptic is a rule-based gate plus explicit methodological controls, not an autonomous critic. The Experimenter executes and independently rescores returned tours; JSON stores tours, seeds, budgets, metrics, timings and failures. No API calls, inference or network are used by the prototype.

The baseline is a legitimate local-search heuristic, not a state-of-the-art TSP solver. Improvements may be established algorithmic advantages, not discoveries. Only uniform synthetic instances of one size and one budget are tested. Search seeds are repeated within each instance, not independent new problem instances. Equal full evaluations do not imply equal CPU cost; no wall-clock superiority is claimed. No optimality gaps are known for the 48-city instances. Bootstrap uncertainty is approximate and distribution-dependent. Fixed parameters were not tuned on these results; only one candidate is validated. Public deterministic validation can be overfit by later development. Do not reuse these holdout seeds for future confirmatory claims.

Recommended next experiment: externally register fresh seeds spanning uniform and clustered distributions at 24, 48 and 96 cities, compare the selected method with deterministic best-improvement 2-opt, and measure both evaluation-limited and wall-time-limited performance. For small instances compute exact optima to report optimality gaps. Freeze all methods and analysis before that run.

## Reproduction and evidence

See `prometheus/README.md`. `manifest.json` records the full frozen protocol, source hashes and runtime. `reviews.json`, `exploration.json`, `selection.json`, `validation.json` and `summary.json` contain the complete observations and decision. Scientific outputs reproduce exactly on the recorded Python version; elapsed times and platform metadata are expected to differ.
