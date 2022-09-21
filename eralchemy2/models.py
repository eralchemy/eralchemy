"""
All the intermediary syntax.
We can several kinds of models can be translated to this syntax.
"""

from __future__ import annotations

import operator
import re
from abc import ABC, abstractmethod
from typing import Any, ClassVar

from .cst import FONT_TAGS, ROW_TAGS, TABLE


class Drawable(ABC):
    """Abstract class to represent all the objects which are drawable."""

    RE: ClassVar[re.Pattern[str]]

    def to_markdown(self) -> str:
        """Transforms the intermediary object to it's syntax in the er markup."""
        raise NotImplementedError()

    def to_dot(self) -> str:
        """Transforms the intermediary object to it's syntax in the dot format."""
        raise NotImplementedError()

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    @staticmethod
    @abstractmethod
    def make_from_match(match: re.Match) -> Drawable:
        """Used in the parsing of files. Transforms a regex match to a Drawable object."""

    def __str__(self) -> str:
        return self.to_markdown()


class Column(Drawable):
    """Represents a Column in the intermediaty syntax"""

    RE = re.compile(
        '(?P<primary>\*?)(?P<name>[^\s]+)\s*(\{label:\s*"(?P<label>[^"]+)"\})?'
    )

    @staticmethod
    def make_from_match(match: re.Match) -> Column:
        return Column(
            name=match.group("name"),
            type=match.group("label"),
            is_key="*" in match.group("primary"),
            is_null=not "*" in match.group("primary"),
        )

    def __init__(self, name: str, type=None, is_key: bool = False, is_null=None):
        """
        :param name: (str) Name of the column
        :param type:
        :param is_key:
        :param is_null:
        :return:
        """
        self.name = name
        self.type = type
        self.is_key = is_key
        if is_null == None:
            self.is_null = not is_key
        else:
            self.is_null = is_null

    def __lt__(self, other: Column) -> bool:
        if self.is_key > other.is_key:
            return True
        elif self.is_key < other.is_key:
            return False
        else:
            return self.name < other.name

    @property
    def key_symbol(self) -> str:
        return "*" if self.is_key else ""

    def to_markdown(self) -> str:
        return '    {}{} {{label:"{}"}}'.format(self.key_symbol, self.name, self.type)

    def to_mermaid(self) -> str:
        return " {}{} {}{}".format(
            self.key_symbol,
            self.type.replace("(", "<").replace(")", ">"),
            self.name,
            " NOT NULL" if not self.is_null else "",
        )

    def to_dot(self) -> str:
        base = ROW_TAGS.format(
            ' ALIGN="LEFT"', "{key_opening}{col_name}{key_closing}{type}{null}"
        )
        return base.format(
            key_opening="<u>" if self.is_key else "",
            key_closing="</u>" if self.is_key else "",
            col_name=FONT_TAGS.format(self.name),
            type=FONT_TAGS.format(" [{}]").format(self.type)
            if self.type is not None
            else "",
            null=" NOT NULL" if not self.is_null else "",
        )


class Relation(Drawable):
    """Represents a Relation in the intermediaty syntax"""

    RE = re.compile(
        "(?P<left_name>[^\s]+)\s*(?P<left_cardinality>[*?+1])--(?P<right_cardinality>[*?+1])\s*(?P<right_name>[^\s]+)"
    )  # noqa: E501
    cardinalities = {"*": "0..N", "?": "{0,1}", "+": "1..N", "1": "1", "": None}
    cardinalities_mermaid = {
        "*": "0..n",
        "?": "0..1",
        "+": "1..n",
    }

    @staticmethod
    def make_from_match(match: re.Match) -> Relation:
        return Relation(
            right_col=match.group("right_name"),
            left_col=match.group("left_name"),
            right_cardinality=match.group("right_cardinality"),
            left_cardinality=match.group("left_cardinality"),
        )

    def __init__(
        self, right_col, left_col, right_cardinality=None, left_cardinality=None
    ):
        if (
            right_cardinality not in self.cardinalities.keys()
            or left_cardinality not in self.cardinalities.keys()
        ):
            raise ValueError(
                'Cardinality should be in {}"'.format(self.cardinalities.keys())
            )
        self.right_col = right_col
        self.left_col = left_col
        self.right_cardinality = right_cardinality
        self.left_cardinality = left_cardinality

    def to_markdown(self) -> str:
        return "{} {}--{} {}".format(
            self.left_col,
            self.left_cardinality,
            self.right_cardinality,
            self.right_col,
        )

    def to_mermaid(self) -> str:
        normalized = (
            Relation.cardinalities_mermaid.get(k, k)
            for k in (
                self.left_col,
                self.left_cardinality,
                self.right_cardinality,
                self.right_col,
            )
        )
        return '{} "{}" -- "{}" {}'.format(*normalized)

    def graphviz_cardinalities(self, card) -> str:
        if card == "":
            return ""
        return "label=<<FONT>{}</FONT>>".format(self.cardinalities[card])

    def to_dot(self) -> str:
        if self.right_cardinality == self.left_cardinality == "":
            return ""
        cards = []
        if self.left_cardinality != "":
            cards.append("tail" + self.graphviz_cardinalities(self.left_cardinality))
        if self.right_cardinality != "":
            cards.append("head" + self.graphviz_cardinalities(self.right_cardinality))
        return '"{}" -- "{}" [{}];'.format(
            self.left_col, self.right_col, ",".join(cards)
        )

    def __eq__(self, other: Any) -> bool:
        if super().__eq__(other):
            return True
        other_inversed = Relation(
            right_col=other.left_col,
            left_col=other.right_col,
            right_cardinality=other.left_cardinality,
            left_cardinality=other.right_cardinality,
        )
        return other_inversed.__dict__ == self.__dict__


class Table(Drawable):
    """Represents a Table in the intermediaty syntax"""

    RE = re.compile("\[(?P<name>[^]]+)\]")

    def __init__(self, name: str, columns: list[Column]) -> None:
        self.name = name
        self.columns = columns

    @staticmethod
    def make_from_match(match: re.Match) -> Table:
        return Table(name=match.group("name"), columns=[])

    @property
    def header_markdown(self) -> str:
        return "[{}]".format(self.name)

    def to_markdown(self) -> str:
        return (
            self.header_markdown
            + "\n"
            + "\n".join(c.to_markdown() for c in self.columns)
        )

    def to_mermaid(self) -> str:
        columns = [c.to_mermaid() for c in self.columns]
        return (
            "class {}{{\n  ".format(self.name)
            + "\n  ".format(self.name).join(columns)  # type:ignore
            + "\n}"
        )

    @property
    def columns_sorted(self):
        return sorted(self.columns, key=operator.attrgetter("name"))

    @property
    def header_dot(self) -> str:
        return ROW_TAGS.format("", '<B><FONT POINT-SIZE="16">{}</FONT></B>').format(
            self.name
        )

    def to_dot(self) -> str:
        body = "".join(c.to_dot() for c in self.columns)
        return TABLE.format(self.name, self.header_dot, body)

    def __str__(self) -> str:
        return self.header_markdown

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Table):
            return False
        if other.name != self.name:
            return False

        if self.columns_sorted != other.columns_sorted:
            return False
        return True
