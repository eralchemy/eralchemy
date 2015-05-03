# -*- coding: utf-8 -*-
"""
This class allow to transform SQLAlchemy metadata to the intermediary syntax.
"""

from models import Relation, Column, Table


def relation_to_intermediary(fk):
    """Transform an SQLAlchemy ForeignKey object to it's intermediary representation. """
    return Relation(
        right_col=fk.parent.table.fullname,
        left_col=fk._column_tokens[1],
        right_cardinality='?',
        left_cardinality='*',
    )


def column_to_intermediary(col):
    """Transform an SQLAlchemy Column object to it's intermediary representation. """
    return Column(
        name=col.name,
        type=col.type,
        is_key=col.primary_key,
    )


def table_to_intermediary(table):
    """Transform an SQLAlchemy Table object to it's intermediary representation. """
    return Table(
        name=table.fullname,
        columns=[column_to_intermediary(col) for col in table.c._data.values()]
    )


def metadata_to_intermediary(metadata):
    """ Transforms SQLAlchemy metadata to the intermediary representation. """
    tables = [table_to_intermediary(table) for table in metadata.tables.values()]
    relationships = [relation_to_intermediary(fk) for table in metadata.tables.values() for fk in table.foreign_keys]
    return tables, relationships


def declarative_to_intermediary(base):
    """ Transform an SQLAlchemy Declarative Base to the intermediary representation. """
    return metadata_to_intermediary(base.metadata)


def database_to_intermediary(database_uri):
    """ Introspect from the database (given the database_uri) to create the intermediary representation. """
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import create_engine

    Base = automap_base()
    engine = create_engine(database_uri)

    # reflect the tables
    Base.prepare(engine, reflect=True)
    return declarative_to_intermediary(Base)