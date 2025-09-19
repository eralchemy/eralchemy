import pytest
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

from eralchemy.main import (
    all_to_intermediary,
    filter_resources,
    get_output_mode,
    intermediary_to_dot,
    intermediary_to_markdown,
    intermediary_to_mermaid,
    intermediary_to_mermaid_er,
    intermediary_to_schema,
)
from tests.common import (
    Base,
    check_filter,
    check_intermediary_representation_simple_all_table,
    check_intermediary_representation_simple_table,
    check_tables_columns,
    check_tables_relationships,
    markdown,
    relationships,
    tables,
)


def test_all_to_intermediary_base():
    tables, relationships = all_to_intermediary(Base)
    check_intermediary_representation_simple_all_table(tables, relationships)


def test_all_to_intermediary_db_sqlite(sqlite_db_uri):
    tables, relationships = all_to_intermediary(sqlite_db_uri)
    check_intermediary_representation_simple_table(tables, relationships)


@pytest.mark.external_db
def test_all_to_intermediary_db(pg_db_uri):
    tables, relationships = all_to_intermediary(pg_db_uri)
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_markdown():
    tables, relationships = all_to_intermediary(markdown.split("\n"))
    check_intermediary_representation_simple_table(tables, relationships)


def test_all_to_intermediary_fails():
    with pytest.raises(ValueError):
        all_to_intermediary("plop")


def test_filter_no_include_no_exclude():
    actual_tables, actual_relationships = filter_resources(tables, relationships)
    check_filter(actual_tables, actual_relationships)


@pytest.mark.parametrize(
    "include_tables",
    (
        ["parent", "child", "excl"],
        ["^(?!exc)\\w+$"],  # all not starting with excl
        ["parent", "child"],
        ["parent", "^ch.*"],
        ["par.*", "child"],
    ),
)
def test_filter_include_tables(include_tables):
    actual_tables, actual_relationships = filter_resources(
        tables,
        relationships,
        include_tables=include_tables,
    )
    check_tables_relationships(actual_tables, actual_relationships)


@pytest.mark.parametrize(
    "exclude_tables",
    (
        ["ent", "ld", ".*lude"],
        ["par", "ch", "^exclude"],
        ["ar.*", "hild", "exc.*"],
        ["exclude"],
    ),
)
def test_filter_exclude_tables(exclude_tables):
    actual_tables, actual_relationships = filter_resources(
        tables,
        relationships,
        exclude_tables=exclude_tables,
    )
    check_tables_relationships(actual_tables, actual_relationships)


@pytest.mark.parametrize(
    "include_columns",
    (
        ["id"],
        ["id.*", "not_match"],
    ),
)
def test_filter_include_columns(include_columns):
    actual_tables, actual_relationships = filter_resources(
        tables,
        relationships,
        include_columns=include_columns,
    )
    check_tables_columns(actual_tables, id_is_included=True)


@pytest.mark.parametrize(
    "exclude_columns",
    (
        ["id"],
        ["i."],
    ),
)
def test_filter_exclude_columns(exclude_columns):
    actual_tables, actual_relationships = filter_resources(
        tables,
        relationships,
        exclude_columns=exclude_columns,
    )
    check_tables_columns(actual_tables, id_is_included=False)


def test_get_output_mode():
    # access .func for partial
    assert get_output_mode("hello.png", "auto").func == intermediary_to_schema
    assert get_output_mode("hello.er", "auto") == intermediary_to_markdown
    assert get_output_mode("hello.dot", "auto") == intermediary_to_dot
    assert get_output_mode("hello.md", "auto") == intermediary_to_mermaid

    assert get_output_mode("anything", "graph") == intermediary_to_schema
    assert get_output_mode("anything", "dot") == intermediary_to_dot
    assert get_output_mode("anything", "er") == intermediary_to_markdown
    assert get_output_mode("anything", "mermaid") == intermediary_to_mermaid
    assert get_output_mode("anything", "mermaid_er") == intermediary_to_mermaid_er

    with pytest.raises(ValueError):
        get_output_mode("anything", "mode")


def test_import_render_er():
    from eralchemy import render_er  # noqa: F401


@pytest.mark.parametrize(
    "sort_mode, expected_column_order",
    (
        pytest.param(
            None,
            [
                # key columns in alphabetical order first
                "fifth_column",
                "first_column",
                # then non-key columns in alphabetical order
                "fourth_column",
                "second_column",
                "third_column",
            ],
            id="sort_mode=None",
        ),
        pytest.param(
            "alphabetical",
            [
                # key columns in alphabetical order first
                "fifth_column",
                "first_column",
                # then non-key columns in alphabetical order
                "fourth_column",
                "second_column",
                "third_column",
            ],
            id="sort_mode='alphabetical'",
        ),
        pytest.param(
            "original",
            [
                # key columns in original order first
                "first_column",
                "fifth_column",
                # then non-key columns in original order
                "second_column",
                "third_column",
                "fourth_column",
            ],
            id="sort_mode='original'",
        ),
    ),
)
def test_sort_mode(sort_mode, expected_column_order):
    Base = declarative_base()

    class Table(Base):
        __tablename__ = "table"
        first_column = Column(String, primary_key=True)
        second_column = Column(String)
        third_column = Column(String)
        fourth_column = Column(String)
        fifth_column = Column(String, primary_key=True)

    tables, relationships = all_to_intermediary(Base)
    actual_tables, actual_relationships = filter_resources(
        tables,
        relationships,
        sort_mode=sort_mode,
    )

    assert len(actual_tables) == 1
    actual_table = actual_tables[0]
    assert len(actual_table.columns) == len(expected_column_order)

    # The order of columns in `table` and `expected_column_order` should be the same.
    for column_index in range(len(actual_table.columns)):
        assert actual_table.columns[column_index].name == expected_column_order[column_index]
