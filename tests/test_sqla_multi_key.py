from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import declarative_base

from eralchemy.models import Relation, Table
from eralchemy.sqla import (
    declarative_to_intermediary,
)


def test_columns_parent():
    Base = declarative_base()

    class Parent(Base):
        __tablename__ = "parent"
        id = Column(String(), primary_key=True)

    class Child(Base):
        __tablename__ = "child"
        id = Column(String(), primary_key=True)
        parent = Column(String(), ForeignKey(Parent.id), primary_key=True)

    tables, relationships = declarative_to_intermediary(Base)

    assert len(tables) == 2
    assert len(relationships) == 1
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relationships)
    relation = relationships[0]
    assert relation.right_cardinality == "*"
    assert relation.left_cardinality == "1"


def test_columns_one_to_many_parent():
    Base = declarative_base()

    class Parent(Base):
        __tablename__ = "parent"
        id = Column(String(), primary_key=True)

    class Child(Base):
        __tablename__ = "child"
        id = Column(String(), primary_key=True)
        parent = Column(String(), ForeignKey(Parent.id))

    tables, relationships = declarative_to_intermediary(Base)

    assert len(tables) == 2
    assert len(relationships) == 1
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relationships)
    relation = relationships[0]
    assert relation.right_cardinality == "*"
    assert relation.left_cardinality == "?"


def test_columns_one_to_one_parent():
    Base = declarative_base()

    class Parent(Base):
        __tablename__ = "parent"
        id = Column(String(), primary_key=True)

    class Child(Base):
        __tablename__ = "child"
        id = Column(String(), ForeignKey(Parent.id), primary_key=True)

    tables, relationships = declarative_to_intermediary(Base)

    assert len(tables) == 2
    assert len(relationships) == 1
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relationships)
    relation = relationships[0]
    assert relation.right_cardinality == "1"
    assert relation.left_cardinality == "1"


def test_compound_one_to_one_parent():
    Base = declarative_base()

    class Parent(Base):
        __tablename__ = "parent"
        id = Column(String(), primary_key=True)
        id2 = Column(String(), primary_key=True)

    class Child(Base):
        __tablename__ = "child"
        id = Column(String(), ForeignKey(Parent.id), primary_key=True)
        id2 = Column(String(), ForeignKey(Parent.id2), primary_key=True)

    tables, relationships = declarative_to_intermediary(Base)

    assert len(tables) == 2
    assert len(relationships) == 2
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relationships)
    for relation in relationships:
        assert relation.right_cardinality == "1"
        assert relation.left_cardinality == "1"
