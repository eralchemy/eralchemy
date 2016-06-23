# -*- coding: utf-8 -*-
from eralchemy.version import version as __version__
from eralchemy.cst import GRAPH_BEGINNING
from eralchemy.sqla import metadata_to_intermediary, declarative_to_intermediary, database_to_intermediary
from pygraphviz.agraph import AGraph
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ArgumentError
from eralchemy.helpers import check_args
from eralchemy.parser import markdown_file_to_intermediary, line_iterator_to_intermediary, ParsingException
import argparse
import sys

try:
    basestring
except NameError:
    basestring = str


def cli():
    """Entry point for the application script"""
    parser = argparse.ArgumentParser(prog='ERAlchemy')
    parser.add_argument('-i', nargs='?', help='Database URI to process.')
    parser.add_argument('-o', nargs='?', help='Name of the file to write.')
    parser.add_argument('-s', nargs='?', help='Name of the schema.')
    parser.add_argument('-x', nargs='*', help='Name of the table(s) to exclude.')
    parser.add_argument('-v', help='Prints version number.', action='store_true')

    args = parser.parse_args()
    check_args(args)
    if args.v:
        print('ERAlchemy version {}.'.format(__version__))
        exit(0)
    render_er(args.i, args.o, exclude=args.x, schema=args.s)


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
    '_BoundDeclarativeMeta': declarative_to_intermediary
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


def filter_excludes(tables, relationships, exclude):
    """ This function excludes the tables and relationships with tables which are
    in the exclude (lst of str, tables names) """
    exclude = exclude or []
    tables_filtered = [t for t in tables if t.name not in exclude]
    relationships_filtered = [r for r in relationships
                              if r.right_col not in exclude and r.left_col not in exclude]
    return tables_filtered, relationships_filtered


def render_er(input, output, mode='auto', exclude=None, schema=None):
    """
    Transforms the metadata into a representation.
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
    :param schema: name of the schema
    """
    try:
        tables, relationships = all_to_intermediary(input, schema=schema)
        if exclude is not None:
            tables, relationships = filter_excludes(tables, relationships, exclude)
        intermediary_to_output = get_output_mode(output, mode)
        intermediary_to_output(tables, relationships, output)
    except ImportError as e:
        module_name = e.message.split()[-1]
        print('Please install {0} using "pip install {0}".'.format(module_name))
    except ParsingException as e:
        sys.stderr.write(e.message)


if __name__ == '__main__':
    cli()
