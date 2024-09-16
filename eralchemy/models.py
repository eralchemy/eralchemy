"""All the intermediary syntax.

We can several kinds of models can be translated to this syntax.
"""

from __future__ import annotations

import operator
import re
from abc import ABC, abstractmethod
from typing import ClassVar

from .cst import FONT_TAGS, ROW_TAGS, TABLE


class Drawable(ABC):
    """Abstract class to represent all the objects which are drawable."""

    RE: ClassVar[re.Pattern[str]]

    def to_markdown(self) -> str:
        """Transforms the intermediary object to its syntax in the er markup."""
        raise NotImplementedError()

    def to_dot(self) -> str:
        """Transforms the intermediary object to its syntax in the dot format."""
        raise NotImplementedError()

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    @staticmethod
    @abstractmethod
    def make_from_match(match: re.Match) -> Drawable:
        """Used in the parsing of files. Transforms a regex match to a Drawable object."""

    def __str__(self) -> str:
        return self.to_markdown()


def sanitize_mermaid(text: str, *, is_er: bool = False):
    RE = re.compile("[^0-9a-zA-Z_-]+")
    """Mermaid does not allow special characters in column names"""
    if not text:
        return text
    if is_er and (text[0].isdigit() or text[0] == "-"):
        # mermaid ER does not allow leading dash or digits in column names
        text = "_" + text
    return re.sub(RE, "_", text)


class Column(Drawable):
    """Represents a Column in the intermediaty syntax."""

    RE = re.compile(
        r'(?P<primary>\*?)(?P<name>\w+(\s*\w+)*)\s*(\{label:\s*"(?P<label>[^"]+)"\})?',
    )

    @staticmethod
    def make_from_match(match: re.Match) -> Column:
        return Column(
            name=match.group("name"),
            type=match.group("label"),
            is_key="*" in match.group("primary"),
            is_null="*" not in match.group("primary"),
        )

    def __init__(self, name: str, type=None, is_key: bool = False, is_null=None):
        """Initialize the Column class.

        :param name: (str) Name of the column
        :param type:
        :param is_key:
        :param is_null:
        :return:
        """
        self.name = name
        self.type = type
        self.is_key = is_key
        if is_null is None:
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
        name = sanitize_mermaid(self.name)
        return f'    {self.key_symbol}{name} {{label:"{self.type}"}}'

    def to_mermaid(self) -> str:
        return " {}{} {}{}".format(
            self.key_symbol,
            self.type.replace("(", "<").replace(")", ">"),
            self.name,
            " NOT NULL" if not self.is_null else "",
        )

    def to_mermaid_er(self) -> str:
        type_str = self.type.replace(" ", "_")
        name = sanitize_mermaid(self.name, is_er=True)
        return f" {type_str} {name} {'PK' if self.is_key else ''}"

    def to_dot(self) -> str:
        base = ROW_TAGS.format(
            ' ALIGN="LEFT" {port}',
            "{key_opening}{col_name}{key_closing} {type}{null}",
        )
        return base.format(
            port=f'PORT="{self.name}"' if self.name else "",
            key_opening="<u>" if self.is_key else "",
            key_closing="</u>" if self.is_key else "",
            col_name=FONT_TAGS.format(self.name),
            type=(FONT_TAGS.format(" [{}]").format(self.type) if self.type is not None else ""),
            null=" NOT NULL" if not self.is_null else "",
        )


