#!/usr/bin/env python3
"""
Run  project tests.

This script mostly useful for running tests in single file.

"""

import os
import sys
import argparse
import subprocess
import pathlib


def get_cover_package(path):
    if ':' in path:
        path = path[:path.index(':')]

    base = pathlib.Path(__file__).parents[1].resolve()
    path = pathlib.Path(path).resolve()
    path = path.relative_to(base)
    if len(path.parts) > 1:
        return '.'.join(path.parts[:2])
    else:
        return path.parts[0]


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
        '--with-coverage',
    ] + [
        '--cover-package=%s' % package
        for package in set(map(get_cover_package, args.paths))
    ] + args.paths

    if args.profile:
        cmd = [
            'bin/kernprof',
            '--line-by-line',
            '--builtin',
            '--outfile=/dev/null',
            '--view',
        ] + cmd

    coverage_file = pathlib.Path(__file__).parents[1].resolve() / '.coverage'
    if coverage_file.exists():
        os.unlink(str(coverage_file))

    sys.exit(subprocess.call(cmd))


if __name__ == '__main__':
    main()
