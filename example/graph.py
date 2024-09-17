# from https://github.com/sqlalchemy/sqlalchemy/blob/main/examples/graphs/directed_graph.py
"""A directed graph example."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

from eralchemy import render_er

Base = declarative_base()


class Node(Base):
    __tablename__ = "node"

    node_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lower_edges: Mapped[list[Edge]] = relationship(back_populates="lower_node")
    higher_edges: Mapped[list[Edge]] = relationship(back_populates="higher_node")

    def add_neighbors(self, *nodes):
        for node in nodes:
            Edge(self, node)
        return self

    def higher_neighbors(self) -> list[Node]:
        return [x.higher_node for x in self.lower_edges]

    def lower_neighbors(self) -> list[Node]:
        return [x.lower_node for x in self.higher_edges]


class Edge(Base):
    __tablename__ = "edge"

    lower_id: Mapped[int] = mapped_column(Integer, ForeignKey("node.node_id"), primary_key=True)
    higher_id: Mapped[int] = mapped_column(Integer, ForeignKey("node.node_id"), primary_key=True)
    lower_node: Mapped[Node] = relationship(back_populates="lower_edges")
    higher_node: Mapped[Node] = relationship(back_populates="higher_edges")

    def __init__(self, n1: Node, n2: Node) -> None:
        if n1.node_id < n2.node_id:
            self.lower_node = n1
            self.higher_node = n2
        else:
            self.lower_node = n2
            self.higher_node = n1


if __name__ == "__main__":
    render_er(Base, "graph.png")
    render_er(Base, "graph.dot")
    render_er(Base, "graph.pdf")
