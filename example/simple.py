from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from eralchemy import render_er

Base = declarative_base()


class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey("parent.id"))
    parent = relationship("Parent", backref="children")


def example():
    render_er(Base, "simple.png")
    render_er(Base, "simple.dot")
    # render_er(Base, "simple.pdf")
    render_er(Base, "simple.er")
    render_er(Base, "simple.pu")
    render_er(Base, "simple.puml")
    render_er(Base, "simple.uml")


if __name__ == "__main__":
    example()
