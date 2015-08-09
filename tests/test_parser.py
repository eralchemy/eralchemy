# -*- coding: utf-8 -*-
import pytest
from eralchemy.parser import remove_comments_from_line, parse_line
from eralchemy.models import Column, Table, Relation
# examples from https://github.com/BurntSushi/erd/blob/master/examples/nfldb.er
table_lst = [
    '[player]',
    '[team]',
    '[game]',
    '[drive]',
]

relations_lst = [
    'player      *--1 team',
    'game        *--1 team',
    'game        *--* team',
    'drive       1--1 team',
    'play        ?--1 team',
    'play_player *--+ team',
]

columns_lst = [
    # '*+gsis_id', # TODO add fk
    # '*+drive_id',
    '*play_id',
    'time',
    'pos_team',
    'yardline',
    'down',
    'yards_to_go',
]
elements_lst = table_lst + relations_lst + columns_lst


def test_remove_from_lines():
    r = remove_comments_from_line
    for code in elements_lst:
        assert r(code) == code
        assert r('{} ## some comment'.format(code)) == code
        assert r('{} ## some comment'.format(code)) == code
        assert r('{} #  # some comment'.format(code)) == code
        assert r('   {} #  # some comment'.format(code)) == code
        assert r('{}'.format(code)) == code
        assert r('#{} #  # some comment'.format(code)) == ''
        assert r('# #{} #  # some comment'.format(code)) == ''
        assert r('##{}'.format(code)) == ''


def test_parse_line():
    for s in columns_lst:
        rv = parse_line(s)
        assert rv.name == s.replace('*', '')
        assert isinstance(rv, Column)

    for s in relations_lst:
        rv = parse_line(s)
        assert rv.right_col == s[16:].strip()
        assert rv.left_col == s[:12].strip()
        assert rv.right_cardinality == s[15]
        assert rv.left_cardinality == s[12]
        assert isinstance(rv, Relation)

    for s in table_lst:
        rv = parse_line(s)
        assert rv.name == s[1:-1]
        assert rv.columns == []
        assert isinstance(rv, Table)

