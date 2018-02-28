import pytest

from eralchemy.helpers import check_args
from eralchemy.main import get_argparser


def parse_test(lst_arguments):
    parser = get_argparser()
    args = parser.parse_args(lst_arguments)
    check_args(args)


def test_version():
    with pytest.raises(SystemExit) as se:
        parse_test(['-v'])
    assert se.value.code == 0


def test_normal():
    parse_test('sqlite:///relative/path/to/db.db erd_from_sqlite.pdf'.split(' '))
