from __future__ import annotations

from typing import ClassVar, Iterator

from .models import Column, Drawable, Relation, Table

TYPES: list[type[Drawable]] = [Table, Relation, Column]


class ParsingException(Exception):
    base_traceback = "Error on line {line_nb}: {line}\n{error}"
    hint: ClassVar[str | None] = None

    @property
    def traceback(self) -> str:
        rv = self.base_traceback.format(
            line_nb=getattr(self, "line_nb", "?"),
            line=getattr(self, "line", ""),
            error=self.args[0],
        )
        if self.hint is not None:
            rv += f"\nHINT: {self.hint}"
        return rv


class DuplicateTableException(ParsingException):
    pass


class DuplicateColumnException(ParsingException):
    pass


class RelationNoColException(ParsingException):
    hint = "Try to declare the tables before the relationships."


class NoCurrentTableException(ParsingException):
    hint = "Try to declare the tables before the relationships and columns."


def remove_comments_from_line(line: str) -> str:
    if "#" not in line:
        return line.strip()
    return line[: line.index("#")].strip()


def filter_lines_from_comments(lines: list[str]) -> Iterator[tuple[int, str, str]]:
    """Filter the lines from comments and non code lines."""
    for line_nb, raw_line in enumerate(lines):
        clean_line = remove_comments_from_line(raw_line)
        if clean_line == "":
            continue
        yield line_nb, clean_line, raw_line


def parse_line(line: str) -> Drawable:
    for typ in TYPES:
        match = typ.RE.match(line)
        if match:
            return typ.make_from_match(match)
    msg = 'Line "{}" could not be parsed to an object.'
    raise ValueError(msg.format(line))


def _check_no_current_table(new_obj: Drawable, current_table: Table | None) -> None:
    """Raises exception if we try to add a relation or a column with no current table."""
    if current_table is None:
        msg = "Cannot add {} before adding table"
        if isinstance(new_obj, Relation):
            raise NoCurrentTableException(msg.format("relation"))
        if isinstance(new_obj, Column):
            raise NoCurrentTableException(msg.format("column"))


def _update_check_inputs(
    current_table: Table | None,
    tables: list[Table],
    relations: list[Relation],
) -> None:
    assert current_table is None or isinstance(current_table, Table)
    assert isinstance(tables, list)
    assert all(isinstance(t, Table) for t in tables)
    assert all(isinstance(r, Relation) for r in relations)
    assert current_table is None or current_table in tables


def _check_colname_in_lst(column_name: str, columns_names: list[str]) -> None:
    if column_name not in columns_names:
        msg = 'Cannot add a relation with column "{}" which is undefined'
        raise RelationNoColException(msg.format(column_name))


def _check_not_creating_duplicates(
    new_name: str,
    names: list[str],
    type: str,
    exc: type[Exception],
) -> None:
    if new_name in names:
        msg = f'Cannot add {type} named "{new_name}" which is already present in the schema.'
        raise exc(msg)


def update_models(
    new_obj,
    current_table: Table | None,
    tables: list[Table],
    relations: list[Relation],
) -> tuple[Table | None, list[Table], list[Relation]]:
    """Update the state of the parsing."""
    _update_check_inputs(current_table, tables, relations)
    _check_no_current_table(new_obj, current_table)

    if isinstance(new_obj, Table):
        tables_names = [t.name for t in tables]
        _check_not_creating_duplicates(
            new_obj.name,
            tables_names,
            "table",
            DuplicateTableException,
        )
        return new_obj, tables + [new_obj], relations

    if isinstance(new_obj, Relation):
        tables_names = [t.name for t in tables]
        _check_colname_in_lst(new_obj.right_table, tables_names)
        _check_colname_in_lst(new_obj.left_table, tables_names)
        return current_table, tables, relations + [new_obj]

    if isinstance(new_obj, Column):
        assert current_table
        columns_names = [c.name for c in current_table.columns]
        _check_not_creating_duplicates(
            new_obj.name,
            columns_names,
            "column",
            DuplicateColumnException,
        )
        current_table.columns.append(new_obj)
        return current_table, tables, relations

    msg = "new_obj cannot be of type {}"
    raise ValueError(msg.format(new_obj.__class__.__name__))


def markdown_file_to_intermediary(filename: str) -> tuple[list[Table], list[Relation]]:
    """Parse a file and return to intermediary syntax."""
    with open(filename) as f:
        lines = f.readlines()
    return line_iterator_to_intermediary(lines)


def line_iterator_to_intermediary(
    line_iterator: list[str],
) -> tuple[list[Table], list[Relation]]:
    """Parse an iterator of str (one string per line) to the intermediary syntax."""
    current_table = None
    tables: list[Table] = []
    relations: list[Relation] = []
    errors: list[ParsingException] = []
    for line_nb, line, raw_line in filter_lines_from_comments(line_iterator):
        try:
            new_obj = parse_line(line)
            current_table, tables, relations = update_models(
                new_obj,
                current_table,
                tables,
                relations,
            )
        except ParsingException as e:
            e.line_nb = line_nb  # type:ignore
            e.line = raw_line  # type:ignore
            errors.append(e)
    if len(errors) != 0:
        msg = f"eralchemy couldn't complete the generation due the {len(errors)} following errors"
        raise ParsingException(msg + "\n\n".join(e.traceback for e in errors))
    return tables, relations
