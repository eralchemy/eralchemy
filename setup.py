from setuptools import setup
with open('README.rst') as f:
    long_description = f.read()
setup(
    name='ERAlchemy',

    version='0.0.22',

    description='Simple entity relation (ER) diagrams generation',
    long_description=long_description,

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