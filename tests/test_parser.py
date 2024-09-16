import pytest

from eralchemy.main import _intermediary_to_markdown
from eralchemy.models import Column, Relation, Table
from eralchemy.parser import (
    DuplicateColumnException,
    DuplicateTableException,
    NoCurrentTableException,
    ParsingException,
    RelationNoColException,
    line_iterator_to_intermediary,
    parse_line,
    remove_comments_from_line,
    update_models,
)
from tests import common as c

# examples from https://github.com/BurntSushi/erd/blob/master/examples/nfldb.er
table_lst = [
    "[player]",
    "[team]",
    "[game]",
    "[drive]",
]

relations_lst = [
    "player      *--1 team",
    "game        *--1 team",
    "game        *--* team",
    "drive       1--1 team",
    "play        ?--1 team",
    "play_player *--+ team",
]

columns_lst = [
    # '*+gsis_id', # TODO add fk
    # '*+drive_id',
    "*play_id",
    "time",
    "pos_team",
    "yardline",
    "down",
    "yards_to_go",
]
elements_lst = table_lst + relations_lst + columns_lst


def test_remove_from_lines():
    r = remove_comments_from_line
    for code in elements_lst:
        assert r(code) == code
        assert r(f"{code} ## some comment") == code
        assert r(f"   {code}") == code
        assert r(f"{code}   ") == code
        assert r(f"{code} ## some comment") == code
        assert r(f"{code} #  # some comment") == code
        assert r(f"   {code} #  # some comment") == code
        assert r(f"{code}") == code
        assert r(f"#{code} #  # some comment") == ""
        assert r(f"# #{code} #  # some comment") == ""
        assert r(f"##{code}") == ""


def test_parse_line_type():
    col = parse_line('parent_id {label:"INTEGER"}')
    assert col.type == "INTEGER"


def test_parse_line():
    for s in columns_lst:
        rv = parse_line(s)
        assert rv.name == s.replace("*", "")
        assert isinstance(rv, Column)

    for s in relations_lst:
        rv = parse_line(s)  # type: Relation
        assert rv.right_table == s[16:].strip()
        assert rv.right_column == ""
        assert rv.left_table == s[:12].strip()
        assert rv.left_column == ""
        assert rv.right_cardinality == s[15]
        assert rv.left_cardinality == s[12]
        assert isinstance(rv, Relation)

    for s in table_lst:
        rv = parse_line(s)
        assert rv.name == s[1:-1]
        assert rv.columns == []
        assert isinstance(rv, Table)


def test_update_models_fails_no_current_table():
    for new_obj in (c.relation, c.parent_id):
        with pytest.raises(NoCurrentTableException):
            update_models(new_obj, None, [], [])


def test_update_models_fails_relation_no_col():
    with pytest.raises(RelationNoColException):
        update_models(
            new_obj=c.relation,
            current_table=c.parent,
            tables=[c.parent],
            relations=[],
        )


def test_update_models_fails_duplicate_col():
    with pytest.raises(DuplicateColumnException):
        update_models(
            new_obj=c.parent_name,
            current_table=c.parent,
            tables=[c.parent],
            relations=[],
        )


def test_update_models_fails_duplicate_table():
    with pytest.raises(DuplicateTableException):
        update_models(
            new_obj=c.parent,
            current_table=c.parent,
            tables=[c.parent],
            relations=[],
        )


def test_update_models_add_relation():
    current_table, tables, relations = update_models(
        new_obj=c.relation,
        current_table=c.parent,
        tables=[c.parent, c.child],
        relations=[],
    )
    assert c.relation in relations


def test_update_models_add_table():
    current_table, tables, relations = update_models(
        new_obj=c.child,
        current_table=c.parent,
        tables=[
            c.parent,
        ],
        relations=[],
    )
    assert c.child in tables


def test_update_models_new_obj_bad_class():
    with pytest.raises(ValueError):
        update_models(
            new_obj=c.Child,
            current_table=c.parent,
            tables=[
                c.parent,
            ],
            relations=[],
        )


def test_update_models_add_column():
    parent = Table(
        name="parent",
        columns=[c.parent_id],
    )
    current_table, tables, relations = update_models(
        new_obj=c.parent_name,
        current_table=parent,
        tables=[
            parent,
        ],
        relations=[],
    )
    assert c.parent_name in current_table.columns
    assert c.parent_name in tables[0].columns


def test_integration_parser():
    tables, relations = line_iterator_to_intermediary(c.markdown.split("\n"))
    c.assert_lst_equal(tables, c.tables)
    c.assert_lst_equal(relations, [c.relation, c.exclude_relation])


def test_generate_and_parse():
    markdown = _intermediary_to_markdown(c.tables, [c.relation])
    tables, relations = line_iterator_to_intermediary(markdown.split("\n"))
    c.assert_lst_equal(tables, c.tables)
    c.assert_lst_equal(relations, [c.relation])


def test_integration_errors():
    markdown_broken = """
            name {label:"VARCHAR(255)"}
        [child]
            *id {label:"INTEGER"}
            parent_id {label:"INTEGER"}
        parent *--? child
        """
    with pytest.raises(ParsingException):
        line_iterator_to_intermediary(markdown_broken.split("\n"))
    # TODO check error
