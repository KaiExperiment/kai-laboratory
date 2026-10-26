"""KI-02 offline review preparation and evidence traceability.

Review records are *drafts*, never approvals. A local reviewer must inspect
source bytes and decide whether a quoted passage is relevant and trustworthy.
No external network, source execution, or automatic review flagging.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

def prepare_review(case, root):
    if not isinstance(case, dict) or not isinstance(case.get("observations"), list):
        raise ValueError("case must contain observations")
    root = Path(root).resolve()
    entries = []
    for obs in case["observations"]:
        if not isinstance(obs, dict):
            raise ValueError("observation must be an object")
        source = obs.get("source_path")
        quote = obs.get("quote")
        if not isinstance(source, str) or not source.strip():
            raise ValueError("source_path required")
        if not isinstance(quote, str) or not quote.strip():
            raise ValueError("quote required")
        relative = Path(source)
        if relative.is_absolute():
            raise ValueError("absolute source path prohibited")
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ValueError("source path escapes root")
        try:
            data = path.read_bytes()
            decoded = data.decode("utf-8")
        except (OSError, UnicodeError):
            entries.append({"id": obs.get("id"), "status": "unavailable",
                            "relevance_reviewed": False, "provenance_reviewed": False})
            continue
        entries.append({
            "id": obs.get("id"),
            "source_path": source,
            "source_sha256": hashlib.sha256(data).hexdigest(),
            "quote_found": quote in decoded,
            "status": "ready_for_human_review" if quote in decoded else "quote_mismatch",
            "relevance_reviewed": False,
            "provenance_reviewed": False,
            "warning": "Quote match does not establish relevance, truth, independence or provenance.",
        })
    return {"claim_id": case.get("claim_id"), "review_items": entries,
            "automatic_approvals": 0}

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True)
    parser.add_argument("--source-root", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.case).read_text(encoding="utf-8"))
    print(json.dumps(prepare_review(data, args.source_root), indent=2))

if __name__ == "__main__":
    main()
