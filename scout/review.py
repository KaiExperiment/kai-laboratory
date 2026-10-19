"""Local review attestations. This module never executes proposed actions."""
import json
from copy import deepcopy
from pathlib import Path

from .engine import encoded, require, sha, timestamp, verify


def transition(queue, candidate, actor, decision, note, at):
    require(actor in ('Kai', 'Obe'), 'Actor must be Kai or Obe')
    require(isinstance(note, str) and bool(note.strip()), 'Review note required')
    item = next((i for i in queue['items'] if i['candidate'] == candidate), None)
    require(item is not None, 'Unknown candidate')
    if actor == 'Kai':
        require(item['kai'] == 'pending', 'Kai decision already recorded or candidate blocked')
        require(decision in ('select', 'reject'), 'Kai may select or reject')
        item['kai'] = decision
    else:
        require(item['kai'] == 'select', 'Kai must select before Obe review')
        require(item['obe'] == 'pending', 'Obe decision already recorded')
        require(decision in ('approve', 'reject'), 'Obe may approve or reject')
        require(not (decision == 'approve' and item['fixture'] and item['action']['scope'] == 'consequential'),
                'Fixture evidence cannot approve consequential action; create a genuine-evidence run')
        item['obe'] = decision
    queue['events'].append(dict(candidate=candidate, actor=actor, decision=decision, note=note, timestamp=timestamp(at)))
    return queue


def review(run_dir, queue_path, output, candidate, actor, decision, note, at=None):
    verify(run_dir)
    initial = json.loads((Path(run_dir) / 'queue.json').read_bytes())
    supplied = json.loads(Path(queue_path).read_bytes())
    # Rebuild transitions to reject accidental queue edits, foreign runs or bypassed stages.
    rebuilt = deepcopy(initial)
    for event in supplied.get('events', []):
        transition(rebuilt, event['candidate'], event['actor'], event['decision'], event['note'], event['timestamp'])
    require(rebuilt == supplied, 'Queue differs from its run/history')
    before = sha(encoded(supplied))
    transition(supplied, candidate, actor, decision, note, at)
    # No overwrite, including of the frozen run's queue. Caller chooses a new file.
    with Path(output).open('xb') as f:
        f.write(encoded(supplied))
    return dict(queue=output, previous_sha256=before, executed_actions=0)
