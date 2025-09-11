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

config = {
    "DOT_TABLE": DOT_TABLE,
    "DOT_FONT_TAGS": DOT_FONT_TAGS,
    "DOT_ROW_TAGS": DOT_ROW_TAGS,
    "DOT_GRAPH_BEGINNING": DOT_GRAPH_BEGINNING,
    "MARKDOWN_TITLE": MARKDOWN_TITLE,
    "DOT_KEY_OPENING": "<u>",
    "DOT_KEY_CLOSING": "</u>",
}


def dot_star_primary():
    config["DOT_KEY_OPENING"] = "*"
    config["DOT_KEY_ClOSING"] = ""


def dot_star_underline():
    config["DOT_KEY_OPENING"] = "<u>"
    config["DOT_KEY_ClOSING"] = "</u>"


def dot_top_down():
    config["DOT_GRAPH_BEGINNING"] = config["DOT_GRAPH_BEGINNING"].replace(
        "rankdir=LR", "rankdir=TD"
    )


def dot_left_right():
    config["DOT_GRAPH_BEGINNING"] = config["DOT_GRAPH_BEGINNING"].replace(
        "rankdir=TD", "rankdir=LR"
    )
