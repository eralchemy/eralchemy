# -*- coding: utf-8 -*-
from eralchemy.models import Table, Relation, Column

class ParsingException(Exception):
    pass

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


def update_models(new_obj, current_table, tables):
    assert current_table is None or current_table in tables
    if current_table is None:
        msg = 'Cannot add {} before adding table'
        if isinstance(new_obj, Relation):
            raise ParsingException(msg.format('relation'))
        if isinstance(new_obj, Column):
            raise ParsingException(msg.format('column'))



def parse_file(filename):
    """ Parse a file and return to intermediary syntax. """
    with open(filename) as f:
        lines = f.readall()

    current_table = None
    tables = []
    for line in filter_lines_from_comments(lines):
        new_obj = parse_line(line)

        pass