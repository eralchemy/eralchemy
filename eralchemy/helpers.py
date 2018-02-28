from __future__ import print_function
import sys


# from https://github.com/mitsuhiko/flask/blob/master/scripts/make-release.py L92
def fail(message, *args):
    print('Error:', message % args, file=sys.stderr)
    sys.exit(1)


def check_args(args):
    """Checks that the args are coherent."""
    check_args_has_attributes(args)
    if args.uri is None:
        fail('Cannot draw ER diagram of no database.')
    if args.output is None:
        fail('Cannot draw ER diagram with no output file.')


def check_args_has_attributes(args):
    check_args_has_attribute(args, 'uri')
    check_args_has_attribute(args, 'output')
    check_args_has_attribute(args, 'include_tables')
    check_args_has_attribute(args, 'include_columns')
    check_args_has_attribute(args, 'exclude_tables')
    check_args_has_attribute(args, 'exclude_columns')
    check_args_has_attribute(args, 's')


def check_args_has_attribute(args, name):
    if not hasattr(args, name):
        raise Exception('{} should be set'.format(name))
