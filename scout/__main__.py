"""Command-line interface for KI-01: SCOUT."""
import argparse
import json
import sys

from .engine import encoded, require, run, verify
from .review import review


def main(argv=None):
    parser = argparse.ArgumentParser(description='SCOUT: offline evidence research; no external actions.')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('run', help='Ingest dossier and write a fresh evidence bundle')
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True, help='New directory; existing directories are refused')
    p.add_argument('--timestamp', help='Timezone-aware ISO time; pin for exact reproduction')
    p = sub.add_parser('verify', help='Check hashes, replay research and optionally compare runs')
    p.add_argument('reference')
    p.add_argument('reproduced', nargs='?')
    p = sub.add_parser('review', help='Record a local attestation into a new queue file; executes nothing')
    for name in ('run', 'queue', 'output', 'candidate', 'actor', 'decision', 'note'):
        p.add_argument('--' + name, required=True)
    p.add_argument('--timestamp')
    args = vars(parser.parse_args(argv))
    command = args.pop('command')
    try:
        if command == 'run':
            result = run(args['input'], args['output'], args['timestamp'])
            print(json.dumps(dict(run_id=result['run_id'], candidates=len(result['candidates']), output=args['output'])))
        elif command == 'verify':
            reference = verify(args['reference'])
            if args['reproduced']:
                require(encoded(reference) == encoded(verify(args['reproduced'])), 'Runs differ (including timestamp/inputs)')
            print('PASS: hashes, evidence, scores, decisions and report reproduce exactly')
        else:
            print(json.dumps(review(args['run'], args['queue'], args['output'], args['candidate'],
                                    args['actor'], args['decision'], args['note'], args['timestamp'])))
    except (ValueError, OSError, KeyError, TypeError) as e:
        print(f'SCOUT error: {e}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
