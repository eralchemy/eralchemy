"""All the process that can be run using nox.

The nox run are build in isolated environment that will be stored in .nox. to force the venv update, remove the .nox/xxx folder.
"""

import nox

nox.options.sessions = ["lint", "docs", "test"]


@nox.session(reuse_venv=True)
def lint(session):
    """Apply the pre-commits."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(reuse_venv=True)
def docs(session):
    """Build the documentation."""
    build = session.posargs.pop() if session.posargs else "html"
    session.install(".[docs]")
    session.run("sphinx-build", "-v", "-b", build, "docs", f"docs/_build/{build}")


@nox.session(reuse_venv=True)
def ci_test(session):
    """Run the tests report coverage in xml format."""
    session.install(".[test]")
    test_files = session.posargs or ["tests"]
    session.run("pytest", "--color=yes", "--cov", "--cov-report=xml", *test_files)


@nox.session(reuse_venv=True)
def test(session):
    """Run the tests and report coverage in html format."""
    session.install(".[test]")
    test_files = session.posargs or ["tests"]
    session.run("pytest", "--color=yes", "--cov", "--cov-report=html", *test_files)


@nox.session(reuse_venv=True)
def mypy(session):
    """Run a mypy check of the lib."""
    session.install("mypy")
    test_files = session.posargs or ["eralchemy"]
    session.run("mypy", *test_files)
