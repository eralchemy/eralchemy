# -*- coding: utf-8 -*-
from eralchemy.models import Table, Relation, Column


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


def parse_line(line):
    for typ in [Table, Relation, Column]:
        match = typ.RE.match(line)
        if match:
            return typ.make_from_match(match)


def parse_file(filename):
    """ Parse a file and return to intermediary syntax. """
    with open(filename) as f:
        lines = f.readall()

    current_table = None
    tables = []
    for line in filter_lines_from_comments(lines):
        obj = parse_line(line)

        pass