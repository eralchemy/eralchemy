# -*- coding: utf-8 -*-
import pytest
from eralchemy.parser import remove_comments_from_line
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
    'game        *--1 team',
    'drive       *--1 team',
    'play        *--1 team',
    'play_player *--1 team',
]

columns_lst = [
    '*+gsis_id',
    '*+drive_id',
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
    pass