"""KI-02: propose a candidate without executing its contents.

This module is a local, offline *proposal intake* interface. It validates a
JSON manifest and records provenance; it does not invoke a language model,
execute generated Python, install dependencies or mutate repository files.

A model or human may prepare a manifest and candidate file separately.
The evaluator must independently review and test the candidate before use.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

REQUIRED = {"candidate_id", "author_type", "hypothesis", "target", "change_summary", "risk", "source_path"}
ALLOWED_AUTHORS = {"human", "ai_assisted", "model_generated"}
ALLOWED_TARGETS = {"ki02-evidence-classifier"}

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_manifest(manifest):
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")
    missing = REQUIRED - manifest.keys()
    if missing:
        raise ValueError("missing required fields: " + ", ".join(sorted(missing)))
    for field in REQUIRED:
        if not isinstance(manifest[field], str) or not manifest[field].strip():
            raise ValueError(f"{field} must be nonempty text")
    if manifest["author_type"] not in ALLOWED_AUTHORS:
        raise ValueError("unknown author_type")
    if manifest["target"] not in ALLOWED_TARGETS:
        raise ValueError("unknown target")
    if not manifest["candidate_id"].replace("-", "").replace("_", "").isalnum():
        raise ValueError("candidate_id must be alphanumeric with - or _")

def intake(manifest_path, allowed_root):
    path = Path(manifest_path).resolve()
    root = Path(allowed_root).resolve()
    if not path.is_relative_to(root):
        raise ValueError("manifest outside allowed root")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    candidate_path = (path.parent / manifest["source_path"]).resolve()
    if not candidate_path.is_relative_to(root):
        raise ValueError("candidate source outside allowed root")
    if not candidate_path.is_file() or candidate_path.suffix != ".py":
        raise ValueError("candidate must be an existing .py file")
    return {
        "candidate_id": manifest["candidate_id"],
        "author_type": manifest["author_type"],
        "target": manifest["target"],
        "hypothesis": manifest["hypothesis"],
        "change_summary": manifest["change_summary"],
        "risk": manifest["risk"],
        "candidate_sha256": sha256(candidate_path),
        "manifest_sha256": sha256(path),
        "execution_performed": False,
        "review_required": True,
        "warning": "Untrusted source is not executed. Static validation does not establish safety.",
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--allowed-root", required=True)
    args = parser.parse_args()
    print(json.dumps(intake(args.manifest, args.allowed_root), indent=2))

if __name__ == "__main__":
    main()
