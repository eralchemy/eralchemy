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
}
