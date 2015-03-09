#!/usr/bin/env python3
"""
Run  project tests.

This script mostly useful for running tests in single file.

"""

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


def get_paths(paths):
    if paths:
        for path in paths:
            if ':' in path:
                path = path[:path.index(':')]
            yield path
    else:
        yield 'akllt'


def run_tests(args):
    coverage = not args.nocoverage

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
        coverage = False
        cmd = [
            'bin/kernprof',
            '--line-by-line',
            '--builtin',
            '--outfile=/dev/null',
            '--view',
        ] + cmd
    else:
        coverage_modules = list(set(map(get_cover_package, args.paths)))
        subprocess.call(['bin/coverage', 'erase'])
        cmd = [
            'bin/coverage', 'run',
            '--source=%s' % ','.join(coverage_modules),
        ] + cmd

    retcode = subprocess.call(cmd)

    if retcode == 0 and coverage:
        # Also see .coveragerc
        subprocess.call(['bin/coverage', 'report', '--show-missing'])

    return retcode


def run_flake8(args):
    cmd = [
        'bin/flake8',
        '--exclude=migrations',
        '--ignore=E501',
    ] + list(get_paths(args.paths))
    return subprocess.call(cmd)


def run_pylint(args):
    cmd = [
        'bin/pylint',
        '--msg-template="%s"' % (
            '{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}',
        )
    ] + list(get_paths(args.paths))
    return subprocess.call(cmd)


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
    parser.add_argument(
        '--nocoverage', action='store_true', default=False,
        help='run tests without test coverage report',
    )
    args = parser.parse_args(args)

    sys.exit(
        run_tests(args) == 0 and
        run_flake8(args) == 0 and
        run_pylint(args) == 0
    )


if __name__ == '__main__':
    main()
