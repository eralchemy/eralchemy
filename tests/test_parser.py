# -*- coding: utf-8 -*-
import pytest
from eralchemy.parser import remove_comments_from_line


def test_remove_from_lines():
    r = remove_comments_from_line
    for code in [
        '[Person]',
        '*name',
        'height',
        'weight',
        '+birth_location_id'
    ]:
        assert r(code) == code
        assert r('{} ## some comment'.format(code)) == code
        assert r('{} ## some comment'.format(code)) == code
        assert r('{} #  # some comment'.format(code)) == code
        assert r('   {} #  # some comment'.format(code)) == code
        assert r('{}'.format(code)) == code
        assert r('#{} #  # some comment'.format(code)) == ''
        assert r('# #{} #  # some comment'.format(code)) == ''
        assert r('##{}'.format(code)) == ''
