from __future__ import annotations

import sys
from argparse import Namespace
from typing import Any


# from https://github.com/mitsuhiko/flask/blob/master/scripts/make-release.py L92
def fail(message: str, *args: Any) -> None:
    print("Error:", message % args, file=sys.stderr)
    sys.exit(1)


def check_args(args: Namespace) -> None:
    """Checks that the args are coherent."""
    check_args_has_attributes(args)
    if args.v:
        non_version_attrs = [v for k, v in args.__dict__.items() if k != "v"]
        if len([v for v in non_version_attrs if v is not None]) != 0:
            print("non_version_attrs", non_version_attrs)
            fail("Cannot show the version number with another command.")
        return
    if args.i is None:
        fail("Cannot draw ER diagram of no database.")
    if args.o is None:
        fail("Cannot draw ER diagram with no output file.")


def check_args_has_attributes(args: Namespace) -> None:
    check_args_has_attribute(args, "i")
    check_args_has_attribute(args, "o")
    check_args_has_attribute(args, "include_tables")
    check_args_has_attribute(args, "include_columns")
    check_args_has_attribute(args, "exclude_tables")
    check_args_has_attribute(args, "exclude_columns")
    check_args_has_attribute(args, "s")


def check_args_has_attribute(args: Namespace, name: str) -> None:
    if not hasattr(args, name):
        raise Exception(f"{name} should be set")
