
[![PyPI Version](https://img.shields.io/pypi/v/eralchemy2.svg)](
https://pypi.org/project/eralchemy2/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/eralchemy2.svg)](
https://pypi.org/project/eralchemy2/)
![Github Actions](https://github.com/maurerle/eralchemy2/actions/workflows/python-app.yml/badge.svg)


# Entity relation diagrams generator

eralchemy2 generates Entity Relation (ER) diagram (like the one below) from databases or from SQLAlchemy models.
Works with SQLAlchemy < 1.4 but also with versions greater than 1.4

## Example

![Example for a graph](https://raw.githubusercontent.com/maurerle/eralchemy2/main/newsmeme.svg?raw=true "Example for NewsMeme")

[Example for NewsMeme](https://bitbucket.org/danjac/newsmeme)

## Quick Start

### Install
To install eralchemy2, just do:

    $ pip install eralchemy2

`eralchemy2` requires [GraphViz](http://www.graphviz.org/download) to generate the graphs and Python. Both are available for Windows, Mac and Linux.

### Usage from Command Line

#### From a database

    $ eralchemy2 -i sqlite:///relative/path/to/db.db -o erd_from_sqlite.pdf

The database is specified as a [SQLAlchemy](http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#database-urls)
database url.

#### From a markdown file.

    $ curl 'https://raw.githubusercontent.com/maurerle/eralchemy2/main/example/newsmeme.er' > markdown_file.er
    $ eralchemy2 -i 'markdown_file.er' -o erd_from_markdown_file.pdf

#### From a Postgresql DB to a markdown file excluding tables named `temp` and `audit`

    $ eralchemy2 -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -o filtered.er --exclude-tables temp audit

#### From a Postgresql DB to a markdown file excluding columns named `created_at` and `updated_at` from all tables

    $ eralchemy2 -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -o filtered.er --exclude-columns created_at updated_at

#### From a Postgresql DB to a markdown file for the schema `schema`

    $ eralchemy2 -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -s schema

### Usage from Python

```python
from eralchemy2 import render_er
## Draw from SQLAlchemy base
render_er(Base, 'erd_from_sqlalchemy.png')

## Draw from database
render_er("sqlite:///relative/path/to/db.db", 'erd_from_sqlite.png')
```

## Architecture
![Architecture schema](https://raw.githubusercontent.com/maurerle/eralchemy2/main/eralchemy_architecture.png?raw=true "Architecture schema")

Thanks to it's modular architecture, it can be connected to other ORMs/ODMs/OGMs/O*Ms.

## Contribute

Every feedback is welcome on the [GitHub issues](https://github.com/maurerle/eralchemy2/issues).

To run the tests, use : `$ py.test` or `$ tox`.
Some tests require a local postgres database with a schema named test in a database
named test all owned by a user named eralchemy with a password of eralchemy.
This can be easily set up using docker-compose with: `docker-compose up -d`.

All tested PR are welcome.

## Notes

eralchemy2 is a fork of its predecessor [ERAlchemy](https://github.com/Alexis-benoist/eralchemy) by @Alexis-benoist, which is not maintained anymore and does not work with SQLAlchemy > 1.4.
If it is maintained again, I'd like to push the integrated changes upstream.

ERAlchemy was inspired by [erd](https://github.com/BurntSushi/erd), though it is able to render the ER diagram directly
from the database and not just only from the `ER` markup language.

Released under an Apache License 2.0

Initial Creator: Alexis Benoist [Alexis_Benoist](https://twitter.com/Alexis_Benoist)
