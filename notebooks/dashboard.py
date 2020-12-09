# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: bigquery-erd
#     language: python
#     name: bigquery-erd
# ---

from copy import copy
from tempfile import NamedTemporaryFile

from google.cloud.bigquery import Client
from bigquery_erd import bigquery_to_intermediary
from bigquery_erd.utils import get_tables
from eralchemy.main import intermediary_to_dot
from IPython.display import Image
from pygraphviz import AGraph
import panel as pn

pn.extension()

CLIENT = Client()

TABLES = list(get_tables("test-project-jjagusch", dataset_id="newsmeme", client=CLIENT))

intermediary = bigquery_to_intermediary(TABLES)


# +
def _repr_svg_(self):
    # possible values for prog: neato|dot|twopi|circo|fdp|nop
    return self.draw(format='svg', prog="dot").decode(self.encoding)

AGraph._repr_svg_ = _repr_svg_


# +
def filter_intermediary(intermediary, filter_datasets=None, filter_tables=None, filter_relations=None):
    tables, relations = intermediary
    if filter_datasets:
        tables = [table for table in tables if table.name.split(".")[0] in filter_datasets]
    if filter_tables:
        filter_table_names = set(table.name for table in filter_tables)
        tables = [table for table in tables if table.name in filter_table_names]
    if filter_relations:
        relations = [relation for relation in relations if relation in filter_relations]
    table_names = set(table.name for table in tables)
    relations = [relation for relation in relations if relation.left_col in table_names and relation.right_col in table_names]
    
    return tables, relations

def remove_columns(tables):
    def make_empty_table(table):
        empty_table = copy(table)
        empty_table.columns = []
        return empty_table

    return [make_empty_table(table) for table in tables]    


# -

tables, relations = intermediary
datasets = list(set(table.name.split(".")[0] for table in intermediary[0]))


def render_intermediary(intermediary):
    with NamedTemporaryFile() as tf:
        intermediary_to_dot(*intermediary, tf.name)
        return AGraph(tf.name)


# +
select_datasets = pn.widgets.MultiSelect(name='Select Datasets', value=datasets, options=datasets, height=200)
select_tables = pn.widgets.MultiSelect(name="Select Tables", value=tables, options=tables, height=200)
select_relations = pn.widgets.MultiSelect(name="Select Relations", value=relations, options=relations, height=200)

pane_graph = pn.Pane(render_intermediary(intermediary))
check_show_columns = pn.widgets.Checkbox(name="Show Columns", value=True)


# +
@pn.depends(select_datasets, watch=True)
def update_tables(datasets):
    select_tables.value = [table for table in select_tables.value if table.name.split(".")[0] in datasets]
    
@pn.depends(select_tables, watch=True)
def update_relations(tables):
    table_names = set(table.name for table in tables)
    select_relations.value = [relation for relation in select_relations.value if relation.left_col in table_names and relation.right_col in table_names]
    
@pn.depends(select_datasets, select_tables, select_relations, check_show_columns, watch=True)
def update_graph(*args):
    tables, relations = intermediary
    if not check_show_columns.value:
        tables = remove_columns(tables)
    pane_graph.object = render_intermediary(filter_intermediary((tables, relations), filter_datasets=select_datasets.value, filter_tables=select_tables.value, filter_relations=select_relations.value))


# -

pn.Column(pn.Row(select_datasets, select_tables, select_relations, check_show_columns), pane_graph)


