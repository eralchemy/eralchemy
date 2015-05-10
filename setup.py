"""Entity relation (ER) diagrams generator
=======================================

ERAlchemy is integrated with SQLAlchemy and is able to generate the ER
digram from an existing database.

Example
=======

.. figure:: https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/graph_example.png?raw=true
   :alt: Example for a graph

   Example for a graph

Quick Start
===========

Use from python
---------------

.. code:: python

    from eralchemy import draw_er
    # Draw from SQLAlchemy base
    draw_er(Base, 'erd_from_sqlalchemy.png')

    # Draw from database
    draw_er("sqlite:///relative/path/to/db.db", 'erd_from_sqlite.png')

Use from the command line
-------------------------

::

    $ eralchemy -i sqlite:///relative/path/to/db.db -o erd_from_sqlite.png

Install
=======

To install ERAlchemy, just do

::

    pip install eralchemy

``ERAlchemy`` requires
`GraphViz <http://www.graphviz.org/Download.php>`__ to generate the
graphs.

Architecture
============

.. figure:: https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/eralchemy_architecture.png?raw=true
   :alt: Architecture schema

   Architecture schema

Thanks to it's modular architecture, it can be connected to other
ORMs/ODMs/OGMs/O\*Ms.

Notes
=====

ERAlchemy was inspired by `erd <https://github.com/BurntSushi/erd>`__.

License
=======

Released under an Apache License 2.0

Creator: Alexis Benoist
"""

from setuptools import setup

setup(
    name='ERAlchemy',

    version='0.0.12',

    description='Simple entity relation (ER) diagrams generation',
    long_description=__doc__,

    # The project's main homepage.
    url='https://github.com/Alexis-benoist/eralchemy',

    # Author details
    author='Alexis Benoist',
    author_email='alexis.benoist@gmail.com',

    # Choose your license
    license='Apache License 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # What does your project relate to?
    keywords='sql relational databases ER diagram render',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=[
        'eralchemy',
    ],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'SQLAlchemy',
        'pygraphviz'
    ],
    entry_points={
        'console_scripts': [
            'eralchemy=eralchemy:cli',
        ],
    },
)