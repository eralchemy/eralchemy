"""
This class allow to transform SQLAlchemy metadata to the intermediary syntax.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.exc import CompileError
from sqlalchemy.ext.automap import AutomapBase, automap_base

from .models import Column, Relation, Table

if TYPE_CHECKING:
    from typing_extensions import Protocol

    class DeclarativeBase(Protocol):
        metadata: sa.MetaData


def relation_to_intermediary(fk: sa.ForeignKey) -> Relation:
    """Transform an SQLAlchemy ForeignKey object to it's intermediary representation."""
    return Relation(
        right_col=format_name(fk.parent.table.fullname),
        left_col=format_name(fk._column_tokens[1]),
        right_cardinality="1" if fk.parent.primary_key or fk.parent.unique else "*",
        left_cardinality="?" if fk.parent.nullable else "1",
    )


def format_type(typ: Any) -> str:
    """Transforms the type into a nice string representation."""
    try:
        return str(typ)
    except CompileError:
        return "Null"


def format_name(name: Any) -> str:
    """Transforms the name into a nice string representation."""
    return str(name)


def column_to_intermediary(
    col: sa.Column, type_formatter: Callable[[Any], str] = format_type
) -> Column:
    """Transform an SQLAlchemy Column object to it's intermediary representation."""
    return Column(
        name=col.name,
        type=type_formatter(col.type),
        is_key=col.primary_key,
        is_null=col.nullable,
    )


def table_to_intermediary(table: sa.Table) -> Table:
    """Transform an SQLAlchemy Table object to it's intermediary representation."""
    table_columns = getattr(table.c, "_colset", getattr(table.c, "_data", {}).values())
    return Table(
        name=table.fullname,
        columns=[column_to_intermediary(col) for col in table_columns],
    )


def metadata_to_intermediary(
    metadata: sa.MetaData,
) -> tuple[list[Table], list[Relation]]:
    """Transforms SQLAlchemy metadata to the intermediary representation."""
    tables = [table_to_intermediary(table) for table in metadata.tables.values()]
    relationships = [
        relation_to_intermediary(fk)
        for table in metadata.tables.values()
        for fk in table.foreign_keys
    ]
    return tables, relationships


def declarative_to_intermediary(
    base: DeclarativeBase,
) -> tuple[list[Table], list[Relation]]:
    """Transform an SQLAlchemy Declarative Base to the intermediary representation."""
    return metadata_to_intermediary(base.metadata)


def name_for_scalar_relationship(
    base: AutomapBase,
    local_cls: Any,
    referred_cls: type[Any],
    constraint: sa.ForeignKeyConstraint,
) -> str:
    """Overriding naming schemes."""
    return referred_cls.__name__.lower() + "_ref"


def database_to_intermediary(
    database_uri: str, schema: str | None = None
) -> tuple[list[Table], list[Relation]]:
    """Introspect from the database (given the database_uri) to create the intermediary representation."""
    Base = automap_base()
    engine = create_engine(database_uri)
    if schema is not None:
        Base.metadata.schema = schema

    # reflect the tables
    Base.prepare(
        engine, reflect=True, name_for_scalar_relationship=name_for_scalar_relationship
    )
    return declarative_to_intermediary(Base)
