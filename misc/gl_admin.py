
#!/usr/bin/env python

import argparse
import logging
import sys
from concurrent.futures import ProcessPoolExecutor

import gitlab

__version__ = 'version'


def clean_group(g):
    #print('=====', g.full_path)
    for m in list(mm for mm in g.members.list(as_list=False) if mm.state in ['blocked', 'ldap_blocked']):
        try:
            m.delete()
            #print('m.delete()', g.full_path, m.username)
        except gitlab.exceptions.GitlabDeleteError:
            print('m.delete()', g.full_path, m.username)


def clean_project(p):
    #print('=====', p.path_with_namespace)
    for m in list(mm for mm in p.members.list(as_list=False) if mm.state in ['blocked', 'ldap_blocked']):
        try:
            m.delete()
            #print('m.delete()', p.path_with_namespace, m.username)
        except gitlab.exceptions.GitlabDeleteError:
            print('m.delete()', p.path_with_namespace, m.username)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-V', '--version', action='version', version=__version__)
    args = parser.parse_args()

    logging.basicConfig(level=[logging.WARNING, logging.INFO, logging.DEBUG][min(args.verbose, 2)])

    with gitlab.Gitlab.from_config('prod') as gl:
        with ProcessPoolExecutor(16) as executor:

            if True:
                list(executor.map(clean_group, gl.groups.list(as_list=False)))

            if True:
                list(
                    executor.map(clean_project, gl.projects.list(as_list=False, archived=True))
                )


if __name__ == '__main__':
    sys.exit(main())
