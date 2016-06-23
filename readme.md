# Entity relation diagrams generator

[![Join the chat at https://gitter.im/Alexis-benoist/eralchemy](https://badges.gitter.im/Alexis-benoist/eralchemy.svg)](https://gitter.im/Alexis-benoist/eralchemy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

ERAlchemy generates Entity Relation (ER) diagram (like the one below) from databases or from SQLAlchemy models.

## Example

![Example for a graph](https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/newsmeme.png?raw=true "Example for NewsMeme")

[Example for NewsMeme](https://bitbucket.org/danjac/newsmeme)

## Quick Start

### Install on a mac
The simplest way to install eralchemy on OSX is by using [Homebrew](http://brew.sh)

    $ brew install eralchemy

### Install
To install ERAlchemy, just do:

    $ pip install eralchemy

`ERAlchemy` requires [GraphViz](http://www.graphviz.org/Download.php) to generate the graphs and Python. Both are available for Windows, Mac and Linux.

### Use from the command line and a database

    $ eralchemy -i sqlite:///relative/path/to/db.db -o erd_from_sqlite.pdf

The database is specified as a [SQLAlchemy](http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#database-urls)
database url.

### Use from the command line and a markdown file.

    $ curl 'https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/example/newsmeme.er' > markdown_file.er
    $ eralchemy -i 'markdown_file.er' -o erd_from_markdown_file.pdf

### Use from python
```python
from eralchemy import render_er
## Draw from SQLAlchemy base
render_er(Base, 'erd_from_sqlalchemy.png')

## Draw from database
render_er("sqlite:///relative/path/to/db.db", 'erd_from_sqlite.png')
```

### Use from the command line with a Postgresql database to a markdown file excluding tables named `temp` and `audit`

    $ eralchemy -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -o filtered.er -x temp audit

### Use from the command line with a Postgresql database to a markdown file for the schema `schema`

    $ eralchemy -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -s schema

## Architecture
![Architecture schema](https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/eralchemy_architecture.png?raw=true "Architecture schema")

Thanks to it's modular architecture, it can be connected to other ORMs/ODMs/OGMs/O*Ms.

## Contribute

Every feedback is welcome on the [GitHub issues](https://github.com/Alexis-benoist/eralchemy/issues).

To run the tests, use : `$ py.test`.
Some tests require a local postgres database with a schema named test in a database
named test all owned by a user named postgres with a password of postgres.

All tested PR are welcome.

## Notes

ERAlchemy was inspired by [erd](https://github.com/BurntSushi/erd), though it is able to render the ER diagram directly
from the database and not just only from the `ER` markup language.

Released under an Apache License 2.0

Creator: Alexis Benoist [@Alexis_Benoist](https://twitter.com/Alexis_Benoist)
