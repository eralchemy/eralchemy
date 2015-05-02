# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from eralchemy import draw_er

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


def test():
    draw_er(Base, 'simple.pdf')

if __name__ == '__main__':
    test()