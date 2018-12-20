#!/usr/bin/env python

import argparse
import logging
import sys

__version__ = '0.1'

import gitlab


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-V', '--version', action='version', version=__version__)
    args = parser.parse_args()

    logging.basicConfig(level=[logging.WARNING, logging.INFO, logging.DEBUG][min(args.verbose, 2)])

    with gitlab.Gitlab.from_config() as gl:
        for u in gl.users.list(as_list=False, blocked=True):
            for p in u.projects.list(as_list=False):
                print('delete', p.path_with_namespace, f'gl.projects.get({p.id}, lazy=True).delete()')


if __name__ == '__main__':
    sys.exit(main())
