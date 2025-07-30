#!/usr/bin/env python3

"""
Utility
"""

from argparse import ArgumentParser
import os
from pathlib import Path
PROJECT_ROOT = Path(__file__).absolute().parents[1]
import sys; sys.path.append(str(PROJECT_ROOT))  # noqa


class Utility:
    def __init__(self, *args, **kwargs):
        self.input = kwargs['input']
        self.output = kwargs['output']
        self.switch = kwargs['switch']

        return

    def run(self):
        """
        Implement the utility's main functionality here
        """

        print(self.input)
        print(self.output)
        print(self.switch)

        return 0


def main():
    description = 'Utility'
    parser = ArgumentParser(description=description)
    parser.add_argument('-i', '--input', dest='input', required=True)
    parser.add_argument('-o', '--output', dest='output', required=True)
    parser.add_argument('-s', '--switch', dest='switch')
    
    args = parser.parse_args()
    input, output, switch = args.input, args.output, args.switch

    utility = Utility(input=input, output=output, switch=switch)
    try:
        retval = utility.run()
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        retval = 1

        return retval


if __name__ == '__main__':
    retval = main()
    sys.exit(retval)
