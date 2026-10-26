"""KI-02 offline end-to-end demonstration.

The reviewer decisions below are explicitly simulated test inputs, not
authentic human approvals. No claim about real-world evidence is made.
"""
from __future__ import annotations
import json
import tempfile
from pathlib import Path
from .review_queue import prepare_review
from .review_recheck import evaluate_with_source_recheck

def demo():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "first.txt").write_text("Measurement A supports the target claim.", encoding="utf-8")
        (root / "second.txt").write_text("Measurement B supports the target claim.", encoding="utf-8")
        observations = []
        for i, name, quote in (
            (1, "first.txt", "Measurement A supports the target claim."),
            (2, "second.txt", "Measurement B supports the target claim."),
        ):
            observations.append({
                "id": f"obs-{i}", "claim_id": "synthetic-claim",
                "source_id": f"source-{i}", "independence_group": f"group-{i}",
                "stance": "supports", "source_path": name, "quote": quote,
                "relevance_reviewed": False, "provenance_reviewed": False,
            })
        case = {"claim_id": "synthetic-claim", "observations": observations}
        prepared = prepare_review(case, root)
        unreviewed = {
            item["id"]: {
                "relevance_reviewed": False, "provenance_reviewed": False,
                "source_sha256": item["source_sha256"],
            }
            for item in prepared["review_items"]
        }
        before = evaluate_with_source_recheck(case, prepared, unreviewed, root)
        # Simulated review approval for this synthetic integration fixture ONLY.
        simulated = {
            key: {**value, "relevance_reviewed": True, "provenance_reviewed": True}
            for key, value in unreviewed.items()
        }
        after = evaluate_with_source_recheck(case, prepared, simulated, root)
        return {"review_queue_statuses": [i["status"] for i in prepared["review_items"]],
                "automatic_approvals": prepared["automatic_approvals"],
                "before_simulated_review": before,
                "after_simulated_review": after,
                "review_type": "simulated_not_authenticated"}

if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))
