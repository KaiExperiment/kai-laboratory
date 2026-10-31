import copy
import tempfile
import unittest
from pathlib import Path
from ki02.review_queue import prepare_review
from ki02.review_log import add_event, verify
from ki02.review_audited import evaluate_with_audit_log

class AuditedReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.case = {"claim_id": "c1", "observations": []}
        for n in (1, 2):
            name = f"s{n}.txt"
            quote = f"Independent source {n} supports c1."
            (self.root / name).write_text(quote, encoding="utf-8")
            self.case["observations"].append({
                "id": f"o{n}", "claim_id": "c1", "source_id": f"s{n}",
                "independence_group": f"g{n}", "stance": "supports",
                "source_path": name, "quote": quote,
                "relevance_reviewed": False, "provenance_reviewed": False})
        self.prepared = prepare_review(self.case, self.root)
        self.decisions = {}
        self.events = []
        for item in self.prepared["review_items"]:
            sha = item["source_sha256"]
            self.decisions[item["id"]] = {
                "source_sha256": sha, "relevance_reviewed": True,
                "provenance_reviewed": True}
            self.events = add_event(
                self.events, reviewer_id="simulated", observation_id=item["id"],
                source_sha256=sha, relevance_reviewed=True,
                provenance_reviewed=True, rationale="Synthetic approval only.")
    def evaluate(self, events=None, decisions=None, **kwargs):
        return evaluate_with_audit_log(
            self.case, self.prepared,
            self.decisions if decisions is None else decisions,
            self.root, self.events if events is None else events, **kwargs)
    def test_valid_synthetic_reviews(self):
        self.assertEqual(self.evaluate(), "accept")
    def test_missing_review(self):
        with self.assertRaises(ValueError):
            self.evaluate(events=self.events[:1])
    def test_altered_log(self):
        events = copy.deepcopy(self.events)
        events[0]["payload"]["rationale"] = "forged"
        with self.assertRaises(ValueError):
            self.evaluate(events=events)
    def test_mismatched_decision(self):
        decisions = copy.deepcopy(self.decisions)
        decisions["o1"]["relevance_reviewed"] = False
        with self.assertRaises(ValueError):
            self.evaluate(decisions=decisions)
    def test_mismatched_fingerprint(self):
        events = add_event(self.events, reviewer_id="simulated",
                           observation_id="o1", source_sha256="a" * 64,
                           relevance_reviewed=True, provenance_reviewed=True,
                           rationale="Wrong source.")
        with self.assertRaises(ValueError):
            self.evaluate(events=events)
    def test_replayed_old_chain_rejected_by_checkpoint(self):
        checkpoint = verify(self.events)
        newer = add_event(self.events, reviewer_id="simulated",
                          observation_id="o1",
                          source_sha256=self.decisions["o1"]["source_sha256"],
                          relevance_reviewed=True, provenance_reviewed=True,
                          rationale="New synthetic review.")
        with self.assertRaises(ValueError):
            self.evaluate(expected_head=verify(newer))
        self.assertEqual(self.evaluate(expected_head=checkpoint), "accept")
    def test_rollback_sequence_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(minimum_sequence=3)
    def test_changed_source_rejected(self):
        (self.root / "s1.txt").write_text("Modified", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.evaluate()

if __name__ == "__main__":
    unittest.main()
