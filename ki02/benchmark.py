"""KI-02 benchmark: deterministic, dependency-free scoring infrastructure.

This is NOT an AI agent. It establishes a measurable baseline for future
SCOUT wrappers / Architect-generated candidates. All fixtures are synthetic.
Run: python -m unittest discover -s ki02/tests -v
Run: python -m ki02.benchmark --split dev
Held-out test is intentionally not evaluated during candidate development.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = ROOT / "cases.json"

def load_cases(split):
    data = json.loads(CASES.read_text(encoding="utf-8"))
    if split not in ("dev", "holdout"):
        raise ValueError("split must be dev or holdout")
    return [case for case in data if case["split"] == split]

def baseline(case):
    """Deliberately naive reference policy, not a language model."""
    text = case["evidence"].lower()
    if "contradicts" in text:
        return "reject"
    if "supports" in text:
        return "accept"
    return "abstain"

def score(cases, predictor=baseline):
    results = []
    for case in cases:
        predicted = predictor(case)
        if predicted not in ("accept", "reject", "abstain"):
            raise ValueError("invalid prediction")
        results.append({"id": case["id"], "expected": case["expected"],
                        "predicted": predicted, "correct": predicted == case["expected"]})
    n = len(results)
    return {"count": n, "correct": sum(r["correct"] for r in results),
            "accuracy": sum(r["correct"] for r in results) / n if n else None,
            "results": results}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--split", choices=("dev", "holdout"), default="dev")
    args = p.parse_args()
    print(json.dumps(score(load_cases(args.split)), indent=2))

if __name__ == "__main__":
    main()
