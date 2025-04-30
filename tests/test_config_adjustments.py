from eralchemy import render_er
from eralchemy.cst import config, dot_star_primary, dot_top_down, reset_config


def render_dot():
    reset_config()
    assert config["DOT_KEY_OPENING"] == "<u>"
    assert config["DOT_KEY_CLOSING"] == "</u>"
    assert "rankdir=LR" in config["DOT_GRAPH_BEGINNING"]
    output = render_er("../example/forum.er", output=None, mode="dot").decode("utf-8")
    assert "<u><FONT>id</FONT></u> " in output

    with open("expected_plain_output.dot") as f:
        expected = f.read()
    assert expected == output


def render_dot_with_config():
    reset_config()
    dot_star_primary()
    assert config["DOT_KEY_OPENING"] == "*"
    assert config["DOT_KEY_CLOSING"] == ""
    output = render_er("../example/forum.er", output=None, mode="dot").decode("utf-8")
    assert "*<FONT>id</FONT> " in output

    with open("expected_star_primary_output.dot") as f:
        expected = f.read()
    assert expected == output


def reder_dot_top_down():
    reset_config()
    dot_top_down()
    assert "rankdir=TB" in config["DOT_GRAPH_BEGINNING"]
    output = render_er("../example/forum.er", output=None, mode="dot").decode("utf-8")
    assert "rankdir=TB" in output
