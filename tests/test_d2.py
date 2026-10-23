import shutil
import subprocess

import pytest

from eralchemy import main
from eralchemy.cst import config, d2_layout, reset_config
from eralchemy.main import (
    get_output_mode,
    intermediary_to_d2,
    intermediary_to_d2_image,
    line_iterator_to_intermediary,
    render_er,
)
from eralchemy.models import Column, Relation, Table, d2_key, quote_d2
from tests.common import relationships, tables

ZWSP = "​"


@pytest.fixture(autouse=True)
def _reset_config():
    yield
    reset_config()


def test_quote_d2():
    assert quote_d2("label") == '"label"'
    assert quote_d2("public.users") == '"public.users"'
    assert quote_d2('a"b\\c') == '"a\\"b\\\\c"'
    assert quote_d2("a\nb") == '"a\\nb"'


def test_d2_key_avoids_keywords_and_case_collisions():
    taken: set[str] = set()
    assert d2_key("users", taken) == "users"
    assert d2_key("Users", taken) == "Users" + ZWSP
    assert d2_key("USERS", taken) == "USERS" + ZWSP * 2
    assert d2_key("Shape", taken) == "Shape" + ZWSP
    assert d2_key("layers", taken) == "layers" + ZWSP


def test_d2_column_marks_pk_and_fk():
    column = Column(name="association_id", type="UUID", is_key=True, is_foreign_key=True)
    assert column.to_d2() == '  "association_id": "UUID" {constraint: [primary_key; foreign_key]}'


def test_d2_column_without_constraint_or_type():
    assert Column(name="name", type="VARCHAR(255)").to_d2() == '  "name": "VARCHAR(255)"'
    assert Column(name="name").to_d2() == '  "name": ""'


def test_d2_table():
    table = Table(name="parent", columns=[Column(name="id", type="INTEGER", is_key=True)])
    assert table.to_d2() == (
        '"parent": {\n  shape: sql_table\n  "id": "INTEGER" {constraint: [primary_key]}\n}'
    )


def test_d2_table_keeps_columns_apart():
    table = Table(
        name="t", columns=[Column(name="ID", type="INTEGER"), Column(name="id", type="TEXT")]
    )
    assert table.d2_column_keys() == {"ID": "ID", "id": "id" + ZWSP}


def test_d2_relation_uses_crowfoot_arrowheads():
    relation = Relation(
        left_table="s.child",
        left_column="parent_id",
        right_table="s.parent",
        right_column="id",
        left_cardinality="*",
        right_cardinality="1",
    )
    assert relation.to_d2() == (
        '"s.child"."parent_id" <-> "s.parent"."id": {\n'
        "  source-arrowhead.shape: cf-many\n"
        "  target-arrowhead.shape: cf-one-required\n"
        "}"
    )


def test_d2_relation_without_cardinality():
    relation = Relation(
        left_table="child",
        right_table="parent",
        left_cardinality="",
        right_cardinality="",
    )
    assert relation.to_d2() == '"child" -- "parent"'


def test_intermediary_to_d2():
    d2 = intermediary_to_d2(tables, relationships, title="Forum").decode()
    assert d2.startswith(config["D2_CONFIG"] + "\n")
    assert '"title": "Forum" {\n  shape: text\n  near: top-center\n}\n' in d2
    for table in tables:
        assert table.to_d2() in d2
    for relation in relationships:
        assert relation.to_d2() in d2


def test_intermediary_to_d2_title_does_not_take_a_table():
    d2 = intermediary_to_d2([Table(name="title", columns=[])], [], title="T").decode()
    assert '"title": "T"' in d2
    assert f'"title{ZWSP}": {{\n      shape: sql_table\n    }}' in d2


def test_intermediary_to_d2_puts_unlinked_tables_in_a_grid():
    lone = Table(name="lone", columns=[Column(name="id", type="INTEGER")])
    taller = Table(name="taller", columns=[Column(name="id"), Column(name="name")])
    d2 = intermediary_to_d2([*tables, lone, taller], relationships).decode()
    grid = d2[d2.index('"unlinked": "" {') :]
    assert "near: bottom-center" in grid
    assert grid.index('"taller"') < grid.index('"lone"')
    for table in tables:
        assert table.to_d2() in d2[: d2.index('"unlinked"')]

    alone = intermediary_to_d2([lone], []).decode()
    assert '"unlinked": "" {' in alone
    assert "near:" not in alone


def test_intermediary_to_d2_drops_missing_endpoints():
    parent = Table(name="parent", columns=[Column(name="id", type="INTEGER")])
    child = Table(name="child", columns=[Column(name="id", type="INTEGER")])
    excluded_column = Relation(
        left_table="child",
        left_column="parent_id",
        right_table="parent",
        right_column="id",
        left_cardinality="*",
        right_cardinality="1",
    )
    excluded_table = Relation(
        left_table="ghost",
        right_table="parent",
        left_cardinality="*",
        right_cardinality="1",
    )
    d2 = intermediary_to_d2([parent, child], [excluded_column, excluded_table]).decode()
    assert '"child" <-> "parent"."id"' in d2
    assert "ghost" not in d2
    assert "parent_id" not in d2


def test_d2_layout():
    d2_layout("elk")
    assert "layout-engine: elk" in intermediary_to_d2(tables, relationships).decode()
    config["D2_CONFIG"] = ""
    assert intermediary_to_d2(tables, relationships).decode().startswith('"parent"')


@pytest.mark.skipif(shutil.which("d2") is None, reason="d2 is not installed")
def test_d2_compiles(tmp_path):
    markdown = """
        [Users]
            *id {label:"INTEGER"}
            Shape {label:"VARCHAR(255) # not a comment"}
        [users]
            *ID {label:"INTEGER"}
            id {label:"TEXT"}
        [layers]
            *id {label:"INTEGER"}
            users_id {label:"INTEGER"}
        layers."users_id" *--1 Users."id"
        """
    d2_tables, d2_relationships = line_iterator_to_intermediary(markdown.splitlines())
    source = tmp_path / "erd.d2"
    source.write_bytes(intermediary_to_d2(d2_tables, d2_relationships, title='A "title"\n2'))
    subprocess.run(["d2", str(source), str(tmp_path / "erd.svg")], check=True)


def test_get_output_mode_renders_d2_images():
    assert get_output_mode(None, "d2") == intermediary_to_d2
    assert get_output_mode("erd.d2", "d2") == intermediary_to_d2
    assert get_output_mode("erd", "d2") == intermediary_to_d2
    mode = get_output_mode("erd.svg", "d2")
    assert mode.func == intermediary_to_d2_image
    assert mode.keywords == {"extension": "svg"}


def test_get_output_mode_uses_d2_without_graphviz(monkeypatch):
    monkeypatch.setattr(main, "GRAPHVIZ_AVAILABLE", False)
    monkeypatch.setattr(main.shutil, "which", lambda _: "/usr/bin/d2")
    assert get_output_mode("erd.svg", "auto").func == intermediary_to_d2_image


def test_d2_image_needs_d2(monkeypatch):
    monkeypatch.setattr(main.shutil, "which", lambda _: None)
    with pytest.raises(FileNotFoundError, match="d2 is not installed"):
        intermediary_to_d2_image(tables, relationships)


@pytest.mark.skipif(shutil.which("d2") is None, reason="d2 is not installed")
def test_render_er_to_d2_svg(tmp_path):
    output = tmp_path / "erd.svg"
    render_er(["[parent]", '    *id {label:"INTEGER"}'], str(output), mode="d2")
    assert output.read_bytes().startswith(b"<?xml")
