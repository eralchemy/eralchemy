# ERAlchemy: Simple entity relation (ER) diagrams generation.

It's now integrated with SQLAlchemy.

It's also able to generate the ER digram from an existing database.


# Quick Start 
## Use from python
```python
from eralchemy import draw_er
# Draw from SQLAlchemy base
draw_er(Base, 'erd_from_sqlalchemy.png')

# Draw from database
draw_er("sqlite:///relative/path/to/db.db", 'erd_from_sqlite.png')
``` 

## Use from the command line
    render_er -i sqlite:///relative/path/to/db.db -o erd_from_sqlite.png


# Install
To install ERAlchemy, just do
    pip install eralchemy
`ERAlchemy` requires [GraphViz](http://www.graphviz.org/Download.php) to generate the graphs.

Install [graphviz](http://www.graphviz.org/Download.php) for your system.

# Architecture
![Architecture schema](https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/eralchemy_architecture.png?raw=true "Architecture schema")

Thanks to it's modular architecture, it's an extensible tool: it can also be connected to other ORMs/ODMs/OGMs.

# Notes
ERAlchemy was inspired by [erd](https://github.com/BurntSushi/erd).

# License
Released under an Apache License 2.0

Creator: Alexis Benoist