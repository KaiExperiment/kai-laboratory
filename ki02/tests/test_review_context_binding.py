"""KI-02 audit binding regression tests: detect valid reviews reused across cases.

These tests document a current limitation: event payloads identify observation
and source fingerprint, but not claim, quote, stance or independence group.
They are expected-failure tests until review events bind the full context.
"""
import copy
import unittest
from ki02.tests.test_review_audited import AuditedReviewTests

class CrossCaseReplayTests(AuditedReviewTests):
    @unittest.expectedFailure
    def test_same_observation_reused_for_different_claim(self):
        self.case["claim_id"] = "another-claim"
        self.prepared["claim_id"] = "another-claim"
        for observation in self.case["observations"]:
            observation["claim_id"] = "another-claim"
        with self.assertRaises(ValueError):
            self.evaluate()

    @unittest.expectedFailure
    def test_same_source_reused_with_changed_stance(self):
        self.case["observations"][0]["stance"] = "contradicts"
        with self.assertRaises(ValueError):
            self.evaluate()

    @unittest.expectedFailure
    def test_same_source_reused_with_changed_independence_group(self):
        self.case["observations"][1]["independence_group"] = "g1"
        with self.assertRaises(ValueError):
            self.evaluate()

if __name__ == "__main__":
    unittest.main()
