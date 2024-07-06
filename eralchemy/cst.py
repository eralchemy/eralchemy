"""All the constants used in the module."""

TABLE = (
    '"{}" [label=<<FONT FACE="Helvetica"><TABLE BORDER="0" CELLBORDER="1"'
    ' CELLPADDING="4" CELLSPACING="0">{}{}</TABLE></FONT>>];'
)

START_CELL = '<TR><TD ALIGN="LEFT"><FONT>'
FONT_TAGS = "<FONT>{}</FONT>"
# Used for each row in the table.
ROW_TAGS = "<TR><TD{}>{}</TD></TR>"
DOT_GRAPH_BEGINNING = """
      graph {
         graph [rankdir=LR];
         node [label="\\N",
             shape=plaintext
         ];
         edge [color=gray50,
             minlen=2,
             style=dashed
         ];
      """
ER_FORMAT_TITLE = 'title {{label: "{}", size: "40"}}'
