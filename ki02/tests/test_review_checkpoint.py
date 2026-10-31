"""KI-02 trusted-checkpoint contract tests (synthetic)."""
import copy
import unittest
from ki02.tests.test_review_v2 import VersionedReviewTests
from ki02.review_checkpoint import (
    make_checkpoint, verify_checkpoint, evaluate_with_checkpoint)
from ki02.review_v2 import add_v2_event

class CheckpointTests(VersionedReviewTests):
    def setUp(self):
        super().setUp()
        self.checkpoint = make_checkpoint(self.events, stream_id="experiment-A")

    def checked(self, events=None, checkpoint=None, stream_id="experiment-A", **kwargs):
        return evaluate_with_checkpoint(
            self.case, self.prepared, self.decisions, self.root,
            self.events if events is None else events,
            self.checkpoint if checkpoint is None else checkpoint,
            stream_id=stream_id, **kwargs)

    def test_matching_checkpoint_accepts(self):
        self.assertEqual(self.checked(), "accept")

    def test_old_chain_rejected(self):
        with self.assertRaises(ValueError):
            self.checked(events=self.events[:1])

    def test_stream_swap_rejected(self):
        with self.assertRaises(ValueError):
            self.checked(stream_id="experiment-B")

    def test_checkpoint_replacement_rejected_if_trusted_copy_retained(self):
        # An adversary can fabricate a matching new checkpoint. Only the
        # independently retained trusted checkpoint detects the substitution.
        forged = copy.deepcopy(self.events)
        obs = self.case["observations"][0]
        forged = add_v2_event(
            forged, observation=obs,
            source_sha256=self.decisions[obs["id"]]["source_sha256"],
            reviewer_id="spoofed", relevance_reviewed=True,
            provenance_reviewed=True, rationale="Injected.")
        with self.assertRaises(ValueError):
            self.checked(events=forged)
        forged_checkpoint = make_checkpoint(forged, stream_id="experiment-A")
        self.assertEqual(self.checked(events=forged, checkpoint=forged_checkpoint), "accept")

    def test_invalid_checkpoint_schema_rejected(self):
        cp = dict(self.checkpoint, checkpoint_version=2)
        with self.assertRaises(ValueError):
            self.checked(checkpoint=cp)

    def test_checkpoint_minimum_sequence(self):
        with self.assertRaises(ValueError):
            self.checked(minimum_sequence=len(self.events) + 1)

if __name__ == "__main__":
    unittest.main()
