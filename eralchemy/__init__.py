# -*- coding: utf-8 -*-
from eralchemy.main import render_er
import argparse
from eralchemy.helpers import check_args
__version__ = '1.0.0'


def cli():
    """Entry point for the application script"""
    parser = argparse.ArgumentParser(prog='ERAlchemy')
    parser.add_argument('-i', nargs='?', help='Database URI to process.')
    parser.add_argument('-o', nargs='?', help='Name of the file to write.')
    parser.add_argument('-s', nargs='?', help='Name of the schema.')
    parser.add_argument('-x', nargs='*', help='Name of the table(s) to exclude.')
    parser.add_argument('-v', help='Prints version number.', action='store_true')

    args = parser.parse_args()
    check_args(args)
    if args.v:
        print 'ERAlchemy version {}.'.format(__version__)
        exit(0)
    render_er(args.i, args.o, exclude=args.x, schema=args.s)


if __name__ == '__main__':
    cli()
