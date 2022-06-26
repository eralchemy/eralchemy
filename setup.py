from setuptools import setup

try:
    with open('README.rst') as f:
        long_description = f.read()
except IOError:
    with open('README.md') as f:
        long_description = f.read()


def read_version():
    with open('eralchemy2/version.py') as f:
        code = f.readlines()[0]
    exec(code)
    assert ('version' in locals())
    return locals()['version']


setup(
    name='eralchemy2',

    version=read_version(),

    description='Simple entity relation (ER) diagrams generation',
    long_description=long_description,

    # The project's main homepage.d
    url='https://github.com/maurerle/eralchemy2',

    # Author details
    author='Florian Maurer',
    author_email='fmaurer+github@disroot.org',

    # Choose your license
    license='Apache License 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database',
    ],

    # What does your project relate to?
    keywords='sql relational databases ER diagram render',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=[
        'eralchemy2',
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
            'eralchemy2=eralchemy2.main:cli',
        ],
    },
)
