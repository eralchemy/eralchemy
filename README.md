[![license](https://img.shields.io/badge/License-Apache%202.0-yellow?logo=opensourceinitiative&logoColor=white)](LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/eralchemy?logo=pypi&logoColor=white)](https://pypi.org/project/ERAlchemy/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/eralchemy?logo=pypi&logoColor=white)](https://pypi.org/project/eralchemy/)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/eralchemy/eralchemy/unit.yaml?logo=github&logoColor=white)](https://github.com/eralchemy/eralchemy/actions/workflows/unit.yaml)
[![Codecov](https://img.shields.io/codecov/c/github/eralchemy/eralchemy?logo=codecov&logoColor=white)](https://app.codecov.io/gh/eralchemy/eralchemy)

# Entity relation diagrams generator

eralchemy generates Entity Relation (ER) diagram (like the one below) from databases or from SQLAlchemy models.

## Example

![Example for a graph](https://raw.githubusercontent.com/eralchemy/eralchemy/main/docs/_static/forum.svg "Example for a simple Forum")

## Quick Start

### Install

To install eralchemy, just do:

    $ pip install eralchemy

### Graph library flavors

To create Pictures and PDFs, eralchemy relies on either graphviz or pygraphviz.

You can use either

    $ pip install eralchemy[graphviz]

or

    $ pip install eralchemy[pygraphviz]

to retrieve the correct dependencies.
The `graphviz` library is the default if both are installed.

`eralchemy` requires [GraphViz](http://www.graphviz.org/download) to generate the graphs and Python. Both are available for Windows, Mac and Linux.

For Debian based systems, run:

    $ apt install graphviz libgraphviz-dev

before installing eralchemy.

### Install using conda

There is also a packaged version in conda-forge, which directly installs the dependencies:

    $ conda install -c conda-forge eralchemy

### Usage from Command Line

#### From a database

    $ eralchemy -i sqlite:///relative/path/to/db.db -o erd_from_sqlite.pdf

The database is specified as a [SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)
database url.

#### From a markdown file.

    $ curl 'https://raw.githubusercontent.com/eralchemy/eralchemy/main/example/forum.er' > markdown_file.er
    $ eralchemy -i 'markdown_file.er' -o erd_from_markdown_file.pdf

#### From a Postgresql DB to a markdown file excluding tables named `temp` and `audit`

    $ eralchemy -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -o filtered.er --exclude-tables temp audit

#### From a Postgresql DB to a markdown file excluding columns named `created_at` and `updated_at` from all tables

    $ eralchemy -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -o filtered.er --exclude-columns created_at updated_at

#### From a Postgresql DB to a markdown file for the schemas `schema1` and `schema2`

    $ eralchemy -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -s "schema1, schema2"

#### Specify Output Mode

    $ eralchemy -i 'markdown_file.er' -o erd_from_markdown_file.md -m mermaid_er

### Usage from Python

```python
from eralchemy import render_er
## Draw from SQLAlchemy base
render_er(Base, 'erd_from_sqlalchemy.png')

## Draw from database
render_er("sqlite:///relative/path/to/db.db", 'erd_from_sqlite.png')
```

## Architecture

![Architecture schema](https://raw.githubusercontent.com/eralchemy/eralchemy/main/docs/_static/eralchemy_architecture.png "Architecture schema")

Thanks to it's modular architecture, it can be connected to other ORMs/ODMs/OGMs/O\*Ms.

## Contribute

Every feedback is welcome on the [GitHub issues](https://github.com/eralchemy/eralchemy/issues).

### Development

Install the development dependencies using

    $ pip install -e .[ci,dev]

Make sure to run the pre-commit to fix formatting

    $ pre-commit run --all

All tested PR are welcome.

## Running tests

This project uses the pytest test suite.
To run the tests, use : `$ pytest` or `$ tox`.

Some tests require having a local PostgreSQL database with a schema named test in a database
named test all owned by a user named eralchemy with a password of eralchemy.
If docker compose is available, one can use `docker compose up -d` for this purpose.
You can deselect the tests which require a PostgreSQL database using:

    $ pytest -m "not external_db"

## Publishing a release

    $ rm -r dist && python -m build && python3 -m twine upload --repository pypi dist/*

## Notes

ERAlchemy was inspired by [erd](https://github.com/BurntSushi/erd), though it is able to render the ER diagram directly
from the database and not just only from the `ER` markup language.

Released under an Apache License 2.0
