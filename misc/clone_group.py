import argparse
import functools
import logging
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

import gitlab


def clone(clone_dir, project):
    directory = os.path.join(clone_dir, project.path_with_namespace)
    os.makedirs(directory, exist_ok=True)
    try:
        subprocess.check_call(['git', 'clone', project.ssh_url_to_repo, directory],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        if e.returncode != 128:
            return project.path_with_namespace, None, e.stderr

        try:
            subprocess.check_call(['git', '-C', directory, 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            return project.path_with_namespace, None, e.stderr
        return project.path_with_namespace, 'Updated', None

    return project.path_with_namespace, 'Cloned', None


def projects(gl, groups):
    for gname in groups:
        yield from gl.groups.get(gname, lazy=True).projects.list(as_list=False, per_page=100)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--dest', default='.')
    parser.add_argument('-j', '--max-workers', type=int)
    parser.add_argument('group', nargs='+')
    args = parser.parse_args()

    logging.basicConfig(level=[logging.WARNING, logging.INFO, logging.DEBUG][min(args.verbose, 2)])

    with gitlab.Gitlab.from_config('prod') as gl:
        with ProcessPoolExecutor(args.max_workers) as executor:
            for repo, status, err in executor.map(functools.partial(clone, args.dest), projects(gl, args.group)):
                if err:
                    logging.error('%s: %s', repo, err)
                else:
                    logging.info('%s: %s', repo, status)


if __name__ == '__main__':
    import sys
    sys.exit(main())
