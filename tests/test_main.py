# -*- coding: utf-8 -*-
from eralchemy.main import all_to_intermediary, get_output_mode, intermediary_to_schema,\
    intermediary_to_dot, intermediary_to_markdown
from tests.common import Base, check_intermediary_representation_missing_excluded, check_intermediary_representation_simple_table, create_db, markdown

import pytest


def test_all_to_intermediary_base():
    tables, relationships = all_to_intermediary(Base)
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_base_exclude():
    tables, relationships = all_to_intermediary(Base, exclude='exclude')
    check_intermediary_representation_missing_excluded(tables, relationships)


def test_all_to_intermediary_db():
    db_uri = create_db()
    tables, relationships = all_to_intermediary(db_uri)
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_db_exclude():
    db_uri = create_db()
    tables, relationships = all_to_intermediary(db_uri, exclude='exclude')
    check_intermediary_representation_missing_excluded(tables, relationships)


def test_all_to_intermediary_markdown():
    tables, relationships = all_to_intermediary(markdown.split('\n'))
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_markdown_exclude():
    tables, relationships = all_to_intermediary(markdown.split('\n'), exclude='exclude')
    check_intermediary_representation_missing_excluded(tables, relationships)


def test_all_to_intermediary_fails():
    with pytest.raises(ValueError):
        all_to_intermediary('plop')


def test_get_output_mode():
    assert get_output_mode('hello.png', 'auto') == intermediary_to_schema
    assert get_output_mode('hello.er', 'auto') == intermediary_to_markdown
    assert get_output_mode('hello.dot', 'auto') == intermediary_to_dot

    assert get_output_mode('anything', 'graph') == intermediary_to_schema
    assert get_output_mode('anything', 'dot') == intermediary_to_dot
    assert get_output_mode('anything', 'er') == intermediary_to_markdown

    with pytest.raises(ValueError):
        get_output_mode('anything', 'mode')
