ERAlchemy is an extensible tool to generate ER diagrams.
It's now integrated with SQLAlchemy.

# Quick Start 

    from eralchemy import draw_er
    draw_er(Base.metadata, 'output.png')


# Install
`ERAlchemy` requires [GraphViz](http://www.graphviz.org/Download.php) to generate the graphs.
Install [graphviz](http://www.graphviz.org/Download.php) for your system.
Install 

## Formats
Formats (not all may be available on every system depending on how Graphviz was built)

‘canon’, ‘cmap’, ‘cmapx’, ‘cmapx_np’, ‘dia’, ‘dot’, ‘fig’, ‘gd’, ‘gd2’, ‘gif’, ‘hpgl’, ‘imap’, ‘imap_np’, ‘ismap’, ‘jpe’, ‘jpeg’, ‘jpg’, ‘mif’, ‘mp’, ‘pcl’, ‘pdf’, ‘pic’, ‘plain’, ‘plain-ext’, ‘png’, ‘ps’, ‘ps2’, ‘svg’, ‘svgz’, ‘vml’, ‘vmlz’, ‘vrml’, ‘vtx’, ‘wbmp’, ‘xdot’, ‘xlib’

ERAlchemy was inspired by [erd](https://github.com/BurntSushi/erd).