import argparse
from pathlib import Path
from .experiment import ROOT, run


def main():
    parser = argparse.ArgumentParser(description='PROMETHEUS offline supervised experimental prototype')
    parser.add_argument('--output', type=Path, required=True, help='New or empty evidence directory')
    parser.add_argument('--protocol', type=Path, default=ROOT / 'protocol.json')
    args = parser.parse_args()
    try:
        run(args.output, args.protocol)
    except ValueError as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
