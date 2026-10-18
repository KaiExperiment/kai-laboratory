"""Reproducible experiment, selection and evidence reporting."""
import hashlib
import json
import platform
import random
import statistics
import time
from pathlib import Path
from .roles import investigator, skeptic
from .strategies import instance, length, solve

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_protocol(p):
    a, b = p['exploration_seeds'], p['validation_seeds']
    if set(a) & set(b) or len(set(a)) != len(a) or len(set(b)) != len(b):
        raise ValueError('Instance splits must be unique and disjoint')
    if min(len(a), len(b)) < 2 or p['cities'] < 3 or p['evaluations'] < 1:
        raise ValueError('Insufficient trials, cities or budget')
    if not p['search_seeds'] or len(set(p['search_seeds'])) != len(p['search_seeds']):
        raise ValueError('Search seeds must be nonempty and unique')
    if not 0 < p['anneal_final_temperature'] <= p['anneal_initial_temperature']:
        raise ValueError('Invalid annealing schedule')


def experimenter(p, seeds, strategies, split):
    rows = []
    # Establish every baseline run before evaluating candidates in this split.
    for strategy in strategies:
        for seed in seeds:
            distances = instance(seed, p['cities'])
            for search_seed in p['search_seeds']:
                row = dict(split=split, instance_seed=seed, search_seed=search_seed, strategy=strategy)
                start = time.perf_counter()
                try:
                    result = solve(distances, strategy, search_seed, p['evaluations'],
                                   p['anneal_initial_temperature'], p['anneal_final_temperature'])
                    if sorted(result['tour']) != list(range(p['cities'])):
                        raise ValueError('Invalid permutation')
                    if abs(length(result['tour'], distances) - result['length']) > 1e-10:
                        raise ValueError('Score verification failed')
                    row.update(result, status='ok')
                except Exception as exc:
                    row.update(status='failed', error=f'{type(exc).__name__}: {exc}')
                row['seconds'] = time.perf_counter() - start
                rows.append(row)
    return rows


def summarize(rows, candidate, p):
    seeds = sorted({r['instance_seed'] for r in rows})
    values = []
    for seed in seeds:
        pairs = []
        for run in p['search_seeds']:
            records = {r['strategy']: r for r in rows if r['instance_seed'] == seed and r['search_seed'] == run}
            if any(s not in records or records[s]['status'] != 'ok' for s in (p['baseline'], candidate)):
                return dict(candidate=candidate, eligible=False, reason='Failed or missing paired run')
            base, trial = records[p['baseline']]['length'], records[candidate]['length']
            pairs.append(100 * (base - trial) / base)
        values.append(statistics.mean(pairs))
    rng = random.Random(p['bootstrap_seed'])
    bootstrap = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(p['bootstrap_replicates']))
    return dict(candidate=candidate, eligible=True, instances=len(values),
                mean_percent_reduction=statistics.mean(values),
                stdev_percent_reduction=statistics.stdev(values),
                ci95=[bootstrap[int(.025 * len(bootstrap))], bootstrap[int(.975 * len(bootstrap))]],
                wins=sum(v > 1e-10 for v in values), ties=sum(abs(v) <= 1e-10 for v in values),
                losses=sum(v < -1e-10 for v in values), instance_reductions=values)


def select(summaries):
    eligible = [s for s in summaries if s['eligible'] and s['mean_percent_reduction'] >= 1]
    return min(eligible, key=lambda s: (-s['mean_percent_reduction'], s['candidate']))['candidate'] if eligible else None


