import unittest
from ki02.evidence_schema import assess


def obs(i, stance, claim='c1', group=None, relevant=True, provenance=True):
    return {'id': str(i), 'claim_id': claim, 'source_id': f'source-{i}',
            'independence_group': group or f'group-{i}', 'stance': stance,
            'relevance_reviewed': relevant, 'provenance_reviewed': provenance}

class EvidenceSchemaTests(unittest.TestCase):
    def test_two_supports_accept(self):
        self.assertEqual(assess({'claim_id': 'c1', 'observations': [obs(1, 'supports'), obs(2, 'supports')]}), 'accept')
    def test_two_contradictions_reject(self):
        self.assertEqual(assess({'claim_id': 'c1', 'observations': [obs(1, 'contradicts'), obs(2, 'contradicts')]}), 'reject')
    def test_mixed_abstains(self):
        self.assertEqual(assess({'claim_id': 'c1', 'observations': [obs(1, 'supports'), obs(2, 'contradicts')]}), 'abstain')
    def test_wrong_claim_ignored(self):
        self.assertEqual(assess({'claim_id': 'c1', 'observations': [obs(1, 'supports', 'c2'), obs(2, 'supports', 'c2')]}), 'abstain')
    def test_unreviewed_ignored(self):
        self.assertEqual(assess({'claim_id': 'c1', 'observations': [obs(1, 'supports', relevant=False), obs(2, 'supports')]}), 'abstain')
    def test_unverified_provenance_ignored(self):
        self.assertEqual(assess({'claim_id': 'c1', 'observations': [obs(1, 'supports', provenance=False), obs(2, 'supports')]}), 'abstain')
    def test_duplicate_independence_group_not_two_sources(self):
        self.assertEqual(assess({'claim_id': 'c1', 'observations': [obs(1, 'supports', group='shared'), obs(2, 'supports', group='shared')]}), 'abstain')
    def test_empty_abstains(self):
        self.assertEqual(assess({'claim_id': 'c1', 'observations': []}), 'abstain')
    def test_invalid_stance_rejected(self):
        with self.assertRaises(ValueError):
            assess({'claim_id': 'c1', 'observations': [obs(1, 'guess')]})
    def test_duplicate_id_rejected(self):
        with self.assertRaises(ValueError):
            assess({'claim_id': 'c1', 'observations': [obs(1, 'supports'), obs(1, 'supports')]})
    def test_nonboolean_review_rejected(self):
        bad = obs(1, 'supports'); bad['relevance_reviewed'] = 'yes'
        with self.assertRaises(ValueError):
            assess({'claim_id': 'c1', 'observations': [bad]})
