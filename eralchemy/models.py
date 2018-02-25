# -*- coding: utf-8 -*-
from eralchemy.cst import TABLE, FONT_TAGS, ROW_TAGS
import operator
import re

"""
All the intermediary syntax.
We can several kinds of models can be translated to this syntax.
"""


class Drawable:
    """ Abstract class to represent all the objects which are drawable."""
    RE = None

    def to_markdown(self):
        """Transforms the intermediary object to it's syntax in the er markup. """
        raise NotImplemented()

    def to_dot(self):
        """Transforms the intermediary object to it's syntax in the dot format. """
        raise NotImplemented()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def make_from_match(self):
        """ Used in the parsing of files. Transforms a regex match to a Drawable object. """
        raise NotImplemented()

    def __str__(self):
        return self.to_markdown()


class Column(Drawable):
    """ Represents a Column in the intermediaty syntax """
    RE = re.compile('(?P<primary>\*?)(?P<name>[^\s]+)\s*(\{label:\s*"(?P<label>[^"]+)"\})?')

    @staticmethod
    def make_from_match(match):
        return Column(
            name=match.group('name'),
            type=match.group('label'),
            is_key='*' in match.group('primary'),  # TODO foreign key
        )

    def __init__(self, name, type=None, is_key=False):
        """
        :param name: (str) Name of the column
        :param type:
        :param is_key:
        :return:
        """
        self.name = name
        self.type = type
        self.is_key = is_key

    @property
    def key_symbol(self):
        return '*' if self.is_key else ''

    def to_markdown(self):
        return '    {}{} {{label:"{}"}}'.format(self.key_symbol, self.name, self.type)

    def to_dot(self):
        base = ROW_TAGS.format(' ALIGN="LEFT"', '{key_opening}{col_name}{key_closing}{type}')
        return base.format(
            key_opening='<u>' if self.is_key else '',
            key_closing='</u>' if self.is_key else '',
            col_name=FONT_TAGS.format(self.name),
            type=FONT_TAGS.format(' [{}]').format(self.type) if self.type is not None else ''
        )


class Relation(Drawable):
    """ Represents a Relation in the intermediaty syntax """
    RE = re.compile(
        '(?P<left_name>[^\s]+)\s*(?P<left_cardinality>[*?+1])--(?P<right_cardinality>[*?+1])\s*(?P<right_name>[^\s]+)')  # noqa: E501
    cardinalities = {
        '*': '0..N',
        '?': '{0,1}',
        '+': '1..N',
        '1': '1',
        '': None
    }

    @staticmethod
    def make_from_match(match):
        return Relation(
            right_col=match.group('right_name'),
            left_col=match.group('left_name'),
            right_cardinality=match.group('right_cardinality'),
            left_cardinality=match.group('left_cardinality'),
        )

    def __init__(self, right_col, left_col, right_cardinality=None, left_cardinality=None):
        if right_cardinality not in self.cardinalities.keys() \
                or left_cardinality not in self.cardinalities.keys():
            raise ValueError('Cardinality should be in {}"'.format(self.cardinalities.keys()))
        self.right_col = right_col
        self.left_col = left_col
        self.right_cardinality = right_cardinality
        self.left_cardinality = left_cardinality

    def to_markdown(self):
        return "{} {}--{} {}".format(
            self.left_col,
            self.left_cardinality,
            self.right_cardinality,
            self.right_col,
        )

    def graphviz_cardinalities(self, card):
        if card == '':
            return ''
        return 'label=<<FONT>{}</FONT>>'.format(self.cardinalities[card])

    def to_dot(self):
        if self.right_cardinality == self.left_cardinality == '':
            return ''
        cards = []
        if self.left_cardinality != '':
            cards.append('tail' +
                         self.graphviz_cardinalities(self.left_cardinality))
        if self.right_cardinality != '':
            cards.append('head' +
                         self.graphviz_cardinalities(self.right_cardinality))
        return '"{}" -- "{}" [{}];'.format(self.left_col, self.right_col, ','.join(cards))

    def __eq__(self, other):
        if Drawable.__eq__(self, other):
            return True
        other_inversed = Relation(
            right_col=other.left_col,
            left_col=other.right_col,
            right_cardinality=other.left_cardinality,
            left_cardinality=other.right_cardinality,
        )
        return other_inversed.__dict__ == self.__dict__


class Table(Drawable):
    """ Represents a Table in the intermediaty syntax """
    RE = re.compile('\[(?P<name>[^]]+)\]')

    def __init__(self, name, columns):
        self.name = name
        self.columns = columns

    @staticmethod
    def make_from_match(match):
        return Table(
            name=match.group('name'),
            columns=[],
        )

    @property
    def header_markdown(self):
        return '[{}]'.format(self.name)

    def to_markdown(self):
        return self.header_markdown + '\n' + '\n'.join(c.to_markdown() for c in self.columns)

    @property
    def columns_sorted(self):
        return sorted(self.columns, key=operator.attrgetter('name'))

    @property
    def header_dot(self):
        return ROW_TAGS.format('', '<B><FONT POINT-SIZE="16">{}</FONT></B>').format(self.name)

    def to_dot(self):
        body = ''.join(c.to_dot() for c in self.columns)
        return TABLE.format(self.name, self.header_dot, body)

    def __str__(self):
        return self.header_markdown

    def __eq__(self, other):
        if not isinstance(other, Table):
            return False
        if other.name != self.name:
            return False

        if self.columns_sorted != other.columns_sorted:
            return False
        return True
