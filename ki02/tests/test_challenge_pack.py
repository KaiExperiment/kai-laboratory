import unittest
from ki02.challenge_pack import generate

class ChallengePackTests(unittest.TestCase):
    def test_repeatable(self):
        self.assertEqual(generate(42), generate(42))

    def test_different_seed_changes_examples(self):
        self.assertNotEqual(generate(42), generate(43))

    def test_three_labels_present(self):
        self.assertEqual({x["expected"] for x in generate(42)}, {"accept", "reject", "abstain"})

    def test_count_and_ids(self):
        cases = generate(42, 31)
        self.assertEqual(len(cases), 31)
        self.assertEqual(len({c["id"] for c in cases}), 31)

    def test_small_count_rejected(self):
        with self.assertRaises(ValueError):
            generate(1, 4)

if __name__ == "__main__":
    unittest.main()
