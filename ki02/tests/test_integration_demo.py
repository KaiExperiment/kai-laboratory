import unittest
from ki02.integration_demo import demo

class IntegrationDemoTests(unittest.TestCase):
    def test_review_gate_end_to_end(self):
        result = demo()
        self.assertEqual(result["review_queue_statuses"],
                         ["ready_for_human_review", "ready_for_human_review"])
        self.assertEqual(result["automatic_approvals"], 0)
        self.assertEqual(result["before_simulated_review"], "abstain")
        self.assertEqual(result["after_simulated_review"], "accept")
        self.assertEqual(result["review_type"], "simulated_not_authenticated")

if __name__ == "__main__":
    unittest.main()
