ERAlchemy is an extensible tool to generate ER diagrams.
It's now integrated with SQLAlchemy.
It's also able to generate the ER digram from an existing database.
It can also be connected to other ORMs/ODMs/OGMs.

# Quick Start 

    from eralchemy import draw_er
    draw_er(Base.metadata, 'output.png')


# Install
`ERAlchemy` requires [GraphViz](http://www.graphviz.org/Download.php) to generate the graphs.
Install [graphviz](http://www.graphviz.org/Download.php) for your system.

# Architecture
ERAlchemy was inspired by [erd](https://github.com/BurntSushi/erd).