"""Versioned audit regression suite, using synthetic reviewer events."""
import copy
import unittest
from ki02.tests.test_review_audited import AuditedReviewTests
from ki02.review_v2 import add_v2_event, evaluate_v2, verify_v2, verify_historical_v1
from ki02.review_log import add_event

class VersionedReviewTests(AuditedReviewTests):
    def setUp(self):
        super().setUp()
        self.events = []
        for observation in self.case["observations"]:
            self.events = add_v2_event(
                self.events, observation=observation,
                source_sha256=self.decisions[observation["id"]]["source_sha256"],
                reviewer_id="synthetic", relevance_reviewed=True,
                provenance_reviewed=True, rationale="Simulated only.")

    def evaluate(self, events=None, decisions=None, **kwargs):
        return evaluate_v2(self.case, self.prepared,
                           self.decisions if decisions is None else decisions,
                           self.root, self.events if events is None else events, **kwargs)

    def test_mismatched_fingerprint(self):
        observation = self.case["observations"][0]
        wrong = add_v2_event(
            self.events, observation=observation, source_sha256="a" * 64,
            reviewer_id="synthetic", relevance_reviewed=True,
            provenance_reviewed=True, rationale="Wrong source.")
        with self.assertRaises(ValueError):
            self.evaluate(events=wrong)

    def test_replayed_old_chain_rejected_by_checkpoint(self):
        checkpoint = verify_v2(self.events)
        observation = self.case["observations"][0]
        newer = add_v2_event(
            self.events, observation=observation,
            source_sha256=self.decisions[observation["id"]]["source_sha256"],
            reviewer_id="synthetic", relevance_reviewed=True,
            provenance_reviewed=True, rationale="New review.")
        with self.assertRaises(ValueError):
            self.evaluate(expected_head=verify_v2(newer))
        self.assertEqual(self.evaluate(expected_head=checkpoint), "accept")

    def test_reviewer_identity_is_not_authenticated(self):
        # An attacker who can append and rehash a chain can claim any reviewer ID.
        # This passing test documents a limitation, not a security guarantee.
        observation = self.case["observations"][0]
        forged = add_v2_event(
            self.events, observation=observation,
            source_sha256=self.decisions[observation["id"]]["source_sha256"],
            reviewer_id="unverified-other-reviewer",
            relevance_reviewed=True, provenance_reviewed=True,
            rationale="Unverified identity.")
        self.assertEqual(evaluate_v2(
            self.case, self.prepared, self.decisions, self.root, forged), "accept")

    def test_rejected_latest_review_blocks_older_approval(self):
        observation = self.case["observations"][0]
        rejected = add_v2_event(
            self.events, observation=observation,
            source_sha256=self.decisions[observation["id"]]["source_sha256"],
            reviewer_id="synthetic", relevance_reviewed=False,
            provenance_reviewed=False, rationale="Approval withdrawn.")
        with self.assertRaises(ValueError):
            self.evaluate(events=rejected)

    def test_invalid_schema_version_rejected(self):
        events = copy.deepcopy(self.events)
        events[0]["payload"]["schema_version"] = 3
        with self.assertRaises(ValueError):
            self.evaluate(events=events)

    def test_duplicate_observation_rejected(self):
        self.case["observations"].append(copy.deepcopy(self.case["observations"][0]))
        with self.assertRaises(ValueError):
            self.evaluate()

    def test_explicit_v2_context_digest(self):
        self.assertEqual(self.events[0]["payload"]["schema_version"], 2)
        self.assertEqual(len(self.events[0]["payload"]["context_sha256"]), 64)
        self.assertEqual(self.evaluate(), "accept")

    def test_claim_change_fails(self):
        self.case["claim_id"] = self.prepared["claim_id"] = "different"
        for obs in self.case["observations"]:
            obs["claim_id"] = "different"
        with self.assertRaises(ValueError):
            self.evaluate()

    def test_stance_change_fails(self):
        self.case["observations"][0]["stance"] = "contradicts"
        with self.assertRaises(ValueError):
            self.evaluate()

    def test_group_change_fails(self):
        self.case["observations"][0]["independence_group"] = "other"
        with self.assertRaises(ValueError):
            self.evaluate()

    def test_context_digest_tamper_fails(self):
        events = copy.deepcopy(self.events)
        events[0]["payload"]["context_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.evaluate(events=events)

    def test_v1_cannot_authorise_v2(self):
        obs = self.case["observations"][0]
        legacy = add_event([], reviewer_id="synthetic", observation_id=obs["id"],
                           source_sha256=self.decisions[obs["id"]]["source_sha256"],
                           relevance_reviewed=True, provenance_reviewed=True,
                           rationale="Historical event.")
        self.assertEqual(len(verify_historical_v1(legacy)), 64)
        with self.assertRaises(ValueError):
            self.evaluate(events=legacy)

    def test_truncated_log_with_checkpoint_fails(self):
        with self.assertRaises(ValueError):
            self.evaluate(events=self.events[:1], expected_head=verify_v2(self.events))

if __name__ == "__main__":
    unittest.main()
