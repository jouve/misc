#!/usr/bin/env python

# put credentials in ~/.python-gitlab.cfg as described here:
# https://python-gitlab.readthedocs.io/en/stable/cli.html#configuration

import argparse
import logging
import sys

import gitlab

__version__ = '0.1'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('project')
    parser.add_argument('mr')
    args = parser.parse_args()

    logging.basicConfig(level=[logging.WARNING, logging.INFO, logging.DEBUG][min(args.verbose, 2)], stream=sys.stderr)

    with gitlab.Gitlab.from_config() as gl:  # credentials from ~/.python-gitlab.cfg
        project = gl.projects.get(  # https://docs.gitlab.com/ee/api/projects.html#get-single-project
            args.project, lazy=True
        )
        mr = project.mergerequests.get(  # https://docs.gitlab.com/ee/api/merge_requests.html#get-single-mr
            args.mr, lazy=True
        )
        changes = mr.changes()['changes']  # https://docs.gitlab.com/ee/api/merge_requests.html#get-single-mr-changes

    for change in changes:
        print(change['diff'])

    return 0


if __name__ == '__main__':
    sys.exit(main())
