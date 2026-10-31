"""KI-02 evidence contract v1: validate structured assertions, not free-text truth.

This module deliberately DOES NOT infer evidence from prose or verify source
truth. Operator-supplied assertions are inputs, not independently established
facts. Ambiguous or conflicting assertions produce abstention.
"""
from __future__ import annotations

LABELS = frozenset({'accept', 'reject', 'abstain'})
STANCES = frozenset({'supports', 'contradicts', 'neutral'})


def assess(case):
    """Return a conservative decision for a validated structured case.

    Each observation explicitly identifies its target claim, source, stance,
    independence group, and whether its relevance and provenance were reviewed.
    This is a *decision policy*, not a semantic verifier.
    """
    if not isinstance(case, dict):
        raise ValueError('case must be an object')
    claim_id = case.get('claim_id')
    observations = case.get('observations')
    if not isinstance(claim_id, str) or not claim_id.strip():
        raise ValueError('claim_id must be nonempty text')
    if not isinstance(observations, list):
        raise ValueError('observations must be a list')
    seen_ids = set()
    support_groups, counter_groups = set(), set()
    for item in observations:
        if not isinstance(item, dict):
            raise ValueError('observation must be an object')
        for key in ('id', 'claim_id', 'source_id', 'independence_group'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f'{key} must be nonempty text')
        if item['id'] in seen_ids:
            raise ValueError('duplicate observation id')
        seen_ids.add(item['id'])
        if item.get('stance') not in STANCES:
            raise ValueError('invalid stance')
        for key in ('relevance_reviewed', 'provenance_reviewed'):
            if type(item.get(key)) is not bool:
                raise ValueError(f'{key} must be boolean')
        if item['claim_id'] != claim_id:
            continue
        if not (item['relevance_reviewed'] and item['provenance_reviewed']):
            continue
        if item['stance'] == 'supports':
            support_groups.add(item['independence_group'])
        elif item['stance'] == 'contradicts':
            counter_groups.add(item['independence_group'])
    # Contradictions and uncertainty are not resolved by counting votes.
    if support_groups and counter_groups:
        return 'abstain'
    # Require at least two operator-declared independent corroborations.
    if len(support_groups) >= 2:
        return 'accept'
    if len(counter_groups) >= 2:
        return 'reject'
    return 'abstain'
