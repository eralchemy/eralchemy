# -*- coding: utf-8 -*-
from eralchemy.main import all_to_intermediary, get_output_mode, intermediary_to_schema,\
    intermediary_to_dot, intermediary_to_markdown, filter_excludes
from tests.common import Base, check_excluded_tables_relationships, \
    check_intermediary_representation_simple_table, create_db, markdown, relationships,\
    tables, check_intermediary_representation_simple_all_table

import pytest


def test_all_to_intermediary_base():
    tables, relationships = all_to_intermediary(Base)
    check_intermediary_representation_simple_all_table(tables, relationships)


def test_all_to_intermediary_db_sqlite():
    db_uri = create_db(db_uri="sqlite:///test.db", use_sqlite=True)
    tables, relationships = all_to_intermediary(db_uri)
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_db():
    db_uri = create_db()
    tables, relationships = all_to_intermediary(db_uri)
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_markdown():
    tables, relationships = all_to_intermediary(markdown.split('\n'))
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_fails():
    with pytest.raises(ValueError):
        all_to_intermediary('plop')


def test_filter_excludes_no_excludes():
    actual_tables, actual_relationships = filter_excludes(tables, relationships, None)
    assert actual_tables == tables
    assert actual_relationships == relationships


def test_filter_excludes_specified():
    actual_tables, actual_relationships = filter_excludes(tables, relationships, 'exclude')
    check_excluded_tables_relationships(actual_tables, actual_relationships)


def test_get_output_mode():
    assert get_output_mode('hello.png', 'auto') == intermediary_to_schema
    assert get_output_mode('hello.er', 'auto') == intermediary_to_markdown
    assert get_output_mode('hello.dot', 'auto') == intermediary_to_dot

    assert get_output_mode('anything', 'graph') == intermediary_to_schema
    assert get_output_mode('anything', 'dot') == intermediary_to_dot
    assert get_output_mode('anything', 'er') == intermediary_to_markdown

    with pytest.raises(ValueError):
        get_output_mode('anything', 'mode')
