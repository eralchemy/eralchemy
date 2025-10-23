from eralchemy.models import Column, sanitize_mermaid


def test_mermaid_escape():
    assert "0" == sanitize_mermaid("0")
    assert "_0" == sanitize_mermaid("0", is_er=True)
    assert "_-" == sanitize_mermaid("-", is_er=True)
    assert "-" == sanitize_mermaid("-")
    assert "left_right" == sanitize_mermaid("left/right")
    assert "test" == sanitize_mermaid("test")
    assert "test7" == sanitize_mermaid("test7", is_er=True)
    assert "public_table_column" == sanitize_mermaid("public.table.column")
    assert "public_table_column" == sanitize_mermaid("public%table!column")


def test_mermaid_er_column_marks_fk():
    column = Column(name="parent_id", type="INTEGER", is_foreign_key=True)
    result = column.to_mermaid_er()
    assert result == " INTEGER parent_id FK"


def test_mermaid_er_column_marks_pk_and_fk():
    column = Column(name="association_id", type="UUID", is_key=True, is_foreign_key=True)
    result = column.to_mermaid_er()
    assert result == " UUID association_id PK, FK"