def run(output, protocol_path=ROOT / 'protocol.json'):
    p = json.loads(protocol_path.read_text())
    validate_protocol(p)
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output directory must be empty; preserve existing evidence')
    output.mkdir(parents=True, exist_ok=True)
    source_hashes = {str(f.relative_to(ROOT)): digest(f) for f in sorted(ROOT.rglob('*.py'))}
    # Write protocol before any measurements; immutable within this run.
    manifest = dict(protocol=p, protocol_sha256=digest(protocol_path), source_sha256=source_hashes,
                    python=platform.python_version(), platform=platform.platform(),
                    role_implementation='Deterministic software stages, fixed development-time hypotheses')
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    reviews = [skeptic(h, p) for h in investigator()]
    (output / 'reviews.json').write_text(json.dumps(reviews, indent=2) + '\n')
    accepted = [r['proposal']['strategy'] for r in reviews if r['decision'] != 'reject']
    exploration = experimenter(p, p['exploration_seeds'], [p['baseline']] + accepted, 'exploration')
    (output / 'exploration.json').write_text(json.dumps(exploration, indent=2) + '\n')
    summaries = [summarize(exploration, s, p) for s in accepted]
    selected = select(summaries)
    selection = dict(selected=selected, exploration=summaries)
    # Selection persisted before generating or scoring held-out instances.
    (output / 'selection.json').write_text(json.dumps(selection, indent=2) + '\n')
    validation = experimenter(p, p['validation_seeds'], [p['baseline'], selected], 'validation') if selected else []
    result = summarize(validation, selected, p) if selected else None
    failed_runs = sum(r['status'] != 'ok' for r in exploration + validation)
    success = bool(result and result['eligible'] and result['mean_percent_reduction'] >= 1 and result['ci95'][0] > 0 and failed_runs == 0)
    (output / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
    evidence = dict(selected=selected, validation=result, success=success,
                    failed_runs=failed_runs)
    (output / 'summary.json').write_text(json.dumps(evidence, indent=2) + '\n')
    (output / 'report.md').write_text(report(p, summaries, evidence, exploration + validation))
    print(json.dumps({k: v for k, v in evidence.items() if k != 'validation'}, indent=2))
    return evidence


def report(p, summaries, evidence, rows):
    lines = ['# PROMETHEUS — Ignition 001', '',
             'Observed computational evidence from deterministic supervised software stages. No live AI agents or new scientific discovery are claimed.', '',
             '## Research question and protocol', '',
             'Can a fixed structured search process identify a strategy that improves tour length over a reproducible greedy-swap baseline?', '',
             'Closed Euclidean travelling-salesperson search is combinatorial, offline and nontrivial. '
             f"Each instance has {p['cities']} independent uniform unit-square cities. Every run starts from the same deterministic nearest-neighbor tour "
             f"(start city 0, city-index tie break), then uses exactly {p['evaluations']:,} full objective evaluations including the initial score. "
             'Distance matrix and nearest-neighbor initialization are identical preprocessing and excluded from the evaluation budget; recorded time includes initialization. '
             'Baseline: strictly improving random city swaps. Candidates: greedy segment reversal (2-opt), greedy single-city relocation, '
             f"and geometric simulated annealing with segment reversals (temperature {p['anneal_initial_temperature']} to {p['anneal_final_temperature']}, best-so-far output). "
             'Null and full-tour reversal proposals still consume an evaluation.', '',
             f"{len(p['exploration_seeds'])} exploration and {len(p['validation_seeds'])} disjoint held-out instance seeds, each with {len(p['search_seeds'])} search seeds. "
             'Mean paired percentage reduction is computed per run, then averaged within instance. '
             'Selection requires exploration mean ≥1%; maximum mean wins, lexical tie break. '
             'Held-out success requires mean ≥1%, positive lower 95% percentile bootstrap endpoint and zero paired failures. '
             f"{p['bootstrap_replicates']:,} resamples use instances as independent units. This is an internal protocol fixed before the first execution, not external preregistration. "
             'The seed lists are public for reproduction, not a blind third-party holdout.', '',
             '## Exploration — all implemented candidates', '',
             '| Candidate | Mean reduction | Instance SD | 95% bootstrap interval | W / T / L |',
             '|---|---:|---:|---|---|']
    for s in summaries:
        if s['eligible']:
            lines.append(f"| {s['candidate']} | {s['mean_percent_reduction']:.3f}% | {s['stdev_percent_reduction']:.3f}% | [{s['ci95'][0]:.3f}, {s['ci95'][1]:.3f}]% | {s['wins']} / {s['ties']} / {s['losses']} |")
        else:
            lines.append(f"| {s['candidate']} | ineligible: {s['reason']} | — | — | — |")
    lines += ['', 'Exploration intervals are descriptive; selecting a winner makes them unsuitable as confirmatory evidence.', '', '## Held-out validation', '']
    v = evidence['validation']
    if v and v['eligible']:
        lines += [f"Frozen candidate: **{evidence['selected']}**. Mean reduction **{v['mean_percent_reduction']:.3f}%**, "
                  f"instance SD {v['stdev_percent_reduction']:.3f}%, 95% interval [{v['ci95'][0]:.3f}, {v['ci95'][1]:.3f}]%. "
                  f"Instance wins / ties / losses: {v['wins']} / {v['ties']} / {v['losses']}."]
    else:
        lines += ['No eligible validation estimate. No validated improvement established.']
    lines += [f"\nPredefined success criterion met: **{evidence['success']}**. Failed runs: **{evidence['failed_runs']}**.", '',
              f"Total recorded runs: {len(rows)}; total measured elapsed search time: {sum(r['seconds'] for r in rows):.3f} seconds (hardware-dependent).", '',
              '## Integrity, limitations and follow-up', '',
              'Hypotheses were proposed with AI assistance during development and implemented as the fixed Investigator catalog. '
              'The Skeptic is a rule-based gate plus explicit methodological controls, not an autonomous critic. '
              'The Experimenter executes and independently rescores returned tours; JSON stores tours, seeds, budgets, metrics, timings and failures. '
              'No API calls, inference or network are used by the prototype.', '',
              'The baseline is a legitimate local-search heuristic, not a state-of-the-art TSP solver. Improvements may be established algorithmic advantages, '
              'not discoveries. Only uniform synthetic instances of one size and one budget are tested. Search seeds are repeated within each instance, '
              'not independent new problem instances. Equal full evaluations do not imply equal CPU cost; no wall-clock superiority is claimed. '
              'No optimality gaps are known for the 48-city instances. Bootstrap uncertainty is approximate and distribution-dependent. '
              'Fixed parameters were not tuned on these results; only one candidate is validated. Public deterministic validation can be overfit by later development. '
              'Do not reuse these holdout seeds for future confirmatory claims.', '',
              'Recommended next experiment: externally register fresh seeds spanning uniform and clustered distributions at 24, 48 and 96 cities, '
              'compare the selected method with deterministic best-improvement 2-opt, and measure both evaluation-limited and wall-time-limited performance. '
              'For small instances compute exact optima to report optimality gaps. Freeze all methods and analysis before that run.', '',
              '## Reproduction and evidence', '',
              'See `prometheus/README.md`. `manifest.json` records the full frozen protocol, source hashes and runtime. '
              '`reviews.json`, `exploration.json`, `selection.json`, `validation.json` and `summary.json` contain the complete observations and decision. '
              'Scientific outputs reproduce exactly on the recorded Python version; elapsed times and platform metadata are expected to differ.', '']
    return '\n'.join(lines)
