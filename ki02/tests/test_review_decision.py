import hashlib
import unittest
from ki02.review_decision import evaluate_reviewed_case

def observation(i):
    return {"id": f"o{i}", "claim_id": "c1", "source_id": f"s{i}",
            "independence_group": f"g{i}", "stance": "supports",
            "relevance_reviewed": False, "provenance_reviewed": False}
def fixture():
    observations = [observation(1), observation(2)]
    h = hashlib.sha256(b"test").hexdigest()
    prepared = {"claim_id": "c1", "review_items": [
        {"id": o["id"], "status": "ready_for_human_review", "source_sha256": h}
        for o in observations]}
    decisions = {o["id"]: {"relevance_reviewed": True,
                            "provenance_reviewed": True, "source_sha256": h}
                 for o in observations}
    return {"claim_id": "c1", "observations": observations}, prepared, decisions

class ReviewDecisionTests(unittest.TestCase):
    def test_explicit_review_accepts(self):
        self.assertEqual(evaluate_reviewed_case(*fixture()), "accept")
    def test_no_review_abstains(self):
        case, prepared, decisions = fixture()
        for verdict in decisions.values():
            verdict["relevance_reviewed"] = False
        self.assertEqual(evaluate_reviewed_case(case, prepared, decisions), "abstain")
    def test_source_fingerprint_mismatch_rejected(self):
        case, prepared, decisions = fixture()
        decisions["o1"]["source_sha256"] = "changed"
        with self.assertRaises(ValueError):
            evaluate_reviewed_case(case, prepared, decisions)
    def test_mismatched_quote_cannot_be_approved(self):
        case, prepared, decisions = fixture()
        prepared["review_items"][0]["status"] = "quote_mismatch"
        with self.assertRaises(ValueError):
            evaluate_reviewed_case(case, prepared, decisions)
    def test_missing_review_rejected(self):
        case, prepared, decisions = fixture()
        del decisions["o1"]
        with self.assertRaises(ValueError):
            evaluate_reviewed_case(case, prepared, decisions)
    def test_duplicate_review_rejected(self):
        case, prepared, decisions = fixture()
        prepared["review_items"].append(dict(prepared["review_items"][0]))
        with self.assertRaises(ValueError):
            evaluate_reviewed_case(case, prepared, decisions)
    def test_non_boolean_review_rejected(self):
        case, prepared, decisions = fixture()
        decisions["o1"]["provenance_reviewed"] = "yes"
        with self.assertRaises(ValueError):
            evaluate_reviewed_case(case, prepared, decisions)
