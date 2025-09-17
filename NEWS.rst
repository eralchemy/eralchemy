eralchemy 1.5.0 (2025-09-18)
=============================

This is release 1.6.0 of eralchemy.
This release includes some bug fixes and new features:

Features
--------

- Make Config adjustable for rendering adjustments of dot files
- Add support for PlantUML

Bugfixes
--------

- Fix coverage badge
- Fix indentation in mermaid output for better readability
- Update Architecture image to markdown
- Allow calling format without writing to file
- Fixup mermaid er cardinalities
- Update pre-commit versions

eralchemy 1.5.0 (2024-09-17)
=============================

This is release 1.5.0 back on eralchemy.
Instead of `pip install eralchemy2` one should use `pip install eralchemy[graphviz]`.

Other than that, no breaking changes are to be expected.

Features
--------

- Unite codebase of eralchemy2 and eralchemy back to eralchemy
- Includes features from eralchemy2
- Allow having either graphviz or pygraphviz installed by @maurerle in https://github.com/eralchemy/eralchemy/pull/126
- Draw column relations by @JosePVB in https://github.com/eralchemy/eralchemy/pull/72
- CI now uses nox
- proper regex to include/exclude tables/columns
- allow setting title of diagram
- mermaid rendering support


Bugfixes
--------

- Improve tests by using fixtures by @maurerle in https://github.com/eralchemy/eralchemy/pull/120
- build: create a release workflow by @12rambau in https://github.com/eralchemy/eralchemy/pull/128
- Remove references to newsmeme by @kasium in https://github.com/eralchemy/eralchemy/pull/129
- give more readable error output when non sqlalchemy input is given by @maurerle in https://github.com/eralchemy/eralchemy/pull/118


eralchemy2 1.4.1 (2024-05-20)
=============================

Features
--------

- Add graph titles by @haffi96 in https://github.com/maurerle/eralchemy2/pull/20
- Add regex option for the include_tables and exclude_tables params by @dukkee in https://github.com/maurerle/eralchemy2/pull/31
- Update contribution instructions in README

Bugfixes
--------

- Sanitize mermaid strings in https://github.com/maurerle/eralchemy2/pull/42
- Use F-Strings and trailing commas in https://github.com/maurerle/eralchemy2/pull/40


eralchemy2 1.4.0 (2024-05-11)
=============================

Features
--------

- Add pre commit hook with trailing space removal, ruff and isort by @maurerle in https://github.com/maurerle/eralchemy2/pull/24
- make it possible to change the output mode through cli by @maurerle in https://github.com/maurerle/eralchemy2/pull/32
- apply fix to reference full table name correctly in output by @maurerle in https://github.com/maurerle/eralchemy2/pull/33
- set right_cardinality for relationships with compound primary_keys by @maurerle in https://github.com/maurerle/eralchemy2/pull/34
- add proper spacing before key type when rendering svg with inkscape by @maurerle in https://github.com/maurerle/eralchemy2/pull/35
- Add mermaid ER diagram by @maurerle in https://github.com/maurerle/eralchemy2/pull/36
- Add possibility to retrieve information from multiple schemas at once by @maurerle in https://github.com/maurerle/eralchemy2/pull/37

Deprecations and Removals
-------------------------
- drop support for python 3.7 in https://github.com/maurerle/eralchemy2/pull/26


eralchemy2 1.3.8 (2023-10-30)
=============================

Features
--------

- fix reading columns with whitespace correctly
- add python 3.12 to test matrix

Deprecations and Removals
-------------------------
- drop support for SQLAlchemy < 1.4


eralchemy2 1.3.7 (2023-02-27)
=============================

Features
--------

- add python 3.11 to github actions
- add python 3.11 and sqlalchemy 2.x to test matrix
- fix one-to-one relationships with primary key
- relax version requirements

eralchemy2 1.3.6 (2022-10-19)
=============================

Features
--------

- return feedback for wrong connection string
- better error handling for wrong db uri


eralchemy2 1.3.5 (2022-10-10)
=============================

Features
--------

- add typing
- allow installation on python < 3.8

eralchemy2 1.3.4 (2022-09-20)
=============================

Features
--------

- switch to pyproject.toml and poetry
- add release notes

eralchemy2 1.3.3 (2022-09-11)
=============================

Features
--------

- use black and isort with github actions (#10)
- add backward compatibility for SQLAlchemy < 1.4
- add some typings
- drop support for python 2.x

eralchemy2 1.3.2 (2022-06-26)
=============================

Features
--------

- compatibility for SQLAlchemy >= 1.4
- support mermaid export
- rename package to eralchemy2
