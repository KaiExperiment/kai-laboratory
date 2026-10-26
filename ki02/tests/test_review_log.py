import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from ki02.review_log import add_event, load, save_new, verify, GENESIS

class ReviewLogTests(unittest.TestCase):
    def make(self):
        return add_event([], reviewer_id="synthetic-reviewer", observation_id="o1",
                         source_sha256=hashlib.sha256(b"source").hexdigest(),
                         relevance_reviewed=True, provenance_reviewed=False,
                         rationale="Synthetic review fixture, not verified.",
                         timestamp_utc="2026-10-26T23:00:00+00:00")
    def test_chain_verifies(self):
        self.assertEqual(verify(self.make()), self.make()[0]["entry_hash"])
    def test_mutation_detected(self):
        events = self.make()
        events[0]["payload"]["rationale"] = "changed"
        with self.assertRaises(ValueError):
            verify(events)
    def test_sequence_detected(self):
        events = self.make()
        events[0]["sequence"] = 2
        with self.assertRaises(ValueError):
            verify(events)
    def test_chain_linking(self):
        events = self.make()
        more = add_event(events, reviewer_id="synthetic-reviewer", observation_id="o2",
                         source_sha256=hashlib.sha256(b"source2").hexdigest(),
                         relevance_reviewed=False, provenance_reviewed=False,
                         rationale="No review performed.")
        self.assertEqual(len(more), 2)
        self.assertEqual(more[1]["previous_hash"], more[0]["entry_hash"])
    def test_empty_genesis(self):
        self.assertEqual(verify([]), GENESIS)
    def test_new_file_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review.json"
            save_new(path, self.make())
            self.assertEqual(load(path), self.make())
            with self.assertRaises(FileExistsError):
                save_new(path, self.make())
    def test_invalid_flag_rejected(self):
        with self.assertRaises(ValueError):
            add_event([], reviewer_id="r", observation_id="o",
                      source_sha256=hashlib.sha256(b"x").hexdigest(),
                      relevance_reviewed="yes", provenance_reviewed=False,
                      rationale="bad")

if __name__ == "__main__":
    unittest.main()
