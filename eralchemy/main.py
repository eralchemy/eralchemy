import argparse
import base64
import copy
import logging
import re
import sys
from importlib.metadata import PackageNotFoundError, version

from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ArgumentError

from .cst import DOT_GRAPH_BEGINNING, ER_FORMAT_TITLE
from .helpers import check_args
from .parser import (
    ParsingException,
    line_iterator_to_intermediary,
    markdown_file_to_intermediary,
)
from .sqla import (
    database_to_intermediary,
    declarative_to_intermediary,
    metadata_to_intermediary,
)

USE_PYGRAPHVIZ = True
GRAPHVIZ_AVAILABLE = True
try:
    from pygraphviz.agraph import AGraph

    logging.debug("using pygraphviz")
except ImportError:
    USE_PYGRAPHVIZ = False
    try:
        from graphviz import Source

        logging.debug("using graphviz")
    except ImportError:
        logging.error("either pygraphviz or graphviz should be installed")
        GRAPHVIZ_AVAILABLE = False

try:
    __version__ = version(__package__)
except PackageNotFoundError:
    __version__ = "na"


def cli(args=None) -> None:
    """Entry point for the application script."""
    parser = get_argparser()

    args = parser.parse_args(args)
    check_args(args)
    if args.v:
        print(f"eralchemy version {__version__}.")
        exit(0)
    render_er(
        args.i,
        args.o,
        args.m or "auto",
        title=args.title,
        include_tables=args.include_tables,
        include_columns=args.include_columns,
        exclude_tables=args.exclude_tables,
        exclude_columns=args.exclude_columns,
        schema=args.s,
    )


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eralchemy")
    parser.add_argument("-i", nargs="?", help="Database URI to process.")
    parser.add_argument("-o", nargs="?", help="Name of the file to write.")
    parser.add_argument("-s", nargs="?", help="Name of the schema.")
    parser.add_argument("--title", nargs="?", help="Add a title to the output graph")
    parser.add_argument(
        "-m",
        nargs="?",
        help="Output mode to write format, default: auto",
    )
    parser.add_argument(
        "--exclude-tables",
        "-x",
        nargs="+",
        help="Name of tables not to be displayed.",
    )
    parser.add_argument(
        "--exclude-columns",
        nargs="+",
        help="Name of columns not to be displayed (for all tables).",
    )
    parser.add_argument(
        "--include-tables",
        nargs="+",
        help="Name of tables to be displayed alone.",
    )
    parser.add_argument(
        "--include-columns",
        nargs="+",
        help="Name of columns to be displayed alone (for all tables).",
    )
    parser.add_argument("-v", help="Prints version number.", action="store_true")
    return parser


def intermediary_to_markdown(tables, relationships, output, title=""):
    """Saves the intermediary representation to markdown."""
    er_markup = _intermediary_to_markdown(tables, relationships)
    if title:
        er_markup_with_config = f"{ER_FORMAT_TITLE.format(title)}\n{er_markup}"
    else:
        er_markup_with_config = er_markup
    with open(output, "w") as file_out:
        file_out.write(er_markup_with_config)


def intermediary_to_mermaid(tables, relationships, output, title=""):
    """Saves the intermediary representation to markdown."""
    markup = _intermediary_to_mermaid(tables, relationships)
    if title:
        markup = f"""---
title: {title}
---
{markup}
"""
    md_markup = f"<!--\n\n{markup}\n\n-->\n"
    markup_b64 = base64.urlsafe_b64encode(markup.encode("utf8")).decode("ascii")
    md_markup += f"![](https://mermaid.ink/img/{markup_b64})\n"
    with open(output, "w") as file_out:
        file_out.write(md_markup)


def intermediary_to_mermaid_er(tables, relationships, output, title=""):
    """Saves the intermediary representation to markdown."""
    markup = _intermediary_to_mermaid_er(tables, relationships)
    if title:
        markup = f"""---
title: {title}
---
{markup}
"""
    md_markup = f"<!--\n\n{markup}\n\n-->\n"
    markup_b64 = base64.urlsafe_b64encode(markup.encode("utf8")).decode("ascii")
    md_markup += f"![](https://mermaid.ink/img/{markup_b64})\n"
    with open(output, "w") as file_out:
        file_out.write(md_markup)


