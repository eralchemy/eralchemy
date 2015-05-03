ERAlchemy is an extensible tool to generate entity relation (ER) diagrams.

It's now integrated with SQLAlchemy.

It's also able to generate the ER digram from an existing database.

It can also be connected to other ORMs/ODMs/OGMs.

# Quick Start 

    from eralchemy import draw_er
    # Draw from SQLAlchemy base
    draw_er(Base, 'erd_from_sqlalchemy.png')
    
    # Draw from database
    draw_er("sqlite:///relative/path/to/db.db", 'erd_from_sqlite.png')
    


# Install
`ERAlchemy` requires [GraphViz](http://www.graphviz.org/Download.php) to generate the graphs.
Install [graphviz](http://www.graphviz.org/Download.php) for your system.

# Architecture
![Architecture schema](/eralchemy_architecture.png?raw=true "Architecture schema")
ERAlchemy was inspired by [erd](https://github.com/BurntSushi/erd).
