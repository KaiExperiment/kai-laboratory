import copy
import itertools
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from prometheus import strategies
from prometheus.experiment import ROOT, experimenter, run, select, summarize, validate_protocol
from prometheus.roles import Proposal, investigator, skeptic


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.p = json.loads((ROOT / 'protocol.json').read_text())

    def test_distance_matrix_and_reproduction(self):
        d = strategies.instance(12, 8)
        self.assertEqual(d, strategies.instance(12, 8))
        self.assertNotEqual(d, strategies.instance(13, 8))
        for i in range(8):
            self.assertEqual(d[i][i], 0)
            for j in range(8):
                self.assertEqual(d[i][j], d[j][i])

    def test_known_square_optimum_and_closure(self):
        d = [[0,1,2**.5,1],[1,0,1,2**.5],[2**.5,1,0,1],[1,2**.5,1,0]]
        self.assertEqual(strategies.length([0,1,2,3], d), 4)
        for s in strategies.STRATEGIES:
            self.assertEqual(strategies.solve(d, s, 3, 50)['length'], 4)

    def test_small_instances_against_exhaustive_optimum(self):
        d = strategies.instance(11, 7)
        optimum = min(strategies.length([0] + list(t), d) for t in itertools.permutations(range(1,7)))
        for strategy in strategies.STRATEGIES:
            result = strategies.solve(d, strategy, 7, 300)
            self.assertGreaterEqual(result['length'] + 1e-12, optimum)
            self.assertLessEqual(result['length'], result['initial_length'])
            self.assertEqual(sorted(result['tour']), list(range(7)))

    def test_actual_objective_call_budget_and_reproducibility(self):
        for budget in [1, 2, 57]:
            for strategy in strategies.STRATEGIES:
                d = strategies.instance(1, 9)
                with patch.object(strategies, 'length', wraps=strategies.length) as score:
                    a = strategies.solve(d, strategy, 19, budget)
                    self.assertEqual(score.call_count, budget)
                self.assertEqual(a, strategies.solve(d, strategy, 19, budget))

    def test_all_moves_preserve_permutation_and_input(self):
        import random
        tour = list(range(12))
        for strategy in strategies.STRATEGIES:
            rng = random.Random(4)
            for _ in range(100):
                self.assertEqual(sorted(strategies.propose(tour, strategy, rng)), tour)
                self.assertEqual(tour, list(range(12)))

    def test_invalid_strategy_and_budget_rejected(self):
        for strategy,budget in [('fiction', 5), ('swap', 0)]:
            with self.assertRaises(ValueError):
                strategies.solve(strategies.instance(1, 8), strategy, 1, budget)

    def test_skeptic_rejects_leakage_unfairness_and_unfalsifiable(self):
        for changes in [dict(measurable=False),dict(uses_holdout=True),dict(equal_budget=False)]:
            self.assertEqual(skeptic(Proposal('two_opt','reason','1%',**changes),self.p)['decision'], 'reject')
        self.assertEqual(skeptic(Proposal('fake','r','1%'),self.p)['decision'], 'reject')
        self.assertTrue(all(skeptic(h,self.p)['decision']=='accept_with_controls' for h in investigator()))

    def test_split_leakage_rejected(self):
        p = copy.deepcopy(self.p)
        p['validation_seeds'][0] = p['exploration_seeds'][0]
        with self.assertRaises(ValueError):
            validate_protocol(p)

    def test_selection_threshold_and_ties(self):
        def row(name, mean):
            return dict(candidate=name,eligible=True,mean_percent_reduction=mean)
        self.assertIsNone(select([row('a', .99)]))
        self.assertEqual(select([row('b', 2),row('a',2)]),'a')
        self.assertEqual(select([row('a',1),row('b',3)]),'b')
        self.assertIsNone(select([dict(candidate='failed',eligible=False)]))

    def test_identical_control_and_failure_handling(self):
        p = copy.deepcopy(self.p)
        p.update(search_seeds=[7],evaluations=20,cities=6,bootstrap_replicates=100)
        rows = experimenter(p,[1,2],['swap','two_opt'],'test')
        zero = summarize(rows,'swap',p)
        self.assertEqual(zero['mean_percent_reduction'],0)
        self.assertEqual(zero['ci95'],[0,0])
        rows[0]['status']='failed'
        self.assertFalse(summarize(rows,'two_opt',p)['eligible'])
        with patch('prometheus.experiment.solve',side_effect=RuntimeError('injected failure')):
            failures = experimenter(p,[1],['swap'],'test')
        self.assertEqual(failures[0]['status'],'failed')
        self.assertIn('injected failure',failures[0]['error'])

    def test_instance_is_unit_of_analysis(self):
        p = copy.deepcopy(self.p)
        p.update(search_seeds=[7,19],bootstrap_replicates=100)
        rows=[]
        for seed in [1,2]:
            for run in p['search_seeds']:
                for strategy,score in [('swap',100),('two_opt',90 if seed==1 else 110)]:
                    rows.append(dict(instance_seed=seed,search_seed=run,strategy=strategy,length=score,status='ok'))
        summary = summarize(rows,'two_opt',p)
        self.assertEqual(summary['instances'],2)
        self.assertEqual(summary['mean_percent_reduction'],0)
        self.assertEqual((summary['wins'],summary['losses']),(1,1))

    def test_pipeline_negative_result_and_preserves_evidence(self):
        p = copy.deepcopy(self.p)
        p.update(cities=5,evaluations=1,exploration_seeds=[1,2],validation_seeds=[3,4],search_seeds=[7],bootstrap_replicates=100)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'protocol.json'; path.write_text(json.dumps(p))
            output=Path(tmp)/'results'
            result=run(output,path)
            self.assertFalse(result['success'])
            self.assertIsNone(result['selected'])
            self.assertEqual(json.loads((output/'validation.json').read_text()),[])
            with self.assertRaises(ValueError):
                run(output,path)


if __name__ == '__main__':
    unittest.main()
