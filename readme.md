ERAlchemy is an extensible general tool to generate ER diagrams, now integrated with SQLAlchemy.
# Note 

    from eralchemy import draw_er
    draw_er(Base.metadata, 'output.png')


# Dependencies
`ERAlchemy` requires [GraphViz](http://www.graphviz.org/Download.php) to generate.

This project was inspired by [erd](https://github.com/BurntSushi/erd) which I copied and integrated with SQLAlchemy.