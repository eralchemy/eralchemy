from eralchemy.helpers import check_args
from eralchemy.main import get_argparser


def parse_test(lst_arguments):
    parser = get_argparser()
    args = parser.parse_args(lst_arguments)
    check_args(args)


def test_version():
    parse_test(["-v"])


def test_normal():
    parse_test("-i sqlite:///relative/path/to/db.db -o erd_from_sqlite.pdf".split(" "))
