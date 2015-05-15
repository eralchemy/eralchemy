# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
from eralchemy.sqla import table_to_intermediary, column_to_intermediary, declarative_to_intermediary
from eralchemy.models import Column as ERColumn, Table, Relation
import pytest


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey('parent.id'))
    parent = relationship('Parent', backref='children')



def transform_column_helper(column, name_expected, typ, is_key=False):
    output = column_to_intermediary(column)
    assert output.name == name_expected
    assert output.is_key is is_key
    assert output.type == typ


def test_columns_parent():
    transform_column_helper(
        column=Parent.id,
        name_expected='id',
        typ=u'INTEGER',
        is_key=True
    )

    transform_column_helper(
        column=Parent.name,
        name_expected='name',
        typ=u'VARCHAR(255)'
    )


def test_columns_child():
    transform_column_helper(
        column=Child.id,
        name_expected='id',
        typ=u'INTEGER',
        is_key=True
    )

    transform_column_helper(
        column=Child.parent_id,
        name_expected='parent_id',
        typ=u'INTEGER'
    )


def test_declarative_to_intermediary():
    tables, relationship = declarative_to_intermediary(Base)
    assert len(tables) == 2
    assert len(relationship) == 1
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relationship)


def test_relation():
    pass