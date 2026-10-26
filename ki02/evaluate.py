"""KI-02 evaluator: compare frozen predictors on evaluator-controlled cases.

Run from repository root:
  python -m ki02.evaluate --cases /private/path/challenge.json --output /private/path/results.json

Do not commit private cases or per-case results to a public repository.
This is a deterministic synthetic engineering check, not proof of generalisation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from .benchmark import baseline, score
from .candidate_v0 import candidate

LABELS = {"accept", "reject", "abstain"}

def validate_cases(cases):
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a nonempty list")
    ids = set()
    for item in cases:
        if not isinstance(item, dict):
            raise ValueError("case must be an object")
        if not isinstance(item.get("id"), str) or not item["id"].strip() or item["id"] in ids:
            raise ValueError("case IDs must be nonempty and unique")
        ids.add(item["id"])
        if not isinstance(item.get("evidence"), str):
            raise ValueError("evidence must be text")
        if item.get("expected") not in LABELS:
            raise ValueError("invalid expected label")

def evaluate(cases):
    validate_cases(cases)
    b = score(cases, baseline)
    c = score(cases, candidate)
    return {
        "schema_version": 1,
        "count": len(cases),
        "baseline_correct": b["correct"],
        "candidate_correct": c["correct"],
        "baseline_accuracy": b["accuracy"],
        "candidate_accuracy": c["accuracy"],
        "delta_correct": c["correct"] - b["correct"],
        "delta_accuracy": c["accuracy"] - b["accuracy"],
        "baseline_abstentions": sum(r["predicted"] == "abstain" for r in b["results"]),
        "candidate_abstentions": sum(r["predicted"] == "abstain" for r in c["results"]),
        "case_digest_sha256": hashlib.sha256(
            json.dumps(cases, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "baseline_source_sha256": hashlib.sha256(
            (Path(__file__).parent / "benchmark.py").read_bytes()
        ).hexdigest(),
        "candidate_source_sha256": hashlib.sha256(
            (Path(__file__).parent / "candidate_v0.py").read_bytes()
        ).hexdigest(),
        "limitations": [
            "Candidate was developed with access to the six dev examples.",
            "Template generator code is public; generated cases are not an independent semantic benchmark.",
            "All predictions are deterministic text heuristics, not a language model.",
            "Accuracy alone does not establish reliability on real-world evidence.",
        ],
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cases", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    report = evaluate(cases)
    output = Path(args.output)
    if output.exists():
        p.error("Refusing to overwrite an existing evaluation report")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("limitations",)}, indent=2))

if __name__ == "__main__":
    main()
