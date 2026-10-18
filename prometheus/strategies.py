"""All strategies score full tours: one initial + budget-1 proposal evaluations."""
import math
import random

STRATEGIES = ('swap', 'two_opt', 'relocate', 'anneal')


def instance(seed, cities):
    rng = random.Random(seed)
    points = [(rng.random(), rng.random()) for _ in range(cities)]
    return [[math.dist(a, b) for b in points] for a in points]


def length(tour, distances):
    return math.fsum(distances[tour[i - 1]][tour[i]] for i in range(len(tour)))


def nearest_neighbor(distances):
    remaining = set(range(1, len(distances)))
    tour = [0]
    while remaining:
        city = min(remaining, key=lambda c: (distances[tour[-1]][c], c))
        remaining.remove(city)
        tour.append(city)
    return tour


def propose(tour, strategy, rng):
    trial = tour.copy()
    i, j = sorted(rng.sample(range(len(tour)), 2))
    if strategy == 'swap':
        trial[i], trial[j] = trial[j], trial[i]
    elif strategy in ('two_opt', 'anneal'):
        trial[i:j + 1] = reversed(trial[i:j + 1])
    elif strategy == 'relocate':
        # Random direction matters: sample both ordered insertion directions.
        if rng.random() < .5:
            i, j = j, i
        trial.insert(j, trial.pop(i))
    else:
        raise ValueError(strategy)
    return trial


def solve(distances, strategy, seed, budget, initial_temperature=.02, final_temperature=.0001):
    if strategy not in STRATEGIES or budget < 1 or len(distances) < 3:
        raise ValueError('Unknown strategy, invalid budget or fewer than three cities')
    rng = random.Random(seed)
    tour = nearest_neighbor(distances)
    score = best = length(tour, distances)
    best_tour = tour.copy()
    start = score
    accepted = 0
    for step in range(1, budget):
        trial = propose(tour, strategy, rng)
        value = length(trial, distances)
        delta = value - score
        temperature = initial_temperature * (final_temperature / initial_temperature) ** (step / budget)
        if delta < 0 or (strategy == 'anneal' and rng.random() < math.exp(-max(delta, 0) / temperature)):
            tour, score = trial, value
            accepted += 1
        if score < best:
            best, best_tour = score, tour.copy()
    return dict(length=best, tour=best_tour, initial_length=start,
                evaluations=budget, accepted_moves=accepted)
