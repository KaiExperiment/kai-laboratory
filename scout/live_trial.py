"""Create a conservative SCOUT dossier from one verified collected source.

This is a deterministic smoke test, not automatic market research. No market
demand, novelty, or willingness-to-pay claims are inferred from the source.
"""
import argparse
import json
import shutil
from pathlib import Path

def build(prepared, output):
    source_folder = Path(prepared)
    source = json.loads((source_folder / "source-entry.json").read_text(encoding="utf-8"))
    source_file = source_folder / source["path"]
    if not source_file.is_file():
        raise ValueError("Prepared evidence file is missing")
    if source.get("fixture") is not False or source.get("quality", 99) > 1:
        raise ValueError("This trial requires conservative real-source metadata")
    dest = Path(output)
    if dest.exists():
        raise ValueError("Output already exists")
    dest.mkdir(parents=True)
    (dest / "evidence").mkdir()
    shutil.copyfile(source_file, dest / source["path"])
    dossier = {
        "schema_version": 1,
        "question": "Can a single live public-source snapshot establish demand for a new maker tool? Expected result: abstain.",
        "sources": [source],
        "opportunity_rules": [{
            "id": "maker-opportunity-unverified",
            "title": "Unverified maker software opportunity",
            "category": "product",
            "triggers": ["User-agent"],
            "hypothesis": "A new maker tool could have demand; no such demand is evidenced here.",
            "claims": [
                {"id": "demand-unverified", "text": "UK makers would adopt or pay for a new tool.",
                 "kind": "speculation", "critical": True, "evidence": []}
            ],
            "assessments": {},
            "risks": ["No evidence of customer demand"],
            "uncertainties": ["This source is unrelated to maker demand", "No independent corroboration"],
            "falsification_tests": ["Collect direct, attributable maker demand evidence"],
            "next_action": {"scope": "local", "description": "Seek relevant evidence; do not build or contact anyone"}
        }]
    }
    (dest / "dossier.json").write_text(json.dumps(dossier, indent=2) + "\n", encoding="utf-8")
    return dest

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prepared", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    try:
        print(json.dumps({"dossier": str(build(a.prepared, a.output))}))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