class Relation(Drawable):
    """Represents a Relation in the intermediaty syntax."""

    RE = re.compile(
        r"""
        (?P<left_table>[^\s]+?)
        (?:\.\"(?P<left_column>.+)\")?
        \s*
        (?P<left_cardinality>[*?+1])
        --
        (?P<right_cardinality>[*?+1])
        \s*
        (?P<right_table>[^\s]+?)
        (?:\.\"(?P<right_column>.+)\")?
        \s*$
        """,
        re.VERBOSE,
    )
    cardinalities = {"*": "0..N", "?": "{0,1}", "+": "1..N", "1": "1", "": None}
    cardinalities_mermaid = {
        "*": "0..n",
        "?": "0..1",
        "+": "1..n",
    }
    cardinalities_crowfoot = {
        "*": "0+",
        "?": "one or zero",
        "+": "1+",
    }

    @staticmethod
    def make_from_match(match: re.Match) -> Relation:
        return Relation(**match.groupdict())

    def __init__(
        self,
        right_table,
        left_table,
        right_cardinality=None,
        left_cardinality=None,
        right_column=None,
        left_column=None,
    ):
        if (
            right_cardinality not in self.cardinalities.keys()
            or left_cardinality not in self.cardinalities.keys()
        ):
            raise ValueError(f"Cardinality should be in {self.cardinalities.keys()}")
        self.right_table = right_table
        self.right_column = right_column or ""
        self.left_table = left_table
        self.left_column = left_column or ""
        self.right_cardinality = right_cardinality
        self.left_cardinality = left_cardinality

    def to_markdown(self) -> str:
        return "{}{} {}--{} {}{}".format(
            self.left_table,
            "" if not self.left_column else f'."{self.left_column}"',
            self.left_cardinality,
            self.right_cardinality,
            self.right_table,
            "" if not self.right_column else f'."{self.right_column}"',
        )

    def to_mermaid(self) -> str:
        normalized = (
            Relation.cardinalities_mermaid.get(k, k)
            for k in (
                sanitize_mermaid(self.left_table),
                self.left_cardinality,
                self.right_cardinality,
                sanitize_mermaid(self.right_table),
            )
        )
        return '{} "{}" -- "{}" {}'.format(*normalized)

    def to_mermaid_er(self) -> str:
        left = Relation.cardinalities_crowfoot.get(
            self.left_cardinality,
        )
        right = Relation.cardinalities_crowfoot.get(
            self.right_cardinality,
        )

        left_col = sanitize_mermaid(self.left_table, is_er=True)
        right_col = sanitize_mermaid(self.right_table, is_er=True)
        return f"{left_col} {left}--{right} {right_col} : has"

    def graphviz_cardinalities(self, card) -> str:
        if card == "":
            return ""
        return f"label=<<FONT>{self.cardinalities[card]}</FONT>>"

    def to_dot(self) -> str:
        if self.right_cardinality == self.left_cardinality == "":
            return ""
        cards = []
        if self.left_cardinality != "":
            cards.append("tail" + self.graphviz_cardinalities(self.left_cardinality))
        if self.right_cardinality != "":
            cards.append("head" + self.graphviz_cardinalities(self.right_cardinality))
        left_col = f':"{self.left_column}"' if self.left_column else ""
        right_col = f':"{self.right_column}"' if self.right_column else ""
        return (
            f'"{self.left_table}"{left_col} -- "{self.right_table}"{right_col} [{",".join(cards)}];'
        )

    def __eq__(self, other: object) -> bool:
        if super().__eq__(other):
            return True
        if not isinstance(other, Relation):
            return False
        other_inversed = Relation(
            right_table=other.left_table,
            right_column=other.left_column,
            left_table=other.right_table,
            left_column=other.right_column,
            right_cardinality=other.left_cardinality,
            left_cardinality=other.right_cardinality,
        )
        return other_inversed.__dict__ == self.__dict__


class Table(Drawable):
    """Represents a Table in the intermediaty syntax."""

    RE = re.compile(r"\[(?P<name>[^]]+)\]")

    def __init__(self, name: str, columns: list[Column]) -> None:
        self.name = name
        self.columns = columns

    @staticmethod
    def make_from_match(match: re.Match) -> Table:
        return Table(name=match.group("name"), columns=[])

    @property
    def header_markdown(self) -> str:
        return f"[{self.name}]"

    def to_markdown(self) -> str:
        return self.header_markdown + "\n" + "\n".join(c.to_markdown() for c in self.columns)

    def to_mermaid(self) -> str:
        columns = [c.to_mermaid() for c in self.columns]
        name = sanitize_mermaid(self.name)
        return f"class {name}{{\n" + "\n  ".join(columns) + "\n}"

    def to_mermaid_er(self) -> str:
        columns = [c.to_mermaid_er() for c in self.columns]
        name = sanitize_mermaid(self.name, is_er=True)
        return f"{name} {{\n" + "\n  ".join(columns) + "\n}"

    @property
    def columns_sorted(self):
        return sorted(self.columns, key=operator.attrgetter("name"))

    @property
    def header_dot(self) -> str:
        return ROW_TAGS.format("", f'<B><FONT POINT-SIZE="16">{self.name}</FONT></B>')

    def to_dot(self) -> str:
        body = "".join(c.to_dot() for c in self.columns)
        return TABLE.format(self.name, self.header_dot, body)

    def __str__(self) -> str:
        return self.header_markdown

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Table):
            return False
        if other.name != self.name:
            return False

        if self.columns_sorted != other.columns_sorted:
            return False
        return True
