"""Context binding regression suite: all tests must pass, no expected failures."""
import unittest
from ki02.tests.test_review_audited import AuditedReviewTests
from ki02.review_bound import add_bound_event, evaluate_bound_case

class BoundContextTests(AuditedReviewTests):
    def setUp(self):
        super().setUp()
        self.events = []
        for observation in self.case["observations"]:
            sha = self.decisions[observation["id"]]["source_sha256"]
            self.events = add_bound_event(
                self.events, observation=observation, source_sha256=sha,
                reviewer_id="synthetic", relevance_reviewed=True,
                provenance_reviewed=True, rationale="Synthetic only.")

    def evaluate(self, events=None, decisions=None, **kwargs):
        return evaluate_bound_case(
            self.case, self.prepared, self.decisions if decisions is None else decisions,
            self.root, self.events if events is None else events, **kwargs)

    def test_changed_claim_rejected(self):
        self.case["claim_id"] = self.prepared["claim_id"] = "another-claim"
        for obs in self.case["observations"]:
            obs["claim_id"] = "another-claim"
        with self.assertRaises(ValueError):
            self.evaluate()

    def test_changed_stance_rejected(self):
        self.case["observations"][0]["stance"] = "contradicts"
        with self.assertRaises(ValueError):
            self.evaluate()

    def test_changed_independence_group_rejected(self):
        self.case["observations"][1]["independence_group"] = "g1"
        with self.assertRaises(ValueError):
            self.evaluate()

    def test_changed_quote_rejected(self):
        self.case["observations"][0]["quote"] = "Different quotation"
        with self.assertRaises(ValueError):
            self.evaluate()

    def test_legacy_unbound_event_rejected(self):
        from ki02.review_log import add_event
        obs = self.case["observations"][0]
        sha = self.decisions[obs["id"]]["source_sha256"]
        legacy = add_event([], reviewer_id="synthetic", observation_id=obs["id"],
                           source_sha256=sha, relevance_reviewed=True,
                           provenance_reviewed=True, rationale="Unbound.")
        with self.assertRaises(ValueError):
            self.evaluate(events=legacy)

if __name__ == "__main__":
    unittest.main()
