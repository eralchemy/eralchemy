rm -r ERAlchemy.egg-info
rm -r build
rm -r dist
pandoc --from=markdown --to=rst README.md --output=readme.rst
python setup.py bdist_wheel --universal
twine upload dist/*
open https://pypi.python.org/pypi/ERAlchemy