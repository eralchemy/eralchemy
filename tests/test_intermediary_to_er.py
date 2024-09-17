import re

from eralchemy.main import _intermediary_to_markdown
from tests.common import (
    child,
    child_id,
    child_parent_id,
    parent,
    parent_id,
    parent_name,
    relation,
)

column_re = re.compile(r'(?P<key>\*?)(?P<name>[^*].+) \{label:"(?P<type>.+)"\}')


def test_all_to_er():
    tables = [child, parent]
    relations = [relation]
    output = _intermediary_to_markdown(tables, relations)
    for element in relations + tables:
        assert element.to_markdown() in output


def assert_column_well_rendered_to_er(col):
    col_er = col.to_markdown().strip()
    col_parsed = column_re.match(col_er)
    assert col_parsed.group("key") == ("*" if col.is_key else "")
    assert col_parsed.group("name") == col.name
    assert col_parsed.group("type") == col.type


def test_column_to_er():
    assert_column_well_rendered_to_er(parent_id)
    assert_column_well_rendered_to_er(parent_name)
    assert_column_well_rendered_to_er(child_id)
    assert_column_well_rendered_to_er(child_parent_id)


def test_relation():
    assert relation.to_markdown() in [
        'parent."id" *--? child."parent_id"',
        'child."parent_id" *--? parent."id"',
    ]


def assert_table_well_rendered_to_er(table):
    assert table.header_markdown == "[" + table.name + "]"
    table_er = table.to_markdown()
    for col in table.columns:
        assert col.to_markdown() in table_er


def test_table():
    assert_table_well_rendered_to_er(child)
    assert_table_well_rendered_to_er(parent)
