# Entity relation diagrams generator

ERAlchemy generates Entity Relation (ER) diagram (like the one below) from databases or from SQLAlchemy models.

## Example
### Simple
![Example for a graph](https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/graph_example.png?raw=true "Example for a graph")
### Complex
![Example for a graph](https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/newsmeme.png?raw=true "Example for NewsMeme")
[Example for NewsMeme](https://bitbucket.org/danjac/newsmeme)

## Quick Start 
### Install
To install ERAlchemy, just do:

    $ pip install eralchemy
    
`ERAlchemy` requires [GraphViz](http://www.graphviz.org/Download.php) to generate the graphs.

### Use from python
```python
from eralchemy import render_er
## Draw from SQLAlchemy base
render_er(Base, 'erd_from_sqlalchemy.png')

## Draw from database
render_er("sqlite:///relative/path/to/db.db", 'erd_from_sqlite.png')
``` 

### Use from the command line

    $ eralchemy -i sqlite:///relative/path/to/db.db -o erd_from_sqlite.png


## Architecture
![Architecture schema](https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/eralchemy_architecture.png?raw=true "Architecture schema")

Thanks to it's modular architecture, it can be connected to other ORMs/ODMs/OGMs/O*Ms.

## Notes
Every feedback is welcome on the [GitHub issues](https://github.com/Alexis-benoist/eralchemy/issues).

To run the tests, use : `$ py.test`.

ERAlchemy was inspired by [erd](https://github.com/BurntSushi/erd), though it is able to render the ER diagram directly 
from the database and not just only from the `ER` markup language.

Released under an Apache License 2.0

Creator: Alexis Benoist [@Alexis_Benoist](https://twitter.com/Alexis_Benoist)
