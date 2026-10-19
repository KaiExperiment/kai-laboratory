import unittest
from scout.review_chain import append_event, GENESIS
from scout.engine import encoded, sha


class ReviewChainTests(unittest.TestCase):
    def test_append_creates_verifiable_links_without_mutating_history(self):
        first = append_event([], 'rejected', 'reviewer-a', 'Insufficient support', '2026-10-19T18:00:00Z')
        self.assertEqual(first[0]['previous_hash'], GENESIS)
        self.assertEqual(first[0]['event_hash'], sha(encoded({k: v for k, v in first[0].items() if k != 'event_hash'})))
        second = append_event(first, 'approved', 'reviewer-b', 'Reassessed evidence', '2026-10-19T19:00:00Z')
        self.assertEqual(len(first), 1)
        self.assertEqual(second[1]['previous_hash'], first[0]['event_hash'])

    def test_reverse_timestamp_rejected(self):
        history = append_event([], 'rejected', 'reviewer-a', 'Insufficient support', '2026-10-19T19:00:00Z')
        with self.assertRaisesRegex(ValueError, 'chronological'):
            append_event(history, 'approved', 'reviewer-b', 'Changed view', '2026-10-19T18:00:00Z')


if __name__ == '__main__':
    unittest.main()
