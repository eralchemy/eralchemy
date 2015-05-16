# -*- coding: utf-8 -*-
from common import parent_id, parent_name, child_id, child_parent_id, relation, child, parent
from eralchemy.main import _intermediary_to_dot
import dot_parser
from eralchemy.cst import GRAPH_BEGINNING

import re
import pytest

GRAPH_LAYOUT = GRAPH_BEGINNING + "%s }"
column_re = re.compile('\\<TR\\>\\<TD\\ ALIGN\\=\\"LEFT\\"\\>(.*)\\<\\/TD\\>\\<\\/TR\\>')
header_re = re.compile('\\<TR\\>\\<TD\\>\\<B\\>\\<FONT\\ POINT\\-SIZE\\=\\"16\\"\\>(.*)'
                       '\\<\\/FONT\\>\\<\\/B\\>\\<\\/TD\\>\\<\\/TR\\>')
column_inside = re.compile(
    '(?P<key_opening>.*)\\<FONT\\>(?P<name>.*)\\<\\/FONT\\>'
    '(?P<key_closing>.*)\\<FONT\\>\\ \\[(?P<type>.*)\\]\\<\\/FONT\\>'
)


def assert_is_dot_format(dot):
    assert dot_parser.parse_dot_data(dot) is not None


def test_all_to_dot():
    tables = [child, parent]
    relations = [relation]
    output = _intermediary_to_dot(tables, relations)
    assert_is_dot_format(output)
    for element in relations + tables:
        assert element.to_dot() in output


def assert_column_well_rendered_to_dot(col):
    col_no_table = column_re.match(col.to_dot()).groups()
    assert len(col_no_table) == 1
    col_parsed = column_inside.match(col_no_table[0])
    assert col_parsed.group('key_opening') == ('<u>' if col.is_key else '')
    assert col_parsed.group('name') == col.name
    assert col_parsed.group('key_closing') == ('</u>' if col.is_key else '')
    assert col_parsed.group('type') == col.type


def test_column_is_dot_format():
    assert_column_well_rendered_to_dot(parent_id)
    assert_column_well_rendered_to_dot(parent_name)
    assert_column_well_rendered_to_dot(child_id)
    assert_column_well_rendered_to_dot(child_parent_id)


def test_relation():
    relation_re = re.compile(
        '\\"(?P<l_name>.+)\\"\\ \\-\\-\\ \\"(?P<r_name>.+)\\"\\ '
        '\\[taillabel\\=\\<\\<FONT\\>(?P<l_card>.+)\\<\\/FONT\\>\\>'
        '\\,headlabel\\=\\<\\<FONT\\>(?P<r_card>.+)\\<\\/FONT\\>\\>\\]\\;')
    dot = relation.to_dot()
    r = relation_re.match(dot)
    assert r.group('l_name') == 'child'
    assert r.group('r_name') == 'parent'
    assert r.group('l_card') == '{0,1}'
    assert r.group('r_card') == '0..N'


def assert_table_well_rendered_to_dot(table):
    matchs = header_re.match(table.header_dot).groups()
    assert len(matchs) == 1
    assert matchs[0] == table.name
    table_dot = table.to_dot()
    for col in table.columns:
        assert col.to_dot() in table_dot


def test_table():
    assert_table_well_rendered_to_dot(child)
    assert_table_well_rendered_to_dot(parent)