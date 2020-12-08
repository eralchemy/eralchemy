"""
Converts Google BigQuery tables into the eralchemy intermediate representation.
"""

import os
import re
from collections import namedtuple
from typing import Iterable, Tuple, Union

from google.cloud.bigquery import Table

from eralchemy.models import (
    Column as ERColumn,
    Table as ERTable,
    Relation as ERRelation,
)


_BQColumn = namedtuple("BQColumn", ("name", "field_type", "mode", "description"))

_DEFAULT_PATTERN = r"->\s([?*+1 ]:[?*+1 ]\s)?(.*\.)?(.*)\.(.*)$"
_DEFAULT_CARDINALITY = ("*", "1")

_PATTERN = re.compile(os.environ.get("GBQ_RELATION_PATTERN") or _DEFAULT_PATTERN)


def _walk_columns(fields, name_prefix=""):
    for col in fields:
        name = ".".join((name_prefix, col.name)) if name_prefix else col.name
        yield _BQColumn(name, col.field_type, col.mode, col.description)
        if col.fields:
            for nested_col in _walk_columns(col.fields, name):
                yield nested_col


def _process_relation(column_description, right_dataset, right_table):
    if not column_description:
        return None
    result = re.search(_PATTERN, column_description)
    if not result:
        return None
    cardinality = result.group(1)
    cardinality = (
        tuple(cardinality.strip().split(":")) if cardinality else _DEFAULT_CARDINALITY
    )
    left_dataset = result.group(2)
    left_dataset = left_dataset.strip(".") if left_dataset else right_dataset
    left_table = result.group(3)
    return ERRelation(
        left_col=f"{left_dataset}.{left_table}",
        right_col=f"{right_dataset}.{right_table}",
        left_cardinality=cardinality[1],
        right_cardinality=cardinality[0],
    )


def _process_column_type(column):
    mode = column.mode
    if mode:
        return f"{mode}({column.field_type})"
    return column.field_type


# pylint: disable=unused-argument
def _process_column_is_key(column) -> bool:
    return False


# pylint: enable=unused-argument


def _process_table(table: Table) -> ERTable:
    columns = [
        ERColumn(col.name, _process_column_type(col), _process_column_is_key(col))
        for col in _walk_columns(table.schema)
    ]
    table = ERTable(f"{table.dataset_id}.{table.table_id}", columns)
    return table


def bigquery_to_intermediary(
    tables: Iterable[Table],
) -> Tuple[Iterable[Union[ERTable, ERRelation]]]:
    """
    Converts BigQuery tables into the eralchemy intermediary format.

    Args:
        tables (Iterable[google.cloud.bigquery.Table]): An iterable of Table instances.

    Returns:
        A tuple with two elements:
            - The first element is an iterable of eralchemy.models.Table
            - The second element is an iterable of eralchemy.models.Relation
    """
    tables_ = [_process_table(table) for table in tables]
    relations = [
        _process_relation(col.description, table.dataset_id, table.table_id)
        for table in tables
        for col in _walk_columns(table.schema)
    ]
    relations = [relation for relation in relations if relation]
    return tables_, relations
