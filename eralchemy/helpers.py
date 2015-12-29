import sys


# from https://github.com/mitsuhiko/flask/blob/master/scripts/make-release.py L92
def fail(message, *args):
    print >> sys.stderr, 'Error:', message % args
    sys.exit(1)


def check_args(args):
    """Checks that the args are coherant."""
    if args.v:
        if args.i is not None or \
           args.o is not None or \
           args.s is not None or \
           args.x is not None:
            fail('Cannot show the version number with another command.')
        return
    if args.i is None:
        fail('Cannot draw ER diagram of no database.')
    if args.o is None:
        fail('Cannot draw ER diagram with no output file.')
