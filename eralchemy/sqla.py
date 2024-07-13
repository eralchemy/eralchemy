"""This class allow to transform SQLAlchemy metadata to the intermediary syntax."""

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


def check_all_compound_same_parent(fk: sa.ForeignKey):
    """Checks if all other ForeignKey Constraints of our table are on the same parent table as the current one."""
    table = fk.column.table.fullname
    if not fk.constraint:
        return True
    for col in fk.constraint.table.columns:
        if not col.foreign_keys:
            return False
        for foreign_column in col.foreign_keys:
            if table != foreign_column.column.table.fullname:
                return False
    return True


def relation_to_intermediary(fk: sa.ForeignKey) -> Relation:
    """Transform an SQLAlchemy ForeignKey object to its intermediary representation."""
    primkey_count = 0
    if fk.constraint:
        primkey_count = sum(
            [True for x in fk.constraint.table.columns if x.primary_key],
        )
    # when there is only a single primary key column of the current key
    if (primkey_count == 1 and fk.parent.primary_key) or fk.parent.unique:
        right_cardinality = "1"
    else:
        # check if the other primkeys have a foreign key onto the same table
        # if this is the case, we are not optional and must be unique
        right_cardinality = "1" if check_all_compound_same_parent(fk) else "*"
    return Relation(
        right_table=format_name(fk.parent.table.fullname),
        right_column=format_name(fk.parent.name),
        left_table=format_name(fk.column.table.fullname),
        left_column=format_name(fk.column.name),
        right_cardinality=right_cardinality,
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
    col: sa.Column,
    type_formatter: Callable[[Any], str] = format_type,
) -> Column:
    """Transform an SQLAlchemy Column object to its intermediary representation."""
    return Column(
        name=col.name,
        type=type_formatter(col.type),
        is_key=col.primary_key,
        is_null=col.nullable,
    )


def table_to_intermediary(table: sa.Table) -> Table:
    """Transform an SQLAlchemy Table object to its intermediary representation."""
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
    database_uri: str,
    schema: str | None = None,
) -> tuple[list[Table], list[Relation]]:
    """Introspect from the database (given the database_uri) to create the intermediary representation."""
    Base = automap_base()
    engine = create_engine(database_uri)
    if schema is not None:
        schemas = schema.split(",")
        for schema in schemas:
            schema = schema.strip()
            # reflect the tables
            Base.metadata.schema = schema
            Base.prepare(
                engine,
                name_for_scalar_relationship=name_for_scalar_relationship,
            )
    else:
        # reflect the tables
        Base.prepare(
            engine,
            name_for_scalar_relationship=name_for_scalar_relationship,
        )

    return declarative_to_intermediary(Base)
