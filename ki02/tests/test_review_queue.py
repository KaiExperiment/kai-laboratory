import tempfile
import unittest
from pathlib import Path
from ki02.review_queue import prepare_review

class ReviewQueueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "source.txt").write_text("Observed the target result.", encoding="utf-8")
    def case(self, path="source.txt", quote="Observed the target result."):
        return {"claim_id": "c1", "observations": [
            {"id": "o1", "source_path": path, "quote": quote}]}
    def test_found_quote_never_auto_approved(self):
        report = prepare_review(self.case(), self.root)
        self.assertEqual(report["automatic_approvals"], 0)
        self.assertEqual(report["review_items"][0]["status"], "ready_for_human_review")
        self.assertFalse(report["review_items"][0]["relevance_reviewed"])
        self.assertFalse(report["review_items"][0]["provenance_reviewed"])
        self.assertEqual(len(report["review_items"][0]["source_sha256"]), 64)
    def test_mismatched_quote(self):
        report = prepare_review(self.case(quote="Not present"), self.root)
        self.assertEqual(report["review_items"][0]["status"], "quote_mismatch")
    def test_missing_file(self):
        report = prepare_review(self.case(path="missing.txt"), self.root)
        self.assertEqual(report["review_items"][0]["status"], "unavailable")
    def test_escape_rejected(self):
        with self.assertRaises(ValueError):
            prepare_review(self.case(path="../escape.txt"), self.root)
    def test_absolute_rejected(self):
        with self.assertRaises(ValueError):
            prepare_review(self.case(path="/etc/passwd"), self.root)
    def test_invalid_case_rejected(self):
        with self.assertRaises(ValueError):
            prepare_review({"claim_id": "c1"}, self.root)

if __name__ == "__main__":
    unittest.main()
