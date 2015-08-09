# -*- coding: utf-8 -*-
import re
entity_re = re.compile('\[(?P<name>[^]]+)\]')
column_re = re.compile('(?P<primary>\*?)(?P<name>[^\s]+)')
relation_re = re.compile('(?P<l_name>[^\s]+)\s*(?P<l_card>[*?+1])--(?P<r_card>[*?+1])\s*(?P<r_name>[^\s]+)')


def remove_comments_from_line(line):
    if '#' not in line:
        return line
    return line[:line.index('#')].strip()


def filter_lines_from_comments(lines):
    """ Filter the lines from comments and non code lines. """
    for line in lines:
        rv = remove_comments_from_line(line)
        if rv == '':
            continue
        yield rv


def parse_line():
    pass


def parse_file(filename):
    """ Parse a file and return to intermediary syntax. """
    with open(filename) as f:
        lines = f.readall()

    current_table = None
    tables = []
    for line in filter_lines_from_comments(lines):
        pass

        