# -*- coding: utf-8 -*-
from cst import GRAPH_BEGINING
from sqla import metadata_to_intermediary


def intermediary_to_er(tables, relationships):
    for t in tables:
        print t.to_er()

    for r in relationships:
        print r.to_er()


def intermediary_to_graphviz(tables, relationships):
    print GRAPH_BEGINING
    for t in tables:
        print t.to_graphviz()

    for r in relationships:
        print r.to_graphviz()
    print '}'


def base_to_graphviz(metadata):
    tables, relationships = metadata_to_intermediary(metadata)
    intermediary_to_graphviz(tables, relationships)


def base_to_er(metadata):
    tables, relationships = metadata_to_intermediary(metadata)
    intermediary_to_er(tables, relationships)