def intermediary_to_dot(tables, relationships, output, title=""):
    """Save the intermediary representation to dot format."""
    dot_file = _intermediary_to_dot(tables, relationships, title)
    with open(output, "w") as file_out:
        file_out.write(dot_file)


def intermediary_to_schema(tables, relationships, output, title=""):
    """Transforms and save the intermediary representation to the file chosen."""
    if not GRAPHVIZ_AVAILABLE:
        raise Exception("neither graphviz or pygraphviz are available. Install either library!")
    dot_file = _intermediary_to_dot(tables, relationships, title)
    extension = output.split(".")[-1]
    if USE_PYGRAPHVIZ:
        graph = AGraph()
        graph = graph.from_string(dot_file)
        graph.draw(path=output, prog="dot", format=extension)
    else:
        graph = Source(dot_file, engine="dot", format=extension)
        graph.render(outfile=output, cleanup=True)
    return graph


def _intermediary_to_markdown(tables, relationships):
    """Returns the er markup source in a string."""
    t = "\n".join(t.to_markdown() for t in tables)
    r = "\n".join(r.to_markdown() for r in relationships)
    return f"{t}\n{r}"


def _intermediary_to_mermaid(tables, relationships):
    """Returns the er markup source in a string."""
    t = "\n".join(t.to_mermaid() for t in tables)
    r = "\n".join(r.to_mermaid() for r in relationships)
    return f"classDiagram\n{t}\n{r}"


def _intermediary_to_mermaid_er(tables, relationships):
    """Returns the er markup source in a string."""
    t = "\n".join(t.to_mermaid_er() for t in tables)
    r = "\n".join(r.to_mermaid_er() for r in relationships)
    return f"erDiagram\n{t}\n{r}"


def _intermediary_to_dot(tables, relationships, title=""):
    """Returns the dot source representing the database in a string."""
    t = "\n".join(t.to_dot() for t in tables)
    r = "\n".join(r.to_dot() for r in relationships)

    graph_config = (
        f"""{DOT_GRAPH_BEGINNING}
         label="{title}"
         labelloc=t\n"""
        if title
        else DOT_GRAPH_BEGINNING
    )
    return f"{graph_config}\n{t}\n{r}\n}}"


# Routes from the class name to the function transforming this class in
# the intermediary representation.
switch_input_class_to_method = {
    "MetaData": metadata_to_intermediary,
    "DeclarativeMeta": declarative_to_intermediary,
    # For compatibility with Flask-SQLAlchemy
    "_BoundDeclarativeMeta": declarative_to_intermediary,
    # Renamed in Flask-SQLAlchemy 2.3
    "DefaultMeta": declarative_to_intermediary,
    "DeclarativeAttributeIntercept": declarative_to_intermediary,
}

# Routes from the mode to the method to transform the intermediary
#  representation to the desired output.
switch_output_mode_auto = {
    "er": intermediary_to_markdown,
    "mermaid": intermediary_to_mermaid,
    "mermaid_er": intermediary_to_mermaid_er,
    "graph": intermediary_to_schema,
    "dot": intermediary_to_dot,
}

# Routes from the file extension to the method to transform
# the intermediary representation to the desired output.
switch_output_mode = {
    "er": intermediary_to_markdown,
    "md": intermediary_to_mermaid,
    "dot": intermediary_to_dot,
}


