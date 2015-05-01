# -*- coding: utf-8 -*-

"""
All the constants used in the module.
"""
TABLE = '{} [label=<<FONT FACE="Helvetica"><TABLE BORDER="0" CELLBORDER="1"' \
        ' CELLPADDING="4" CELLSPACING="0">{}{}</TABLE></FONT>>];'

START_CELL = '<TR><TD ALIGN="LEFT"><FONT>'
FONT_TAGS = '<FONT>{}</FONT>'
RAW_TAGS = '<TR><TD{}>{}</TD></TR>'
GRAPH_BEGINING = """
    graph {
	graph [rankdir=LR];
	node [label="\N",
		shape=plaintext
	];
	edge [color=gray50,
		minlen=2,
		style=dashed
	];
	"""