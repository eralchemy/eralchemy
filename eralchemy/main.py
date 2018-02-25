# -*- coding: utf-8 -*-
import argparse
import sys
import copy

from pygraphviz.agraph import AGraph
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ArgumentError

from eralchemy.version import version as __version__
from eralchemy.cst import GRAPH_BEGINNING
from eralchemy.sqla import metadata_to_intermediary, declarative_to_intermediary, database_to_intermediary
from eralchemy.helpers import check_args
from eralchemy.parser import markdown_file_to_intermediary, line_iterator_to_intermediary, ParsingException

try:
    basestring
except NameError:
    basestring = str


def cli():
    """Entry point for the application script"""
    parser = get_argparser()

    args = parser.parse_args()
    check_args(args)
    if args.v:
        print('ERAlchemy version {}.'.format(__version__))
        exit(0)
    render_er(
        args.i,
        args.o,
        include_tables=args.include_tables,
        include_columns=args.include_columns,
        exclude_tables=args.exclude_tables,
        exclude_columns=args.exclude_columns,
        schema=args.s
    )


def get_argparser():
    parser = argparse.ArgumentParser(prog='ERAlchemy')
    parser.add_argument('-i', nargs='?', help='Database URI to process.')
    parser.add_argument('-o', nargs='?', help='Name of the file to write.')
    parser.add_argument('-s', nargs='?', help='Name of the schema.')
    parser.add_argument('--exclude-tables', '-x', nargs='+', help='Name of tables not to be displayed.')
    parser.add_argument('--exclude-columns', nargs='+', help='Name of columns not to be displayed (for all tables).')
    parser.add_argument('--include-tables', nargs='+', help='Name of tables to be displayed alone.')
    parser.add_argument('--include-columns', nargs='+', help='Name of columns to be displayed alone (for all tables).')
    parser.add_argument('-v', help='Prints version number.', action='store_true')
    return parser


def intermediary_to_markdown(tables, relationships, output):
    """ Saves the intermediary representation to markdown. """
    er_markup = _intermediary_to_markdown(tables, relationships)
    with open(output, "w") as file_out:
        file_out.write(er_markup)


def intermediary_to_dot(tables, relationships, output):
    """ Save the intermediary representation to dot format. """
    dot_file = _intermediary_to_dot(tables, relationships)
    with open(output, "w") as file_out:
        file_out.write(dot_file)


def intermediary_to_schema(tables, relationships, output):
    """ Transforms and save the intermediary representation to the file chosen. """
    dot_file = _intermediary_to_dot(tables, relationships)
    graph = AGraph()
    graph = graph.from_string(dot_file)
    extension = output.split('.')[-1]
    graph.draw(path=output, prog='dot', format=extension)


def _intermediary_to_markdown(tables, relationships):
    """ Returns the er markup source in a string. """
    t = '\n'.join(t.to_markdown() for t in tables)
    r = '\n'.join(r.to_markdown() for r in relationships)
    return '{}\n{}'.format(t, r)


def _intermediary_to_dot(tables, relationships):
    """ Returns the dot source representing the database in a string. """
    t = '\n'.join(t.to_dot() for t in tables)
    r = '\n'.join(r.to_dot() for r in relationships)
    return '{}\n{}\n{}\n}}'.format(GRAPH_BEGINNING, t, r)


# Routes from the class name to the function transforming this class in
# the intermediary representation.
switch_input_class_to_method = {
    'MetaData': metadata_to_intermediary,
    'DeclarativeMeta': declarative_to_intermediary,
    # For compatibility with Flask-SQLAlchemy
    '_BoundDeclarativeMeta': declarative_to_intermediary,
    # Renamed in Flask-SQLAlchemy 2.3
    'DefaultMeta': declarative_to_intermediary
}

# Routes from the mode to the method to transform the intermediary
#  representation to the desired output.
switch_output_mode_auto = {
    'er': intermediary_to_markdown,
    'graph': intermediary_to_schema,
    'dot': intermediary_to_dot
}

# Routes from the file extension to the method to transform
# the intermediary representation to the desired output.
switch_output_mode = {
    'er': intermediary_to_markdown,
    'dot': intermediary_to_dot,
}


