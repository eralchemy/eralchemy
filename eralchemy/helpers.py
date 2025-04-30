from __future__ import annotations

import base64
import string
import sys
from argparse import Namespace
from typing import Any
from zlib import compress

# from https://github.com/dougn/python-plantuml/blob/master/plantuml.py
plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + "-_"
base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
b64_to_plantuml = bytes.maketrans(
    base64_alphabet.encode("utf-8"), plantuml_alphabet.encode("utf-8")
)


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


def plantuml_convert(puml_markup):
    zlibbed_str = compress(puml_markup.encode("utf-8"))
    compressed_string = zlibbed_str[2:-4]
    markup_encoded = base64.b64encode(compressed_string).translate(b64_to_plantuml).decode("utf-8")
    return markup_encoded
