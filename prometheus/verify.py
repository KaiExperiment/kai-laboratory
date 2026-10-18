"""Compare two independently executed evidence bundles, excluding timing/host data."""
import argparse
import json
from pathlib import Path


def verify(reference, reproduced):
    for name in ['reviews.json','selection.json','summary.json','exploration.json','validation.json']:
        a,b = (json.loads((Path(root)/name).read_text()) for root in [reference,reproduced])
        if name in ['exploration.json','validation.json']:
            a=[{k:v for k,v in r.items() if k!='seconds'} for r in a]
            b=[{k:v for k,v in r.items() if k!='seconds'} for r in b]
        if a != b:
            raise ValueError(f'Scientific evidence differs: {name}')
    a,b = (json.loads((Path(root)/'manifest.json').read_text()) for root in [reference,reproduced])
    for key in ['protocol','protocol_sha256','source_sha256']:
        if a[key] != b[key]:
            raise ValueError(f'Manifest differs: {key}')
    print('PASS: protocol, source hashes, all tours, metrics, reviews and decisions match exactly; timings and host metadata excluded')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reference')
    parser.add_argument('reproduced')
    args=parser.parse_args()
    verify(args.reference,args.reproduced)