def all_to_intermediary(filename_or_input, schema=None):
    """Dispatch the filename_or_input to the different function to produce the intermediary syntax.

    All the supported classes names are in `switch_input_class_to_method`.
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
    if isinstance(filename_or_input, str):
        if filename_or_input.split(".")[-1] == "er":
            return markdown_file_to_intermediary(filename_or_input)

    # try to read a markdown in a string
    if not isinstance(filename_or_input, str):
        if all(isinstance(e, str) for e in filename_or_input):
            return line_iterator_to_intermediary(filename_or_input)

    # try to read DB URI might raise ArgumentError.
    try:
        make_url(filename_or_input)
        return database_to_intermediary(filename_or_input, schema=schema)
    except ArgumentError as e:
        raise ValueError(f"Cannot process filename_or_input {input_class_name}: {e}")


def get_output_mode(output, mode):
    """From the output name and the mode returns a the function that will transform the intermediary representation to the output."""
    if mode != "auto":
        try:
            return switch_output_mode_auto[mode]
        except KeyError:
            raise ValueError(f'Mode "{mode}" is not supported.')

    extension = output.split(".")[-1]
    try:
        return switch_output_mode[extension]
    except KeyError:
        return intermediary_to_schema


def filter_resources(
    tables,
    relationships,
    include_tables=None,
    include_columns=None,
    exclude_tables=None,
    exclude_columns=None,
):
    """Filter the resources.

    Include the following:
        1. Tables and relationships with tables present in the include_tables (lst of str, tables names)
        2. Columns (of whichever table) present in the include_columns (lst of str, columns names)
    Exclude the following:
        1. Tables and relationships with tables present in the exclude_tables (lst of str, tables names)
        2. Columns (of whichever table) present in the exclude_columns (lst of str, columns names)
    Disclosure note:
        All relationships are taken into consideration before ignoring columns.
        In other words, if one excludes primary or foreign keys, it will still keep the relations display amongst tables.
    """
    _tables = copy.deepcopy(tables)
    _relationships = copy.deepcopy(relationships)

    include_tables_re = re.compile(
        "|".join(f"({name})" for name in (include_tables or [t.name for t in _tables])),
    )
    include_columns_re = re.compile(
        "|".join(
            f"({name})"
            for name in (include_columns or [c.name for t in _tables for c in t.columns])
        ),
    )
    exclude_tables_re = re.compile(
        "|".join(f"({name})" for name in (exclude_tables or [])),
    )
    exclude_columns_re = re.compile(
        "|".join(f"({name})" for name in (exclude_columns or [])),
    )

    def check_table(name):
        return not exclude_tables_re.fullmatch(name) and include_tables_re.fullmatch(
            name,
        )

    _tables = [t for t in _tables if check_table(t.name)]
    _relationships = [
        r
        for r in _relationships
        if not exclude_tables_re.fullmatch(r.right_table)
        and not exclude_tables_re.fullmatch(r.left_table)
        and include_tables_re.fullmatch(r.right_table)
        and include_tables_re.fullmatch(r.left_table)
    ]

    def check_column(name):
        return not exclude_columns_re.fullmatch(name) and include_columns_re.fullmatch(
            name,
        )

    for t in _tables:
        t.columns = sorted([c for c in t.columns if check_column(c.name)])

    return _tables, _relationships


def render_er(
    input,
    output,
    mode="auto",
    include_tables=None,
    include_columns=None,
    exclude_tables=None,
    exclude_columns=None,
    schema=None,
    title=None,
):
    """Transform the metadata into a representation.

    :param input: Possible inputs are instances of:
        MetaData: SQLAlchemy Metadata
        DeclarativeMeta: SQLAlchemy declarative Base
    :param output: name of the file to output the
    :param mode: str in list:
        'er': writes to a file the markup to generate an ER style diagram.
        'graph': writes the image of the ER diagram.
        'mermaid': writes to a file the markup to generate an Mermaid-JS style diagram
        'mermaid_er': writes the markup to generate an Mermaid-JS ER diagram
        'dot': write to file the diagram in dot format.
        'auto': choose from the filename:
            '*.er': writes to a file the markup to generate an ER style diagram.
            '.dot': returns the graph in the dot syntax.
            '.md': writes to a file the markup to generate an Mermaid-JS style diagram
            else: return a graph to the format graph
    :param include_tables: lst of str, table names to include, None means include all
    :param include_columns: lst of str, column names to include, None means include all
    :param exclude_tables: lst of str, table names to exclude, None means exclude nothing
    :param exclude_columns: lst of str, field names to exclude, None means exclude nothing
    :param schema: name of the schema
    :param title: title of the graph, only for .er, .dot, .png, .jpg outputs.
    """
    try:
        tables, relationships = all_to_intermediary(input, schema=schema)
        tables, relationships = filter_resources(
            tables,
            relationships,
            include_tables=include_tables,
            include_columns=include_columns,
            exclude_tables=exclude_tables,
            exclude_columns=exclude_columns,
        )
        intermediary_to_output = get_output_mode(output, mode)
        return intermediary_to_output(tables, relationships, output, title)
    except ImportError as e:
        module_name = e.message.split()[-1]
        print(f'Please install {module_name} using "pip install {module_name}".')
    except (FileNotFoundError, ValueError) as e:
        print(f"{e}")
    except ParsingException as e:
        sys.stderr.write(e.message)


if __name__ == "__main__":
    # cli("-i example/forum.er -o test.dot".split(" "))
    cli()
