# -*- coding: utf-8 -*-

from eralchemy.sqla import column_to_intermediary, declarative_to_intermediary, database_to_intermediary, \
    table_to_intermediary
from tests.common import parent_id, parent_name, child_id, child_parent_id, Parent, Child, Base, \
    child, parent, Relation, Table, relation, exclude_relation, \
    check_intermediary_representation_simple_all_table
from tests.common import check_intermediary_representation_simple_table


def check_column(column, column_intermediary):
    output = column_to_intermediary(column)
    assert output.name == column_intermediary.name
    assert output.is_key is column_intermediary.is_key
    assert output.type == column_intermediary.type


def test_columns_parent():
    check_column(
        column=Parent.id,
        column_intermediary=parent_id
    )

    check_column(
        column=Parent.name,
        column_intermediary=parent_name
    )


def test_columns_child():
    check_column(
        column=Child.id,
        column_intermediary=child_id
    )

    check_column(
        column=Child.parent_id,
        column_intermediary=child_parent_id
    )


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


def test_database_to_intermediary(postgresql_db):
    tables, relationships = database_to_intermediary(postgresql_db)
    check_intermediary_representation_simple_table(tables, relationships)


def test_database_to_intermediary_with_schema(postgresql_db):

    tables, relationships = database_to_intermediary(postgresql_db, schema='test')

    assert len(tables) == 3
    assert len(relationships) == 2
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relationships)
    # Not in because different schema.
    assert relation not in relationships
    assert exclude_relation not in relationships


def test_flask_sqlalchemy():
    from flask_sqlalchemy import SQLAlchemy
    from flask import Flask
    from eralchemy.main import all_to_intermediary
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db = SQLAlchemy(app)
    model = db.Model
    model.metadata = Base.metadata
    tables, relationships = all_to_intermediary(db.Model)
    check_intermediary_representation_simple_all_table(tables, relationships)
