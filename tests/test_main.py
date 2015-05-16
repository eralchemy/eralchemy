# -*- coding: utf-8 -*-
from eralchemy.main import all_to_intermediary, get_output_mode, intermediary_to_schema,\
    intermediary_to_dot, intermediary_to_markdown
from common import Base, check_intermediary_representation_simple_table, create_db

import pytest


def test_all_to_intermediary():
    tables, relationships = all_to_intermediary(Base)
    check_intermediary_representation_simple_table(tables, relationships)

    db_uri = create_db()
    tables, relationships = all_to_intermediary(db_uri)
    check_intermediary_representation_simple_table(tables, relationships)

    with pytest.raises(ValueError):
        tables, relationships = all_to_intermediary('plop')


def test_get_output_mode():
    assert get_output_mode('hello.png', 'auto') == intermediary_to_schema
    assert get_output_mode('hello.er', 'auto') == intermediary_to_markdown
    assert get_output_mode('hello.dot', 'auto') == intermediary_to_dot

    assert get_output_mode('anything', 'graph') == intermediary_to_schema
    assert get_output_mode('anything', 'dot') == intermediary_to_dot
    assert get_output_mode('anything', 'er') == intermediary_to_markdown

    with pytest.raises(ValueError):
        get_output_mode('anything', 'mode')