# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from eralchemy.models import Column as ERColumn, Relation

Base = declarative_base()


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey('parent.id'))
    parent = relationship('Parent', backref='children')



parent_id = ERColumn(
    name='id',
    type=u'INTEGER',
    is_key=True
)

parent_name = ERColumn(
    name='name',
    type=u'VARCHAR(255)',
)

child_id = ERColumn(
    name='id',
    type=u'INTEGER',
    is_key=True
)

child_parent_id = ERColumn(
    name='parent_id',
    type=u'INTEGER',
)
relation = Relation(
    right_col=u'parent',
    left_col=u'child',
    right_cardinality='*',
    left_cardinality='?',
)