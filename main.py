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


def print_table(table):
    print('[{}]'.format(table.fullname))
    for _, col in table.c._data.iteritems():
        print('    {}{} {{label:"{}"}}'.format('*' if col.primary_key else '', col.name, col.type))
    print('')


def first_draft(metadata):
    for _, table in metadata.tables.iteritems():
        print_table(table)
    for _, table in metadata.tables.iteritems():
        for fk in table.foreign_keys:
            a = fk.parent.table.fullname
            b = fk._column_tokens[1]

            print("{} ?--* {}".format(a, b))


def base_to_graphviz(metadata):
    tables, relationships = metadata_to_intermediary(metadata)
    intermediary_to_graphviz(tables, relationships)


def base_to_er(metadata):
    tables, relationships = metadata_to_intermediary(metadata)
    intermediary_to_er(tables, relationships)
