#!/usr/bin/env python
"""
Run  project tests.

This script mostly useful for running tests in single file.

"""

import sys
import argparse
import subprocess


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+', help='paths to test files')
    parser.add_argument(
        '--fast', action='store_true', default=False,
        help='run tests with akllt.settings.fasttests settings',
    )
    parser.add_argument(
        '--profile', action='store_true', default=False,
        help='run tests with line profiler',
    )
    args = parser.parse_args(args)

    if args.fast:
        settings = 'akllt.settings.fasttests'
    else:
        settings = 'akllt.settings.testing'

    cmd = [
        'bin/django', 'test',
        '--settings=%s' % settings,
        '--nocapture',
        '--nologcapture',
        '--doctest-tests',
        '--noinput',
    ] + args.paths

    if args.profile:
        cmd = [
            'bin/kernprof',
            '--line-by-line',
            '--builtin',
            '--outfile=/dev/null',
            '--view',
        ] + cmd

    sys.exit(subprocess.call(cmd))


if __name__ == '__main__':
    main()
