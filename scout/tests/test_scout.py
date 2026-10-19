import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scout.engine import analyse, encoded, ingest, run, verify
from scout.review import review

EXAMPLE = Path(__file__).resolve().parents[1] / 'examples'
AT = '2026-10-19T16:00:00Z'


class ScoutTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'evidence').mkdir()
        for p in (EXAMPLE / 'evidence').iterdir():
            (self.root / 'evidence' / p.name).write_bytes(p.read_bytes())
        self.data = json.loads((EXAMPLE / 'dossier.json').read_bytes())
        self.path = self.root / 'dossier.json'

    def save(self):
        self.path.write_bytes(encoded(self.data))
        return self.path

    def result(self):
        return analyse(self.save(), AT)

    def test_fixture_ranking_and_honest_abstention(self):
        result = self.result()
        a, b, c = result['candidates']
        self.assertEqual(a['id'], 'csv-comparison')
        self.assertEqual(a['decision'], 'fixture_shortlist')
        self.assertEqual(a['score'], 67.5)
        self.assertEqual(a['claims'][-1]['status'], 'unsupported')
        self.assertEqual(b['decision'], 'abstain')
        self.assertEqual(c['decision'], 'abstain')
        self.assertTrue(all(s['fixture'] for s in result['sources']))

    def test_source_removal_challenge_weakens_leader(self):
        a = self.result()['candidates'][0]
        audits = a['challenge']['leave_one_source_out']
        self.assertEqual({x['removed_source'] for x in audits}, {'workflow', 'review'})
        self.assertTrue(all(x['decision'] == 'abstain' for x in audits))
        self.assertTrue(all(x['score'] < a['score'] for x in audits))

    def test_missing_sources_cannot_recommend(self):
        (self.root / 'evidence/workflow.txt').unlink()
        r = self.result()
        a = next(c for c in r['candidates'] if c['id'] == 'csv-comparison')
        self.assertEqual(a['decision'], 'abstain')
        self.assertTrue(any(s['status'] == 'missing' for s in r['sources']))

    def test_contradiction_overrides_optimistic_assessments(self):
        for a in self.data['opportunity_rules'][1]['assessments'].values():
            a['score'] = 4
        candidate = next(c for c in self.result()['candidates'] if c['id'] == 'sensor-experiment')
        self.assertEqual(candidate['decision'], 'abstain')
        self.assertEqual(candidate['challenge']['counterevidence'], ['equipment'])
        self.assertEqual(candidate['score'], 0)

    def test_unsupported_critical_and_fabricated_quote(self):
        rule = self.data['opportunity_rules'][0]
        rule['claims'][-1]['critical'] = True
        self.assertEqual(self.result()['candidates'][0]['decision'], 'abstain')
        rule['claims'][-1]['critical'] = False
        rule['claims'][0]['evidence'][0]['quote'] = 'Invented sales claim'
        a = self.result()['candidates'][0]
        self.assertEqual(a['decision'], 'abstain')
        self.assertFalse(a['claims'][0]['evidence'][0]['valid'])

    def test_unknown_source_and_empty_source(self):
        self.data['opportunity_rules'][0]['claims'][0]['evidence'][0]['source'] = 'nonexistent'
        (self.root / 'evidence/review.txt').write_text('')
        self.assertEqual(self.result()['candidates'][0]['decision'], 'abstain')

    def test_duplicate_content_and_groups_do_not_inflate_evidence(self):
        for mode in ('group', 'content'):
            with self.subTest(mode=mode):
                if mode == 'group':
                    self.data['sources'][1]['independence_group'] = self.data['sources'][0]['independence_group']
                else:
                    self.data['sources'][1]['independence_group'] = 'different'
                    (self.root / 'evidence/review.txt').write_bytes((self.root / 'evidence/workflow.txt').read_bytes())
                    self.data['opportunity_rules'][0]['claims'][2]['evidence'][0]['quote'] = 'Scenario A: a maker needs to compare saved pricing assumptions across products.'
                self.assertEqual(self.result()['candidates'][0]['decision'], 'abstain')

    def test_assessment_without_traceable_claim_gets_zero(self):
        self.data['opportunity_rules'][0]['assessments']['cost']['claims'] = ['fiction']
        a = self.result()['candidates'][0]
        self.assertEqual(a['scores']['cost'], 0)
        self.assertTrue(any('cost: unsupported' in x for x in a['challenge']['flags']))

    def test_low_quality_sources_force_abstention(self):
        for s in self.data['sources']:
            s['quality'] = 0
        a = self.result()['candidates'][0]
        self.assertEqual(a['scores']['evidence'], 0)
        self.assertEqual(a['decision'], 'abstain')

    def test_no_trigger_match_is_not_a_discovery(self):
        self.data['opportunity_rules'][0]['triggers'] = ['qzx-no-match']
        a = self.result()['candidates'][0]
        self.assertEqual(a['decision'], 'abstain')
        self.assertEqual(a['matched_sources'], [])

    def test_deterministic_byte_reproduction_and_ties(self):
        # Stable lexical ordering at equal score, independent of input order.
        twin = copy.deepcopy(self.data['opportunity_rules'][0])
        twin['id'] = 'aaa'
        self.data['opportunity_rules'].append(twin)
        self.assertEqual(self.result()['candidates'][0]['id'], 'aaa')
        self.save()
        run(self.path, self.root / 'a', AT)
        run(self.path, self.root / 'b', AT)
        for name in ('research.json', 'report.md', 'queue.json', 'manifest.json'):
            self.assertEqual((self.root/'a'/name).read_bytes(), (self.root/'b'/name).read_bytes())
        self.assertEqual(verify(self.root/'a'), verify(self.root/'b'))

    def test_run_freezes_inputs_and_refuses_overwrite(self):
        self.save()
        out = self.root/'run'
        run(self.path, out, AT)
        self.path.write_text('{}')
        (self.root/'evidence/workflow.txt').write_text('changed')
        verify(out)
        with self.assertRaises(FileExistsError):
            run(out/'inputs/dossier.json', out, AT)
        (out/'inputs/evidence/workflow.txt').write_text('tampered')
        with self.assertRaises(ValueError):
            verify(out)

    def test_path_escape_duplicate_ids_and_bad_scores_rejected(self):
        original = copy.deepcopy(self.data)
        mutations = [lambda d: d['sources'][0].update(path='../outside'),
                     lambda d: d['sources'][0].update(path=str(self.root/'evidence/workflow.txt')),
                     lambda d: d['sources'].append(d['sources'][0]),
                     lambda d: d['opportunity_rules'][0]['assessments']['cost'].update(score=True),
                     lambda d: d.update(question='')]
        for mutate in mutations:
            self.data = copy.deepcopy(original)
            mutate(self.data)
            with self.assertRaises(ValueError):
                ingest(self.save())

    def test_empty_question_no_sources_and_no_rules(self):
        self.data['sources'] = []
        result = self.result()
        self.assertTrue(all(c['decision'] == 'abstain' for c in result['candidates']))
        self.data['opportunity_rules'] = []
        self.assertEqual(self.result()['candidates'], [])

    def test_review_requires_selection_and_preserves_run(self):
        out = self.root/'run'
        run(self.save(), out, AT)
        initial = out/'queue.json'
        with self.assertRaises(ValueError):
            review(out, initial, self.root/'bad', 'csv-comparison', 'Obe', 'approve', 'premature', AT)
        selected = self.root/'selected.json'
        review(out, initial, selected, 'csv-comparison', 'Kai', 'select', 'Local fixture test only', AT)
        approved = self.root/'approved.json'
        review(out, selected, approved, 'csv-comparison', 'Obe', 'approve', 'Approve described local test only', AT)
        self.assertEqual(json.loads(approved.read_bytes())['items'][0]['obe'], 'approve')
        self.assertEqual(json.loads(initial.read_bytes())['events'], [])
        verify(out)
        with self.assertRaises(ValueError):
            review(out, initial, self.root/'blocked', 'research-service', 'Kai', 'select', 'bad', AT)

    def test_review_tamper_wrong_actor_and_overwrite_rejected(self):
        out=self.root/'run'
        run(self.save(), out, AT)
        initial=out/'queue.json'
        tampered=json.loads(initial.read_bytes()); tampered['items'][0]['kai']='select'
        forged=self.root/'forged'; forged.write_bytes(encoded(tampered))
        with self.assertRaises(ValueError):
            review(out, forged, self.root/'bad', 'csv-comparison', 'Obe', 'approve', 'bad', AT)
        with self.assertRaises(ValueError):
            review(out, initial, self.root/'bad', 'csv-comparison', 'someone', 'select', 'bad', AT)
        with self.assertRaises(FileExistsError):
            review(out, initial, initial, 'csv-comparison', 'Kai', 'select', 'bad', AT)

    def test_fixture_consequential_approval_blocked(self):
        self.data['opportunity_rules'][0]['next_action']['scope']='consequential'
        out=self.root/'run'; run(self.save(), out, AT)
        selected=self.root/'selected'
        review(out, out/'queue.json', selected, 'csv-comparison', 'Kai', 'select', 'Example only', AT)
        with self.assertRaises(ValueError):
            review(out, selected, self.root/'approved', 'csv-comparison', 'Obe', 'approve', 'bad', AT)

    def test_cli_failure_is_nonzero_and_writes_no_bundle(self):
        self.data['question']=''
        result=subprocess.run([sys.executable,'-m','scout','run','--input',str(self.save()),
                               '--output',str(self.root/'bad')],capture_output=True,text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Research question required',result.stderr)
        self.assertFalse((self.root/'bad').exists())

    def test_timezone_required(self):
        with self.assertRaises(ValueError):
            analyse(self.save(), '2026-10-19T16:00:00')


if __name__ == '__main__':
    unittest.main()
