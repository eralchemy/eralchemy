from eralchemy.models import sanitize_mermaid


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
