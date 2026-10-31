import tempfile
import unittest
from pathlib import Path
from ki02.review_queue import prepare_review
from ki02.review_recheck import evaluate_with_source_recheck

class ReviewRecheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.case = {"claim_id": "c1", "observations": []}
        for i in (1, 2):
            name = f"s{i}.txt"
            quote = f"Independent observation {i} supports c1."
            (self.root / name).write_text(quote, encoding="utf-8")
            self.case["observations"].append({
                "id": f"o{i}", "claim_id": "c1", "source_id": f"s{i}",
                "independence_group": f"g{i}", "stance": "supports",
                "source_path": name, "quote": quote,
                "relevance_reviewed": False, "provenance_reviewed": False})
        self.prepared = prepare_review(self.case, self.root)
        self.decisions = {item["id"]: {
            "relevance_reviewed": True, "provenance_reviewed": True,
            "source_sha256": item["source_sha256"]}
            for item in self.prepared["review_items"]}
    def evaluate(self):
        return evaluate_with_source_recheck(self.case, self.prepared, self.decisions, self.root)
    def test_unchanged_source_accepts_simulated_approval(self):
        self.assertEqual(self.evaluate(), "accept")
    def test_modified_source_fails_closed(self):
        (self.root / "s1.txt").write_text("Different contents", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.evaluate()
    def test_deleted_source_fails_closed(self):
        (self.root / "s1.txt").unlink()
        with self.assertRaises(ValueError):
            self.evaluate()
    def test_source_path_swap_fails_closed(self):
        self.case["observations"][0]["source_path"] = "s2.txt"
        with self.assertRaises(ValueError):
            self.evaluate()
    def test_quote_change_fails_closed(self):
        self.case["observations"][0]["quote"] = "not in document"
        with self.assertRaises(ValueError):
            self.evaluate()
    def test_missing_approval_still_abstains(self):
        self.decisions["o1"]["relevance_reviewed"] = False
        self.assertEqual(self.evaluate(), "abstain")
