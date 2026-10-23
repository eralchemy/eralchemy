"""All the constants used in the module."""

DOT_TABLE = (
    '"{}" [label=<<FONT FACE="Helvetica"><TABLE BORDER="0" CELLBORDER="1"'
    ' CELLPADDING="4" CELLSPACING="0">{}{}</TABLE></FONT>>];'
)
DOT_FONT_TAGS = "<FONT>{}</FONT>"
# Used for each row in the table.
DOT_ROW_TAGS = "<TR><TD{}>{}</TD></TR>"
DOT_GRAPH_BEGINNING = """graph {
    graph [rankdir=LR];
    node [label="\\N",
        shape=plaintext
    ];
    edge [color=gray50,
        minlen=2,
        style=dashed
    ];"""
MARKDOWN_TITLE = 'title {{label: "{}", size: "40"}}'
# Written at the top of D2 output. TALA is bundled with D2 since v0.9.0.
# Any D2 can go here, see "Configuration variables" in https://d2lang.com/tour/vars
D2_CONFIG = """vars: {
  d2-config: {
    layout-engine: tala
  }
}"""

DEFAULT_CONFIG = {
    "DOT_TABLE": DOT_TABLE,
    "DOT_FONT_TAGS": DOT_FONT_TAGS,
    "DOT_ROW_TAGS": DOT_ROW_TAGS,
    "DOT_GRAPH_BEGINNING": DOT_GRAPH_BEGINNING,
    "MARKDOWN_TITLE": MARKDOWN_TITLE,
    "D2_CONFIG": D2_CONFIG,
    "DOT_KEY_OPENING": "<u>",
    "DOT_KEY_CLOSING": "</u>",
    "DOT_RELATION_GRAPH": "graph",
    "DOT_RELATION_STYLE": "",
}

config = DEFAULT_CONFIG.copy()


def dot_star_primary():
    config["DOT_KEY_OPENING"] = "*"
    config["DOT_KEY_CLOSING"] = ""


def dot_star_underline():
    config["DOT_KEY_OPENING"] = "<u>"
    config["DOT_KEY_CLOSING"] = "</u>"


def dot_top_down():
    config["DOT_GRAPH_BEGINNING"] = config["DOT_GRAPH_BEGINNING"].replace(
        "rankdir=LR", "rankdir=TB"
    )


def dot_left_right():
    config["DOT_GRAPH_BEGINNING"] = config["DOT_GRAPH_BEGINNING"].replace(
        "rankdir=TB", "rankdir=LR"
    )


def dot_digraph():
    config["DOT_GRAPH_BEGINNING"] = config["DOT_GRAPH_BEGINNING"].replace("graph {", "digraph {")
    config["DOT_RELATION_GRAPH"] = "digraph"


def dot_crowfoot():
    config["DOT_RELATION_STYLE"] = "crow"


def d2_layout(engine: str):
    config["D2_CONFIG"] = D2_CONFIG.replace("tala", engine)


def reset_config():
    for key, value in DEFAULT_CONFIG.items():
        config[key] = value
