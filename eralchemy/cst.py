"""All the constants used in the module."""

TABLE = (
    '"{}" [label=<<FONT FACE="Helvetica"><TABLE BORDER="0" CELLBORDER="1"'
    ' CELLPADDING="4" CELLSPACING="0">{}{}</TABLE></FONT>>];'
)

START_CELL = '<TR><TD ALIGN="LEFT"><FONT>'
FONT_TAGS = "<FONT>{}</FONT>"
# Used for each row in the table.
ROW_TAGS = "<TR><TD{}>{}</TD></TR>"
DOT_GRAPH_BEGINNING = (
    " digraph {\n"
    "    graph [rankdir=LR];\n"
    '    node [label="\\N",\n'
    "        shape=plain\n"
    "    ];\n"
    "    edge [color=gray50,\n"
    "        minlen=2,\n"
    "        style=solid\n"
    "    ];\n"
)
ER_FORMAT_TITLE = 'title {{label: "{}", size: "40"}}'
