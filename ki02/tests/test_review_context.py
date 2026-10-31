import unittest
from ki02.tests.test_review_audited import AuditedReviewTests
from ki02.review_context import context_digest, evaluate_with_context_binding

class ContextBindingTests(AuditedReviewTests):
    def setUp(self):
        super().setUp()
        self.approvals = {
            o["id"]: {"entry_hash": next(e["entry_hash"] for e in self.events
                        if e["payload"]["observation_id"] == o["id"]),
                       "context_sha256": context_digest(o)}
            for o in self.case["observations"]}
    def bound(self):
        return evaluate_with_context_binding(
            self.case, self.prepared, self.decisions, self.root,
            self.events, context_approvals=self.approvals)
    def test_valid_context_accepts(self):
        self.assertEqual(self.bound(), "accept")
    def test_claim_replay_rejected(self):
        self.case["claim_id"] = "other"
        self.prepared["claim_id"] = "other"
        for o in self.case["observations"]:
            o["claim_id"] = "other"
        with self.assertRaises(ValueError):
            self.bound()
    def test_stance_swap_rejected(self):
        self.case["observations"][0]["stance"] = "contradicts"
        with self.assertRaises(ValueError):
            self.bound()
    def test_independence_swap_rejected(self):
        self.case["observations"][1]["independence_group"] = "g1"
        with self.assertRaises(ValueError):
            self.bound()
    def test_quote_swap_rejected(self):
        self.case["observations"][0]["quote"] = "different"
        with self.assertRaises(ValueError):
            self.bound()
    def test_missing_approval_rejected(self):
        del self.approvals["o1"]
        with self.assertRaises(ValueError):
            self.bound()
    def test_wrong_event_rejected(self):
        self.approvals["o1"]["entry_hash"] = self.events[-1]["entry_hash"]
        with self.assertRaises(ValueError):
            self.bound()

if __name__ == "__main__":
    unittest.main()