def all_to_intermediary(filename_or_input, schema=None):
    """ Dispatch the filename_or_input to the different function to produce the intermediary syntax.
    All the supported classes names are in `swich_input_class_to_method`.
    The input can also be a list of strings in markdown format or a filename finishing by '.er' containing markdown
    format.
    """
    # Try to convert from the name of the class
    input_class_name = filename_or_input.__class__.__name__
    try:
        this_to_intermediary = switch_input_class_to_method[input_class_name]
        tables, relationships = this_to_intermediary(filename_or_input)
        return tables, relationships
    except KeyError:
        pass

    # try to read markdown file.
    if isinstance(filename_or_input, basestring):
        if filename_or_input.split('.')[-1] == 'er':
            return markdown_file_to_intermediary(filename_or_input)

    # try to read a markdown in a string
    if not isinstance(filename_or_input, basestring):
        if all(isinstance(e, basestring) for e in filename_or_input):
            return line_iterator_to_intermediary(filename_or_input)

    # try to read DB URI.
    try:
        make_url(filename_or_input)
        return database_to_intermediary(filename_or_input, schema=schema)
    except ArgumentError:
        pass

    msg = 'Cannot process filename_or_input {}'.format(input_class_name)
    raise ValueError(msg)


def get_output_mode(output, mode):
    """
    From the output name and the mode returns a the function that will transform the intermediary
    representation to the output.
    """
    if mode != 'auto':
        try:
            return switch_output_mode_auto[mode]
        except KeyError:
            raise ValueError('Mode "{}" is not supported.')

    extension = output.split('.')[-1]
    try:
        return switch_output_mode[extension]
    except KeyError:
        return intermediary_to_schema


def filter_resources(tables, relationships,
                     include_tables=None, include_columns=None,
                     exclude_tables=None, exclude_columns=None):
    """
    Include the following:
        1. Tables and relationships with tables present in the include_tables (lst of str, tables names)
        2. Columns (of whichever table) present in the include_columns (lst of str, columns names)
    Exclude the following:
        1. Tables and relationships with tables present in the exclude_tables (lst of str, tables names)
        2. Columns (of whichever table) present in the exclude_columns (lst of str, columns names)
    Disclosure note:
        All relationships are taken into consideration before ignoring columns.
        In other words, if one excludes primary or foreign keys, it will still keep the relations display amongst tables
    """
    _tables = copy.deepcopy(tables)
    _relationships = copy.deepcopy(relationships)

    include_tables = include_tables or [t.name for t in _tables]
    include_columns = include_columns or [c.name for t in _tables for c in t.columns]
    exclude_tables = exclude_tables or list()
    exclude_columns = exclude_columns or list()

    _tables = [t for t in _tables if t.name not in exclude_tables and t.name in include_tables]
    _relationships = [r for r in _relationships
                      if r.right_col not in exclude_tables
                      and r.left_col not in exclude_tables
                      and r.right_col in include_tables
                      and r.left_col in include_tables]

    for t in _tables:
        t.columns = [c for c in t.columns if c.name not in exclude_columns and c.name in include_columns]

    return _tables, _relationships


def render_er(input, output, mode='auto', include_tables=None, include_columns=None,
              exclude_tables=None, exclude_columns=None, schema=None):
    """
    Transform the metadata into a representation.
    :param input: Possible inputs are instances of:
        MetaData: SQLAlchemy Metadata
        DeclarativeMeta: SQLAlchemy declarative Base
    :param output: name of the file to output the
    :param mode: str in list:
        'er': writes to a file the markup to generate an ER style diagram.
        'graph': writes the image of the ER diagram.
        'dot': write to file the diagram in dot format.
        'auto': choose from the filename:
            '*.er': writes to a file the markup to generate an ER style diagram.
            '.dot': returns the graph in the dot syntax.
            else: return a graph to the format graph
    :param include_tables: lst of str, table names to include, None means include all
    :param include_columns: lst of str, column names to include, None means include all
    :param exclude_tables: lst of str, table names to exclude, None means exclude nothing
    :param exclude_columns: lst of str, field names to exclude, None means exclude nothing
    :param schema: name of the schema
    """
    try:
        tables, relationships = all_to_intermediary(input, schema=schema)
        tables, relationships = filter_resources(tables, relationships,
                                                 include_tables=include_tables, include_columns=include_columns,
                                                 exclude_tables=exclude_tables, exclude_columns=exclude_columns)
        intermediary_to_output = get_output_mode(output, mode)
        intermediary_to_output(tables, relationships, output)
    except ImportError as e:
        module_name = e.message.split()[-1]
        print('Please install {0} using "pip install {0}".'.format(module_name))
    except ParsingException as e:
        sys.stderr.write(e.message)


if __name__ == '__main__':
    cli()
