"""KI-02 comparison runner for the three frozen heuristic implementations.

This is a smoke-test benchmark on *public, synthetic* development cases only.
It is not an independent or blinded evaluation. Proposals are imported from a
reviewed, explicit allowlist rather than from arbitrary manifest paths.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
from .benchmark import baseline, load_cases, score
from .candidate_v0 import candidate as candidate_v0

ROOT = Path(__file__).resolve().parent
PROPOSAL_001 = ROOT / "proposals" / "architect-001" / "candidate_001.py"

def load_proposal_001():
    spec = importlib.util.spec_from_file_location("ki02_reviewed_proposal_001", PROPOSAL_001)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.candidate

def compare(cases):
    implementations = {
        "baseline": baseline,
        "candidate_v0": candidate_v0,
        "architect_001": load_proposal_001(),
    }
    reports = {name: score(cases, fn) for name, fn in implementations.items()}
    return {
        "kind": "public synthetic development comparison",
        "count": len(cases),
        "scores": {name: {"correct": r["correct"], "accuracy": r["accuracy"],
                          "abstentions": sum(x["predicted"] == "abstain" for x in r["results"])}
                   for name, r in reports.items()},
        "per_case": [
            {"id": case["id"], "expected": case["expected"],
             "predictions": {name: reports[name]["results"][i]["predicted"] for name in reports}}
            for i, case in enumerate(cases)
        ],
        "warning": "Not blinded; development cases were available to the proposal author.",
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=("dev",), default="dev")
    args = parser.parse_args()
    print(json.dumps(compare(load_cases(args.split)), indent=2))

if __name__ == "__main__":
    main()
