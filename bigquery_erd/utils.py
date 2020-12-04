"""
This module contains utilities for this project.
"""

from typing import Iterable, Optional, Iterator

from google.cloud.bigquery import Client, Table


def remove_duplicates(objs: Iterable) -> Iterable:
    """
    Removes duplicates from an interable.
    """
    memory = []
    for obj in objs:
        if obj not in memory:
            yield obj
            memory.append(obj)


def get_tables(
    project_id: str, client: Client, dataset_id: Optional[str] = None
) -> Iterator[Table]:
    """
    Gets BigQuery tables from a Google Cloud project.

    Args:
        project_id (str): ID of the project.
        dataset_id (Optional[str]): The ID of the dataset.
            If `None`, will retrieve tables from all datasets in project.
        client (Client): A Google Cloud Client instance.

    Yields:
        Table: A BigQuery table.
    """
    dataset_refs = (
        [f"{project_id}.{dataset_id}"]
        if dataset_id
        else (dataset.reference for dataset in client.list_datasets(project=project_id))
    )
    datasets = (client.get_dataset(dataset_ref) for dataset_ref in dataset_refs)
    for dataset in datasets:
        for table in client.list_tables(dataset):
            yield client.get_table(table)
