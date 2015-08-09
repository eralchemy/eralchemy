# -*- coding: utf-8 -*-
from eralchemy.models import Table, Relation, Column


class ParsingException(Exception):
    pass


class DuplicateTableException(ParsingException):
    pass


class DuplicateColumnException(ParsingException):
    pass


class RelationNoColException(ParsingException):
    pass


class NoCurrentTableException(ParsingException):
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


def _check_no_current_table(new_obj, current_table):
    """ Raises exception if we try to add a relation or a column
    with no current table. """
    if current_table is None:
        msg = 'Cannot add {} before adding table'
        if isinstance(new_obj, Relation):
            raise NoCurrentTableException(msg.format('relation'))
        if isinstance(new_obj, Column):
            raise NoCurrentTableException(msg.format('column'))


def _update_check_inputs(current_table, tables, relations):
    assert current_table is None or isinstance(current_table, Table)
    assert isinstance(tables, list)
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relations)
    assert current_table is None or current_table in tables


def _check_colname_in_lst(column_name, columns_names):
    if column_name not in columns_names:
        msg = 'Cannot add a relation with column "{}" which is undefined'
        raise RelationNoColException(msg.format(column_name))


def _check_not_creating_duplicates(new_name, names, type, exc):
    if new_name in names:
        msg = 'Cannot add {} named "{}" which is ' \
              'already present in the schema.'
        raise exc(msg.format(type, new_name))


def update_models(new_obj, current_table, tables, relations):
    """ Update the state of the parsing. """
    _update_check_inputs(current_table, tables, relations)
    _check_no_current_table(new_obj, current_table)

    if isinstance(new_obj, Table):
        tables_names = [t.name for t in tables]
        _check_not_creating_duplicates(new_obj.name, tables_names, 'table', DuplicateTableException)
        return new_obj, tables + new_obj, relations

    if isinstance(new_obj, Relation):
        columns_names = [c.name for t in tables for c in t.columns]
        _check_colname_in_lst(new_obj.right_col, columns_names)
        _check_colname_in_lst(new_obj.left_col, columns_names)
        return current_table, tables, relations + new_obj

    if isinstance(new_obj, Column):
        columns_names = [c.name for c in current_table.columns]
        _check_not_creating_duplicates(new_obj.name, columns_names, 'column', DuplicateColumnException)
        current_table.columns.append(new_obj)
        return current_table, tables, relations

    msg = "new_obj cannot be of type {}"
    raise ValueError(msg.format(new_obj.__class__.__name__))


def parse_file(filename):
    """ Parse a file and return to intermediary syntax. """
    with open(filename) as f:
        lines = f.readall()

    current_table = None
    tables = []
    relations = []
    for line in filter_lines_from_comments(lines):
        new_obj = parse_line(line)
        current_table, tables, relations = update_models(new_obj, current_table, tables, relations)
        pass
    return tables, relations