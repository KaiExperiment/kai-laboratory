"""KI-02: evaluate actual SCOUT engine on its existing synthetic dossier.

Run from repo root:
  python -m ki02.scout_baseline
  python -m unittest discover -s ki02/tests -v

This measures deterministic SCOUT decisions, NOT an LLM's autonomy.
"""
from __future__ import annotations
import json
from pathlib import Path
from scout.engine import analyse

ROOT = Path(__file__).resolve().parents[1]
DOSSIER = ROOT / "scout" / "examples" / "dossier.json"
EXPECTED = {
    "csv-comparison": "fixture_shortlist",
    "sensor-experiment": "abstain",
    "research-service": "abstain",
}

def evaluate_scout(dossier=DOSSIER, expected=EXPECTED):
    result = analyse(dossier, at="2026-10-26T20:00:00+00:00")
    actual = {candidate["id"]: candidate["decision"] for candidate in result["candidates"]}
    if set(actual) != set(expected):
        raise ValueError("Dossier candidates differ from baseline labels")
    records = []
    for candidate in result["candidates"]:
        label = expected[candidate["id"]]
        records.append({
            "id": candidate["id"],
            "expected": label,
            "predicted": candidate["decision"],
            "correct": candidate["decision"] == label,
            "score": candidate["score"],
            "blockers": candidate["challenge"]["blockers"],
            "critical_claims": [
                {"id": c["id"], "status": c["status"]}
                for c in candidate["claims"] if c["critical"]
            ],
        })
    return {
        "type": "SCOUT deterministic fixture baseline",
        "source": str(Path(dossier).relative_to(ROOT)) if Path(dossier).is_relative_to(ROOT) else str(dossier),
        "model_driven": False,
        "count": len(records),
        "correct": sum(r["correct"] for r in records),
        "accuracy": sum(r["correct"] for r in records) / len(records),
        "records": records,
        "warning": "Labels were derived from the existing fixture expectations; this is a regression check, not independent validation.",
    }

if __name__ == "__main__":
    print(json.dumps(evaluate_scout(), indent=2))
