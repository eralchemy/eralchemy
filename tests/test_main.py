# -*- coding: utf-8 -*-
from eralchemy.main import all_to_intermediary, get_output_mode, intermediary_to_schema, \
    intermediary_to_dot, intermediary_to_markdown, filter_resources
from tests.common import Base, check_tables_relationships, check_intermediary_representation_simple_table, \
    markdown, relationships, tables, check_intermediary_representation_simple_all_table, check_tables_columns, \
    check_filter

import pytest


def test_all_to_intermediary_base():
    tables, relationships = all_to_intermediary(Base)
    check_intermediary_representation_simple_all_table(tables, relationships)


def test_all_to_intermediary_db_sqlite(sqlite_db):
    tables, relationships = all_to_intermediary(sqlite_db)
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_db(postgresql_db):
    tables, relationships = all_to_intermediary(postgresql_db)
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_markdown():
    tables, relationships = all_to_intermediary(markdown.split('\n'))
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_fails():
    with pytest.raises(ValueError):
        all_to_intermediary('plop')


def test_filter_no_include_no_exclude():
    actual_tables, actual_relationships = filter_resources(tables, relationships)
    check_filter(actual_tables, actual_relationships)


def test_filter_include_tables():
    actual_tables, actual_relationships = filter_resources(tables, relationships, include_tables=['parent', 'child'])
    check_tables_relationships(actual_tables, actual_relationships)


def test_filter_exclude_tables():
    actual_tables, actual_relationships = filter_resources(tables, relationships, exclude_tables=['exclude'])
    check_tables_relationships(actual_tables, actual_relationships)


def test_filter_include_columns():
    actual_tables, actual_relationships = filter_resources(tables, relationships, include_columns=['id'])
    check_tables_columns(actual_tables, id_is_included=True)


def test_filter_exclude_columns():
    actual_tables, actual_relationships = filter_resources(tables, relationships, exclude_columns=['id'])
    check_tables_columns(actual_tables, id_is_included=False)


def test_get_output_mode():
    assert get_output_mode('hello.png', 'auto') == intermediary_to_schema
    assert get_output_mode('hello.er', 'auto') == intermediary_to_markdown
    assert get_output_mode('hello.dot', 'auto') == intermediary_to_dot

    assert get_output_mode('anything', 'graph') == intermediary_to_schema
    assert get_output_mode('anything', 'dot') == intermediary_to_dot
    assert get_output_mode('anything', 'er') == intermediary_to_markdown

    with pytest.raises(ValueError):
        get_output_mode('anything', 'mode')


def test_import_render_er():
    from eralchemy import render_er  # noqa: F401
