"""Adversarial claim-level corroboration tests.

AI-authored experimental tests. Quotes are synthetic and do not establish
semantic truth, source independence, or actual customer demand.
"""
import unittest
from scout.engine import evaluate


def src(text, group, digest=None):
    return dict(status='ok', text=text, sha256=digest or group,
                independence_group=group, quality=3, fixture=False)


def claim(cid, refs, critical=True):
    return dict(id=cid, text=cid, kind='observation', critical=critical,
                semantic_review='approved' if critical else None,
                evidence=[dict(source=s, quote=q, stance='supports') for s, q in refs])


def rule(claims):
    return dict(id='test', title='Synthetic regression', category='experiment',
                triggers=['premise'], hypothesis='Test claim corroboration',
                claims=claims,
                assessments={d: dict(score=4, rationale='Synthetic', claims=['critical'])
                             for d in ('feasibility', 'novelty', 'cost', 'risk')},
                risks=['Synthetic data'], uncertainties=['No semantic proof'],
                falsification_tests=['Check per-claim source support'],
                next_action=dict(scope='local', description='Run tests'))


class CriticalCorroborationTests(unittest.TestCase):
    def test_unrelated_source_cannot_rescue_critical_claim(self):
        result = evaluate(rule([
            claim('critical', [('one', 'Critical premise.')]),
            claim('context', [('two', 'Context premise.')], False),
        ]), {
            'one': src('Critical premise.', 'a'),
            'two': src('Context premise.', 'b'),
        })
        self.assertEqual(result['independent_support_count'], 2)
        self.assertEqual(result['decision'], 'abstain')
        self.assertTrue(any('critical' in b and 'independent' in b
                            for b in result['challenge']['blockers']))

    def test_same_group_cannot_rescue_critical_claim(self):
        result = evaluate(rule([
            claim('critical', [('one', 'Critical premise.'),
                               ('two', 'Second critical premise.')]),
            claim('context', [('three', 'Context premise.')], False),
        ]), {
            'one': src('Critical premise.', 'shared', 'hash-a'),
            'two': src('Second critical premise.', 'shared', 'hash-b'),
            'three': src('Context premise.', 'other'),
        })
        self.assertEqual(result['decision'], 'abstain')
        self.assertTrue(any('critical' in b and 'independent' in b
                            for b in result['challenge']['blockers']))

    def test_each_critical_claim_needs_own_support(self):
        result = evaluate(rule([
            claim('critical', [('one', 'Critical premise.'),
                               ('two', 'Second critical premise.')]),
            claim('other-critical', [('three', 'Other premise.')]),
        ]), {
            'one': src('Critical premise.', 'a'),
            'two': src('Second critical premise.', 'b'),
            'three': src('Other premise.', 'c'),
        })
        self.assertEqual(result['decision'], 'abstain')
        self.assertTrue(any('other-critical' in b for b in result['challenge']['blockers']))

    def test_two_distinct_sources_can_pass_this_gate(self):
        result = evaluate(rule([
            claim('critical', [('one', 'Critical premise.'),
                               ('two', 'Second critical premise.')]),
        ]), {
            'one': src('Critical premise.', 'a'),
            'two': src('Second critical premise.', 'b'),
        })
        self.assertEqual(result['decision'], 'shortlist')
        self.assertEqual(result['claims'][0]['semantic_validation'], 'not_performed')


if __name__ == '__main__':
    unittest.main()
