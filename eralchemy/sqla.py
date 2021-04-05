# -*- coding: utf-8 -*-
"""
This class allow to transform SQLAlchemy metadata to the intermediary syntax.
"""

from eralchemy.models import Relation, Column, Table
import sys
from sqlalchemy.exc import CompileError

if sys.version_info[0] == 3:
    unicode = str


def relation_to_intermediary(fk):
    """Transform an SQLAlchemy ForeignKey object to it's intermediary representation. """
    return Relation(
        right_col=format_name(fk.parent.table.fullname),
        left_col=format_name(fk._column_tokens[1]),
        right_cardinality='?',
        left_cardinality='*',
    )


def format_type(typ):
    """ Transforms the type into a nice string representation. """
    try:
        return unicode(typ)
    except CompileError:
        return 'Null'


def format_name(name):
    """ Transforms the name into a nice string representation. """
    return unicode(name)


def column_to_intermediary(col, type_formatter=format_type):
    """Transform an SQLAlchemy Column object to it's intermediary representation. """
    return Column(
        name=col.name,
        type=type_formatter(col.type),
        is_key=col.primary_key,
    )


def table_to_intermediary(table):
    """Transform an SQLAlchemy Table object to it's intermediary representation. """
    return Table(
        name=table.fullname,
        columns=[column_to_intermediary(col) for col in table.c._colset]
    )


def metadata_to_intermediary(metadata):
    """ Transforms SQLAlchemy metadata to the intermediary representation. """
    tables = [table_to_intermediary(table) for table in metadata.tables.values()]
    relationships = [relation_to_intermediary(fk) for table in metadata.tables.values() for fk in table.foreign_keys]
    return tables, relationships


def declarative_to_intermediary(base):
    """ Transform an SQLAlchemy Declarative Base to the intermediary representation. """
    return metadata_to_intermediary(base.metadata)


def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    """ Overriding naming schemes. """
    name = referred_cls.__name__.lower() + "_ref"
    return name


def database_to_intermediary(database_uri, schema=None):
    """ Introspect from the database (given the database_uri) to create the intermediary representation. """
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import create_engine

    Base = automap_base()
    engine = create_engine(database_uri)
    if schema is not None:
        Base.metadata.schema = schema

    # reflect the tables
    Base.prepare(engine, reflect=True, name_for_scalar_relationship=name_for_scalar_relationship)
    return declarative_to_intermediary(Base)
