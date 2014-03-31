from __future__ import print_function
import sys
import os
import argparse
from ._unparse import roundtrip


def roundtrip_recursive(target):
    if os.path.isfile(target):
        print(target)
        print("=" * len(target))
        roundtrip(target)
        print()
    elif os.path.isdir(target):
        for item in os.listdir(target):
            if item.endswith(".py"):
                roundtrip_recursive(os.path.join(target, item))
    else:
        print(
            "WARNING: skipping '%s', not a file or directory" % target,
            file=sys.stderr
        )


def main(args):
    parser = argparse.ArgumentParser(prog="astunparse")
    parser.add_argument(
        'target',
        nargs='+',
        help="Files or directories to show roundtripped source for"
    )

    arguments = parser.parse_args(args)
    for target in arguments.target:
        roundtrip_recursive(target)


if __name__ == "__main__":
    main(sys.argv[1:])
