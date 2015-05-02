# -*- coding: utf-8 -*-
"""
This class allow to transform SQLAlchemy metadata to the intermediary syntax.
"""

from models import Relation, Column, Table


def relation_to_intermediary(fk):
    return Relation(
        right_col=fk.parent.table.fullname,
        left_col=fk._column_tokens[1],
        right_cardinality='?',
        left_cardinality='*',
    )


def column_to_intermediary(col):
    return Column(
        name=col.name,
        type=col.type,
        is_key=col.primary_key,
    )


def table_to_intermediary(table):
    return Table(
        name=table.fullname,
        columns=[column_to_intermediary(col) for col in table.c._data.values()]
    )


def metadata_to_intermediary(metadata):
    tables = [table_to_intermediary(table) for table in metadata.tables.values()]
    relationships = [relation_to_intermediary(fk) for table in metadata.tables.values() for fk in table.foreign_keys]
    return tables, relationships


def declarative_to_intermediary(base):
    return metadata_to_intermediary(base.metadata)