"""Adversarial semantic-validity probes for SCOUT.

A matching quote alone does not prove a claim. These tests document the
limitation and ensure insufficient corroboration still blocks promotion.
"""
import unittest
from scout.engine import evaluate

def source(text, group, quality=3):
    return {"status": "ok", "text": text, "sha256": group,
            "independence_group": group, "quality": quality, "fixture": False}

def rule():
    return {
        "id": "false-demand", "title": "Misleading citation probe",
        "category": "product", "triggers": ["fee"],
        "hypothesis": "Makers will pay for a tool",
        "claims": [{
            "id": "demand", "text": "Makers will pay for a tool",
            "kind": "observation", "critical": True,
            "evidence": [{"source": "policy", "quote": "A fee exists.", "stance": "supports"}]
        }],
        "assessments": {d: {"score": 4, "rationale": "Deliberately inflated operator rating",
                             "claims": ["demand"]} for d in ("feasibility", "novelty", "cost", "risk")},
        "risks": ["Misleading conclusion"], "uncertainties": ["No demand study"],
        "falsification_tests": ["Interview customers"],
        "next_action": {"scope": "local", "description": "Seek demand evidence"}
    }

class SemanticLimitTests(unittest.TestCase):
    def test_single_irrelevant_quote_cannot_shortlist(self):
        candidate = evaluate(rule(), {"policy": source("A fee exists. A fee applies.", "policy")})
        self.assertEqual(candidate["decision"], "abstain")
        self.assertIn("Fewer than two independent, nonduplicate supporting sources",
                      candidate["challenge"]["blockers"])

    def test_quote_is_traceable_not_semantically_proven(self):
        candidate = evaluate(rule(), {"policy": source("A fee exists.", "policy")})
        self.assertEqual(candidate["claims"][0]["status"], "traceable")
        self.assertEqual(candidate["decision"], "abstain")
        # The above traceability is NOT evidence that anyone will pay.
        # Future semantic validation must address this limitation explicitly.

if __name__ == "__main__":
    unittest.main()
