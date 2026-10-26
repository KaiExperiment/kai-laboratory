"""KI-02: create an evaluator-controlled, deterministic synthetic challenge pack.

This does not make tests secret once shared with a candidate. Evaluator should
generate cases AFTER freezing the candidate, and never expose the generated
pack or random seed to the candidate. This generator is for engineering tests,
not a substitute for independent human-labelled real-world cases.

Usage: python -m ki02.challenge_pack --seed 90210 --output /tmp/ki02-private.json
"""
import argparse
import json
import random
from pathlib import Path

TEMPLATES = (
    ("accept", "A calibrated {instrument} measurement supports the {claim} claim; an independent replication agrees."),
    ("reject", "A calibrated {instrument} measurement contradicts the {claim} claim; a separate replication confirms the contradiction."),
    ("abstain", "A marketing page mentions that {instrument} supports {claim}, but supplies no independently checkable evidence."),
    ("abstain", "A website navigation menu includes the words '{instrument} supports {claim}', with no results."),
    ("abstain", "A report on {instrument} contradicts a different claim; there are no results for {claim}."),
)
INSTRUMENTS = ("scale", "timer", "sensor", "thermometer", "camera", "counter", "meter")
CLAIMS = ("durability", "accuracy", "stability", "efficiency", "repeatability", "reliability")

def generate(seed, count=30):
    if count < 5:
        raise ValueError("count must be at least five")
    rng = random.Random(seed)
    items = []
    for i in range(count):
        label, template = TEMPLATES[i % len(TEMPLATES)]
        evidence = template.format(instrument=rng.choice(INSTRUMENTS), claim=rng.choice(CLAIMS))
        items.append({"id": f"sealed-{i+1:03}", "evidence": evidence, "expected": label})
    rng.shuffle(items)
    return items

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--count", type=int, default=30)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    path = Path(args.output)
    if path.exists():
        p.error("Refusing to overwrite an existing pack")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        json.dump(generate(args.seed, args.count), f, indent=2)
        f.write("\n")
    print(f"Generated {args.count} synthetic cases. Keep output and seed evaluator-only.")

if __name__ == "__main__":
    main()
