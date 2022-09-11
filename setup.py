from setuptools import setup


def read_long_description() -> str:
    with open("README.md") as f:
        return f.read()


def read_version() -> str:
    with open("eralchemy2/version.py") as f:
        code = f.readlines()[0]
    exec(code)
    assert "version" in locals()
    return locals()["version"]


if __name__ == "__main__":
    setup(
        name="eralchemy2",
        version=read_version(),
        description="Simple entity relation (ER) diagrams generation",
        long_description=read_long_description(),
        long_description_content_type='text/markdown',
        url="https://github.com/maurerle/eralchemy2",
        author="Florian Maurer",
        author_email="fmaurer+github@disroot.org",
        license="Apache License 2.0",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Scientific/Engineering :: Visualization",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Database",
        ],
        keywords="sql relational databases ER diagram render",
        packages=["eralchemy2"],
        extras_require={
            "dev": ["black", "isort", "tox", "Flask-SQLAlchemy", "psycopg2"]
        },
        install_requires=["SQLAlchemy", "pygraphviz"],
        entry_points={
            "console_scripts": ["eralchemy2=eralchemy2.main:cli"],
        },
    )
