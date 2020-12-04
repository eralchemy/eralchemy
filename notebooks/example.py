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

from google.cloud.bigquery import Client
from eralchemy.main import (
    intermediary_to_schema,
    intermediary_to_markdown,
    intermediary_to_dot,
)

from bigquery_erd.bigquery import bigquery_to_intermediary
from bigquery_erd.utils import get_tables

client = Client()

tables, relations = bigquery_to_intermediary(
    list(
        get_tables(
            project_id="test-project-jjagusch", dataset_id="newsmeme", client=client
        )
    )
)

intermediary_to_schema(tables, relations, "../examples/newsmeme.png")
intermediary_to_markdown(tables, relations, "../examples/newsmeme.md")
intermediary_to_dot(tables, relations, "../examples/newsmeme.er")
