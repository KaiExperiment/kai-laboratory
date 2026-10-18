"""Fixed proposals and rule-based review; these are not independent AI agents."""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Proposal:
    strategy: str
    rationale: str
    prediction: str
    measurable: bool = True
    uses_holdout: bool = False
    equal_budget: bool = True


def investigator():
    """Hypotheses authored with AI assistance during development, not live inference."""
    return [
        Proposal('two_opt', 'Reverse segments to remove crossing edges that swaps miss.',
                 'At least 1% mean tour-length reduction relative to greedy swaps.'),
        Proposal('relocate', 'Move one city to repair poor local insertion choices.',
                 'At least 1% mean tour-length reduction relative to greedy swaps.'),
        Proposal('anneal', 'Accept some worsening segment reversals to escape local minima.',
                 'At least 1% mean tour-length reduction relative to greedy swaps.'),
    ]


def skeptic(proposal, protocol):
    reasons = []
    if not proposal.measurable or not proposal.prediction.strip():
        reasons.append('No falsifiable measurable prediction')
    if proposal.uses_holdout:
        reasons.append('Holdout leakage')
    if not proposal.equal_budget:
        reasons.append('Unequal objective-evaluation budget')
    if proposal.strategy not in protocol['candidates']:
        reasons.append('Unregistered implementation')
    return dict(proposal=asdict(proposal), decision='reject' if reasons else 'accept_with_controls',
                reasons=reasons, strategy_risks={
                    'two_opt': ['Segment reversal is an established heuristic, not a novel discovery.',
                                'Full-tour reversals are null moves and must still consume budget.'],
                    'relocate': ['Insertion-index conventions can bias neighborhoods; test permutation integrity.',
                                 'Local insertion improvements can still remain trapped in poor basins.'],
                    'anneal': ['Temperature is scale-dependent and may waste a short budget on worsening moves.',
                               'Use a fixed schedule and return the best observed tour; never tune on validation.']
                }.get(proposal.strategy, ['Unknown implementation requires review']), controls=[
                    'Same nearest-neighbor starting tour, instance and full-score evaluation count.',
                    'Average repeated search trials within each instance; bootstrap instances, not pseudoreplicates.',
                    'Select on exploration only; validate one frozen candidate without retuning.',
                    'Evaluation counts are equal, but wall time and proposal overhead may differ.',
                    'Uniform synthetic instances and a heuristic baseline limit generalization.'
                ])
