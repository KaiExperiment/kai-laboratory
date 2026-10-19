"""Verify a collected public snapshot and prepare a SCOUT source record.

No automatic claim generation: a human must assess relevance and evidence quality.
"""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime

def prepare(snapshot, source_id, publisher, title, independence_group, quality=1):
    folder = Path(snapshot)
    record = json.loads((folder / "provenance.json").read_text(encoding="utf-8"))
    if record.get("status") != "ok":
        raise ValueError("Collection did not succeed")
    if not record.get("final_url", "").startswith("https://"):
        raise ValueError("Missing HTTPS final URL")
    if not record.get("retrieved_at"):
        raise ValueError("Missing retrieval time")
    datetime.fromisoformat(record["retrieved_at"])
    raw = (folder / "source.txt").read_bytes()
    if len(raw) != record.get("bytes") or hashlib.sha256(raw).hexdigest() != record.get("sha256"):
        raise ValueError("Collected source does not match provenance")
    if not raw or len(raw) > 200_000:
        raise ValueError("Invalid source size")
    raw.decode("utf-8")
    if not source_id or not publisher or not title or not independence_group:
        raise ValueError("Source metadata required")
    if not isinstance(quality, int) or quality < 0 or quality > 4:
        raise ValueError("Quality must be 0 to 4")
    return {
        "id": source_id,
        "title": title,
        "publisher": publisher,
        "independence_group": independence_group,
        "locator": record["final_url"],
        "accessed_at": record["retrieved_at"],
        "path": "evidence/" + source_id + ".txt",
        "fixture": False,
        "quality": quality,
        "quality_rationale": "Provisional operator rating; successful retrieval and hashing do not prove factual reliability."
    }

def main():
    p = argparse.ArgumentParser(description="Verify collection and prepare a SCOUT dossier source")
    p.add_argument("--snapshot", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--publisher", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--group", required=True)
    p.add_argument("--output", required=True, help="Fresh output directory")
    a = p.parse_args()
    try:
        source = prepare(a.snapshot, a.id, a.publisher, a.title, a.group)
        output = Path(a.output)
        if output.exists():
            raise ValueError("Output directory exists")
        output.mkdir(parents=True)
        evidence = output / "evidence"
        evidence.mkdir()
        (evidence / (a.id + ".txt")).write_bytes((Path(a.snapshot) / "source.txt").read_bytes())
        (output / "source-entry.json").write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "prepared", "source": source, "note": "Add entry to a reviewed dossier; no claims or assessments were inferred."}))
        return 0
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
