"""Deterministic evidence ingestion, opportunity matching, scoring and challenge."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

VERSION = '0.1.0'
WEIGHTS = {'feasibility': 25, 'novelty': 10, 'cost': 20, 'risk': 15, 'evidence': 30}
LIMITATIONS = [
    'Offline ingestion only: no web search, live research, language model or external actions.',
    'Opportunity rules, claims and assessments are supplied by the operator; matching is lexical.',
    'Exact quotes prove traceability, not truth, relevance or logical entailment.',
    'Contradictions require operator annotations; unannotated semantic conflicts may be missed.',
    'Source independence and fixture labels are operator declarations, not independently verified.',
    'Novelty scores do not establish market novelty, patentability, demand or scientific discovery.',
    'Review identities are local attestations, not authenticated access control.',
]


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def timestamp(value=None):
    value = value or datetime.now(timezone.utc).isoformat(timespec='seconds')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.utcoffset() is None:
        raise ValueError('Timestamp must include a timezone')
    return parsed.astimezone(timezone.utc).isoformat(timespec='seconds')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def unique(rows, label):
    require(isinstance(rows, list), f'{label} must be a list')
    require(all(isinstance(r, dict) for r in rows), f'{label} entries must be objects')
    ids = [r.get('id') for r in rows]
    require(all(nonempty(i) for i in ids) and len(ids) == len(set(ids)), f'Invalid/duplicate {label} IDs')


def ingest(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    data = json.loads(raw)
    require(isinstance(data, dict), 'Dossier must be an object')
    require(data.get('schema_version') == 1, 'Unsupported schema_version')
    require(nonempty(data.get('question')), 'Research question required')
    for key in ('sources', 'opportunity_rules'):
        unique(data.get(key), key)
    sources = {}
    for s in data['sources']:
        for key in ('title', 'publisher', 'independence_group', 'locator', 'accessed_at', 'path'):
            require(nonempty(s.get(key)), f'Source {s["id"]}: {key} required')
        require(type(s.get('quality')) is int and 0 <= s['quality'] <= 4 and nonempty(s.get('quality_rationale')), 'Source quality 0-4 and rationale required')
        require(type(s.get('fixture')) is bool, 'Source fixture flag must be boolean')
        timestamp(s['accessed_at'])
        require(not Path(s['path']).is_absolute(), 'Source paths must be relative')
        require(Path(s['path']).parts[0] == 'evidence', 'Sources must be under evidence/')
        source_path = (path.parent / s['path']).resolve()
        require(source_path.is_relative_to(path.parent), 'Sources must stay inside dossier directory')
        record = dict(s)
        try:
            content = source_path.read_bytes()
            record.update(status='ok', sha256=sha(content), text=content.decode('utf-8'))
            if not record['text'].strip():
                record.update(status='missing', error='Empty source')
        except (OSError, UnicodeError) as e:
            record.update(status='missing', error=type(e).__name__, text='', sha256=None)
        sources[s['id']] = record
    for rule in data['opportunity_rules']:
        for key in ('title', 'hypothesis', 'category'):
            require(nonempty(rule.get(key)), f'Rule {rule["id"]}: {key} required')
        require(rule['category'] in ('product', 'invention', 'service', 'experiment'), 'Invalid category')
        require(isinstance(rule.get('triggers'), list) and rule['triggers'] and
                all(nonempty(t) for t in rule['triggers']), 'Nonempty trigger list required')
        unique(rule.get('claims'), 'claims')
        for c in rule['claims']:
            require(c.get('kind') in ('observation', 'inference', 'speculation'), 'Invalid claim kind')
            require(nonempty(c.get('text')) and type(c.get('critical')) is bool, 'Claim text/critical required')
            require(isinstance(c.get('evidence'), list), 'Claim evidence list required')
            for e in c['evidence']:
                require(nonempty(e.get('source')) and nonempty(e.get('quote')) and
                        e.get('stance') in ('supports', 'contradicts'), 'Invalid evidence reference')
        require(isinstance(rule.get('assessments'), dict), 'Assessments required')
        for dim in WEIGHTS.keys() - {'evidence'}:
            a = rule['assessments'].get(dim, {})
            require(type(a.get('score')) is int and 0 <= a['score'] <= 4 and
                    nonempty(a.get('rationale')) and isinstance(a.get('claims'), list),
                    f'Invalid assessment: {dim}')
        for key in ('risks', 'uncertainties', 'falsification_tests'):
            require(isinstance(rule.get(key), list) and rule[key] and all(nonempty(x) for x in rule[key]),
                    f'{key} required')
        action = rule.get('next_action', {})
        require(nonempty(action.get('description')) and action.get('scope') in ('local', 'consequential'),
                'Next action requires description and scope')
    return data, sources, sha(raw)


def evaluate(rule, sources, sensitivity=True):
    matches = sorted(sid for sid, s in sources.items() if s['status'] == 'ok' and
                     any(t.casefold() in s['text'].casefold() for t in rule['triggers']))
    claims, flags, supporting = [], [], set()
    for c in rule['claims']:
        checked = []
        for e in c['evidence']:
            s = sources.get(e['source'])
            valid = bool(s and s['status'] == 'ok' and e['quote'] in s['text'])
            checked.append(dict(e, valid=valid, line=(s['text'][:s['text'].index(e['quote'])].count('\n') + 1) if valid else None))
            if not valid:
                flags.append(f'{c["id"]}: missing source or quote mismatch: {e["source"]}')
        support = [e['source'] for e in checked if e['valid'] and e['stance'] == 'supports']
        counter = [e['source'] for e in checked if e['valid'] and e['stance'] == 'contradicts']
        status = 'contradicted' if counter else ('traceable' if support and c['kind'] != 'speculation' else 'unsupported')
        if status != 'traceable':
            flags.append(f'{c["id"]}: {status} {c["kind"]}')
        if status == 'traceable':
            supporting.update(support)
        claims.append(dict(c, evidence=checked, status=status))
    by_id = {c['id']: c for c in claims}
    # Deduplicate copied text even if the operator supplies different publisher labels.
    hashes = {sources[s]['sha256'] for s in supporting}
    groups = {sources[s]['independence_group'] for s in supporting}
    independent = min(len(hashes), len(groups))
    traceable = sum(c['status'] == 'traceable' for c in claims)
    evidence_score = 0 if not traceable else (1 if independent < 2 else (4 if traceable >= 3 else 3))
    evidence_score = min(evidence_score, min((sources[s]['quality'] for s in supporting), default=0))
    scores = {'evidence': evidence_score}
    for dim, a in rule['assessments'].items():
        if dim not in WEIGHTS or dim == 'evidence':
            continue
        backed = bool(a['claims']) and all(cid in by_id and by_id[cid]['status'] == 'traceable' for cid in a['claims'])
        scores[dim] = a['score'] if backed else 0
        if not backed:
            flags.append(f'{dim}: unsupported assessment; effective score 0')
    score = sum(WEIGHTS[d] * scores[d] / 4 for d in WEIGHTS)
    blockers = []
    if not matches:
        blockers.append('No source matches the opportunity rule')
    if independent < 2:
        blockers.append('Fewer than two independent, nonduplicate supporting sources')
    if not any(c['critical'] for c in claims):
        blockers.append('No critical claim declared')
    if any(c['critical'] and c['status'] != 'traceable' for c in claims):
        blockers.append('Critical claim unsupported or contradicted')
    if any(c['critical'] and any(not e['valid'] for e in c['evidence']) for c in claims):
        blockers.append('Invalid reference on a critical claim')
    if any(c['status'] == 'contradicted' for c in claims):
        blockers.append('Unresolved contradictory evidence')
    if score < 60:
        blockers.append('Weighted score below 60/100')
    fixture = any(sources[s]['fixture'] for s in supporting | set(matches))
    decision = 'abstain' if blockers else ('fixture_shortlist' if fixture else 'shortlist')
    leave_one_out = []
    if sensitivity and not blockers:
        for sid in sorted(supporting):
            reduced = {k: dict(v, status='missing') if k == sid else v for k, v in sources.items()}
            weakened = evaluate(rule, reduced, sensitivity=False)
            leave_one_out.append(dict(removed_source=sid, score=weakened['score'],
                                      decision=weakened['decision'], blockers=weakened['challenge']['blockers']))
        if any(x['decision'] == 'abstain' for x in leave_one_out):
            flags.append('Source-removal challenge: shortlist depends on individual sources; seek corroboration')
    return dict(rule, matched_sources=matches, origin='operator-authored rule matched against local sources',
                claims=claims, scores=scores, score=score, independent_support_count=independent,
                decision=decision, fixture=fixture,
                challenge=dict(flags=flags, blockers=blockers, leave_one_source_out=leave_one_out,
                               counterevidence=[c['id'] for c in claims if c['status'] == 'contradicted'],
                               falsification_tests=rule['falsification_tests'],
                               verdict='weakened/abstain' if blockers else 'provisional; semantic review still required'))


def analyse(path, at=None):
    data, sources, input_hash = ingest(path)
    candidates = sorted((evaluate(r, sources) for r in data['opportunity_rules']),
                        key=lambda c: (-c['score'], c['id']))
    for rank, c in enumerate(candidates, 1):
        c['rank'] = rank
    result = dict(schema_version=1, agent='KI-01: SCOUT', version=VERSION, timestamp=timestamp(at),
                  question=data['question'], input_sha256=input_hash, inputs=data,
                  sources=list(sources.values()),
                  source_sha256={p.name: sha(p.read_bytes()) for p in sorted(Path(__file__).parent.glob('*.py'))},
                  rubric=dict(weights=WEIGHTS, threshold=60),
                  candidates=candidates, limitations=LIMITATIONS)
    result['run_id'] = sha(encoded(result))
    return result


def render(result):
    lines = ['# KI-01: SCOUT research report', '', f'Timestamp (UTC): {result["timestamp"]}',
             f'Run: `{result["run_id"]}`', '', f'Question: {result["question"]}', '',
             '**OFFLINE RUN. Fixture-labelled material is synthetic example evidence, not real research.**', '',
             'Scores rank investigation priorities, not probability of success. Shortlists remain provisional.', '',
             '| Rank | Opportunity | Score / 100 | Decision |', '| --- | --- | --- | --- |']
    for c in result['candidates']:
        lines.append(f'| {c["rank"]} | {c["id"]}: {c["title"]} | {c["score"]:g} | {c["decision"]} |')
    for c in result['candidates']:
        lines += ['', f'## {c["id"]}: {c["title"]}', '', f'Category: {c["category"]}; fixture: {c["fixture"]}.',
                  f'Hypothesis (operator supplied): {c["hypothesis"]}',
                  f'Matched source IDs: {", ".join(c["matched_sources"]) or "none"}', '', '### Claims and provenance', '']
        for claim in c['claims']:
            lines += [f'- {claim["id"]} [{claim["kind"]}; {claim["status"]}; critical={claim["critical"]}]: {claim["text"]}']
            for e in claim['evidence']:
                lines.append(f'  - {e["source"]} ({e["stance"]}, quote verified={e["valid"]}, line={e["line"]}): {json.dumps(e["quote"], ensure_ascii=False)}')
        lines += ['', '### Evaluation', '', f'Effective scores (0–4): {json.dumps(c["scores"], sort_keys=True)}.']
        for d, a in sorted(c['assessments'].items()):
            lines.append(f'- {d}: proposed {a["score"]}; {a["rationale"]}; claim IDs: {a["claims"]}')
        lines += ['', '### Challenge/review', '', c['challenge']['verdict']]
        for key in ('flags', 'blockers', 'falsification_tests'):
            lines += [f'- {key}: {x}' for x in c['challenge'][key]]
        for audit in c['challenge']['leave_one_source_out']:
            lines.append(f'- Remove source {audit["removed_source"]}: score {audit["score"]:g}, {audit["decision"]}; {audit["blockers"]}')
        lines += ['- Risk: ' + x for x in c['risks']]
        lines += ['- Uncertainty: ' + x for x in c['uncertainties']]
        lines += ['', f'Proposed next action ({c["next_action"]["scope"]}): {c["next_action"]["description"]}',
                  ('Kai selection is blocked by abstention.' if c['decision'] == 'abstain' else 'Kai selection is pending; Obe approval is separate.') + ' No action has been executed.']
    lines += ['', '## Source register', '']
    for s in result['sources']:
        lines += [f'- **{s["id"]}**: {s["title"]}; publisher: {s["publisher"]}; independence group: {s["independence_group"]};',
                  f'  locator: {s["locator"]}; snapshot: `{s["path"]}`; accessed: {s["accessed_at"]};',
                  f'  fixture={s["fixture"]}; status={s["status"]}; quality={s["quality"]}/4 ({s["quality_rationale"]}); SHA-256: `{s["sha256"]}`.']
    lines += ['', '## Limitations', ''] + ['- ' + x for x in result['limitations']]
    lines += ['', '## Reproduce', '', 'Use the dossier and source snapshots in inputs/ with the same SCOUT version.',
              '```sh', f'python3 -m scout run --input PATH_TO_RUN/inputs/dossier.json --output work/scout-reproduced --timestamp {result["timestamp"]}',
              'python3 -m scout verify PATH_TO_RUN work/scout-reproduced', '```', '']
    return '\n'.join(lines)


def run(path, output, at=None):
    result = analyse(path, at)
    out = Path(output)
    # Exclusive directory creation avoids silently replacing evidence or review history.
    out.mkdir(parents=True, exist_ok=False)
    (out / 'inputs').mkdir()
    (out / 'inputs/dossier.json').write_bytes(Path(path).read_bytes())
    for s in result['sources']:
        if s['status'] == 'ok':
            target = out / 'inputs' / s['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(s['text'].encode('utf-8'))
    (out / 'research.json').write_bytes(encoded(result))
    (out / 'report.md').write_text(render(result), encoding='utf-8')
    queue = dict(schema_version=1, run_id=result['run_id'], events=[], items=[
        dict(candidate=c['id'], decision=c['decision'], action=c['next_action'], fixture=c['fixture'],
             kai='pending' if c['decision'] != 'abstain' else 'blocked', obe='pending') for c in result['candidates']])
    (out / 'queue.json').write_bytes(encoded(queue))
    manifest = {str(p.relative_to(out)): sha(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file()}
    # Review commands emit new files, never mutate these frozen artifacts.
    (out / 'manifest.json').write_bytes(encoded(manifest))
    return result


def verify(root):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_bytes())
    for name, digest in manifest.items():
        target = (root / name).resolve()
        require(target.is_relative_to(root.resolve()), 'Invalid manifest path')
        require(sha(target.read_bytes()) == digest, f'Artifact changed: {name}')
    result = json.loads((root / 'research.json').read_bytes())
    require(analyse(root / 'inputs/dossier.json', result['timestamp']) == result, 'Research does not reproduce')
    require((root / 'report.md').read_text(encoding='utf-8') == render(result), 'Report differs')
    return result
