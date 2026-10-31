"""Checkpoint evolution regression tests."""
import copy
import unittest
from ki02.tests.test_review_checkpoint import CheckpointTests
from ki02.review_extension import verify_extension, evaluate_extension
from ki02.review_v2 import add_v2_event
from ki02.review_checkpoint import make_checkpoint

class ExtensionTests(CheckpointTests):
    def extend(self, events=None):
        observation = self.case["observations"][0]
        return add_v2_event(
            self.events if events is None else events,
            observation=observation,
            source_sha256=self.decisions[observation["id"]]["source_sha256"],
            reviewer_id="synthetic", relevance_reviewed=True,
            provenance_reviewed=True, rationale="Synthetic continuation.")

    def test_valid_extension_produces_candidate_checkpoint(self):
        extended = self.extend()
        candidate = verify_extension(extended, self.checkpoint, stream_id="experiment-A")
        self.assertEqual(candidate["sequence"], len(extended))
        self.assertEqual(evaluate_extension(
            self.case, self.prepared, self.decisions, self.root, extended,
            self.checkpoint, stream_id="experiment-A")[0], "accept")

    def test_forged_prefix_rejected_even_if_chain_rehashed(self):
        forged = copy.deepcopy(self.events)
        forged[0]["payload"]["reviewer_id"] = "impostor"
        # Reconstruct a valid chain from the altered first event.
        forged[0]["previous_hash"] = "0" * 64
        from ki02.review_v2 import _hash
        forged[0]["entry_hash"] = _hash(forged[0]["previous_hash"], forged[0]["payload"])
        for index in range(1, len(forged)):
            forged[index]["previous_hash"] = forged[index-1]["entry_hash"]
            forged[index]["entry_hash"] = _hash(forged[index]["previous_hash"], forged[index]["payload"])
        with self.assertRaises(ValueError):
            verify_extension(self.extend(forged), self.checkpoint, stream_id="experiment-A")

    def test_truncated_prefix_rejected(self):
        with self.assertRaises(ValueError):
            verify_extension(self.events[:1], self.checkpoint, stream_id="experiment-A")

    def test_wrong_stream_rejected(self):
        with self.assertRaises(ValueError):
            verify_extension(self.extend(), self.checkpoint, stream_id="experiment-B")

    def test_untrusted_forged_checkpoint_cannot_be_distinguished(self):
        # This deliberately shows why the checkpoint MUST be externally trusted.
        forged = self.extend()
        fabricated = make_checkpoint(forged, stream_id="experiment-A")
        self.assertEqual(
            verify_extension(forged, fabricated, stream_id="experiment-A"),
            fabricated)

if __name__ == "__main__":
    unittest.main()
