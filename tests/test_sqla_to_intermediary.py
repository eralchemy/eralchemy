import re

import pytest

from eralchemy.sqla import (
    column_to_intermediary,
    database_to_intermediary,
    declarative_to_intermediary,
    table_to_intermediary,
)
from tests.common import (
    Base,
    Child,
    Parent,
    Relation,
    Table,
    check_intermediary_representation_simple_all_table,
    check_intermediary_representation_simple_table,
    child,
    child_id,
    child_parent_id,
    exclude_relation,
    parent,
    parent_id,
    parent_name,
    relation,
)


def check_column(column, column_intermediary):
    output = column_to_intermediary(column)
    assert output.name == column_intermediary.name
    assert output.is_key is column_intermediary.is_key
    assert output.type == column_intermediary.type


def test_columns_parent():
    check_column(column=Parent.id, column_intermediary=parent_id)

    check_column(column=Parent.name, column_intermediary=parent_name)


def test_columns_child():
    check_column(column=Child.id, column_intermediary=child_id)

    check_column(column=Child.parent_id, column_intermediary=child_parent_id)


def test_declarative_to_intermediary():
    tables, relationships = declarative_to_intermediary(Base)
    check_intermediary_representation_simple_all_table(tables, relationships)


def table_equals_helper(sqla_table, expected_table):
    table = table_to_intermediary(sqla_table.__table__)
    assert len(table.columns) == len(expected_table.columns)
    assert table.name == expected_table.name
    for col in table.columns:
        assert col in expected_table.columns


def test_tables():
    table_equals_helper(Child, child)
    table_equals_helper(Parent, parent)


@pytest.mark.external_db
def test_database_to_intermediary(pg_db_uri):
    tables, relationships = database_to_intermediary(pg_db_uri)
    check_intermediary_representation_simple_table(tables, relationships)


@pytest.mark.external_db
def test_database_to_intermediary_with_schema(pg_db_uri):
    tables, relationships = database_to_intermediary(pg_db_uri, schema="eralchemy_test")

    assert len(tables) == 3
    assert len(relationships) == 2
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relationships)
    # Not in because different schema.
    assert relation not in relationships
    assert exclude_relation not in relationships


@pytest.mark.external_db
def test_database_to_intermediary_with_multiple_schemas(pg_db_uri):
    tables, relationships = database_to_intermediary(
        pg_db_uri,
        schema="public, eralchemy_test",
    )

    assert len(tables) == 6
    assert len(relationships) == 4
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relationships)
    # Not in because different schema.
    assert relation not in relationships
    assert exclude_relation not in relationships


def test_flask_sqlalchemy():
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    from eralchemy.main import all_to_intermediary

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db = SQLAlchemy(app)
    model = db.Model
    model.metadata = Base.metadata
    tables, relationships = all_to_intermediary(db.Model)
    check_intermediary_representation_simple_all_table(tables, relationships)


@pytest.mark.external_db
def test_table_names_in_relationships(pg_db_uri):
    tables, relationships = database_to_intermediary(pg_db_uri)
    table_names = [t.name for t in tables]

    # Assert column names are table names
    assert all(r.right_table in table_names for r in relationships)
    assert all(r.left_table in table_names for r in relationships)

    # Assert column names match table names
    for r in relationships:
        r_name = table_names[table_names.index(r.right_table)]
        l_name = table_names[table_names.index(r.left_table)]

        # Table name in relationship should *NOT* have a schema
        assert r_name.find(".") == -1
        assert l_name.find(".") == -1


@pytest.mark.external_db
def test_table_names_in_relationships_with_schema(pg_db_uri):
    schema_name = "test"
    matcher = re.compile(rf"{schema_name}\.[\S+]", re.I)
    tables, relationships = database_to_intermediary(pg_db_uri, schema=schema_name)
    table_names = [t.name for t in tables]

    # Assert column names match table names, including schema
    assert all(r.right_table in table_names for r in relationships)
    assert all(r.left_table in table_names for r in relationships)

    # Assert column names match table names, including schema
    for r in relationships:
        r_name = table_names[table_names.index(r.right_col)]
        l_name = table_names[table_names.index(r.left_col)]

        # Table name in relationship *SHOULD* have a schema
        assert re.match(matcher, r_name) is not None
        assert re.match(matcher, l_name) is not None
