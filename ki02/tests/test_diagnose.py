import unittest
from ki02.diagnose import diagnose

class DiagnosticTests(unittest.TestCase):
    def test_diagnostics_are_nonempty(self):
        report = diagnose()
        self.assertGreater(report['count'], 0)
        self.assertEqual(report['count'], len(report['per_case']))

    def test_known_negation_failure_is_visible(self):
        report = diagnose()
        item = next(r for r in report['per_case'] if r['id'] == 'diag-01')
        self.assertEqual(item['expected'], 'reject')
        self.assertEqual(item['predictions']['baseline'], 'abstain')

if __name__ == '__main__':
    unittest.main()
