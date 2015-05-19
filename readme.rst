Entity relation diagrams generator
==================================

ERAlchemy generates Entity Relation (ER) diagram (like the one below)
from databases or from SQLAlchemy models.

Example
-------

.. figure:: https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/graph_example.png?raw=true
   :alt: Example for a graph

   Example for a graph

Quick Start
-----------

Install
~~~~~~~

To install ERAlchemy, just do:

::

    $ pip install eralchemy

``ERAlchemy`` requires
`GraphViz <http://www.graphviz.org/Download.php>`__ to generate the
graphs.

Use from python
~~~~~~~~~~~~~~~

.. code:: python

    from eralchemy import render_er
    ## Draw from SQLAlchemy base
    render_er(Base, 'erd_from_sqlalchemy.png')

    ## Draw from database
    render_er("sqlite:///relative/path/to/db.db", 'erd_from_sqlite.png')

Use from the command line
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ eralchemy -i sqlite:///relative/path/to/db.db -o erd_from_sqlite.png

Architecture
------------

.. figure:: https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/eralchemy_architecture.png?raw=true
   :alt: Architecture schema

   Architecture schema

Thanks to it's modular architecture, it can be connected to other
ORMs/ODMs/OGMs/O\*Ms.

Notes
-----

Every feedback is welcome on the `GitHub
issues <https://github.com/Alexis-benoist/eralchemy/issues>`__.

To run the tests, use : ``$ py.test``.

ERAlchemy was inspired by `erd <https://github.com/BurntSushi/erd>`__.

Released under an Apache License 2.0

Creator: Alexis Benoist
[@Alexis\_Benoist](https://twitter.com/Alexis\_Benoist)
