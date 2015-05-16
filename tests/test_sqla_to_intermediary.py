# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from eralchemy.sqla import column_to_intermediary, declarative_to_intermediary, database_to_intermediary, table_to_intermediary
from eralchemy.models import Table, Relation
from common import parent_id, parent_name, child_id, child_parent_id, relation,\
    Parent, Child, Base,\
    child, parent


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


def check_intermediary_representation_simple_table(tables, relationships):
    assert len(tables) == 2
    assert len(relationships) == 1
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relationships)
    assert relation == relationships[0]


def test_declarative_to_intermediary():
    tables, relationships = declarative_to_intermediary(Base)
    check_intermediary_representation_simple_table(tables, relationships)


def table_equals_helper(sqla_table, expected_table):
    table = table_to_intermediary(sqla_table.__table__)
    assert len(table.columns) == len(expected_table.columns)
    assert table.name == expected_table.name
    for col in table.columns:
        assert col in expected_table.columns


def test_tables():
    table_equals_helper(Child, child)
    table_equals_helper(Parent, parent)


def test_database_to_intermediary():
    DB_URI = "sqlite:///test.db"
    engine = create_engine(DB_URI)
    Base.metadata.create_all(engine)
    tables, relationships = database_to_intermediary(DB_URI)
    check_intermediary_representation_simple_table(tables, relationships)