#!/usr/bin/env python3

import argparse
import csv
import json
import logging
import subprocess
import sys
import itertools
from concurrent import futures


__version__ = '0.1'

def cloc(licenses, d):
    print(f'[{d}] cloc')
    try:
        data = json.loads(subprocess.check_output(['cloc', '--json', d], stderr=subprocess.PIPE))
    except (subprocess.CalledProcessError, ValueError):
        data = dict()
    print(f'[{d}] cloc: done')
    return (
        d, ' '.join(licenses.get(d) or list()), data.get('C/C++ Header', dict()).get('code', ''),
        data.get('C', dict()).get('code', ''), data.get('C++', dict()).get('code', '')
    )


#!/usr/bin/env python

import argparse
import logging
import sys



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('--licenses')
    parser.add_argument('--out')
    parser.add_argument('-j', '--parallel', type=int, default=0)
    parser.add_argument('--unordered', action='store_true')
    parser.add_argument('repos', nargs='+')
    args = parser.parse_args()

    logging.basicConfig(level=[logging.WARNING, logging.INFO, logging.DEBUG][min(args.verbose, 2)])

    with open(args.licenses) as fl:
        licenses = json.load(fl)

    def out():
        if args.parallel > 1:
            with futures.ProcessPoolExecutor(args.parallel) as executor:
                if args.unordered:
                    # result unordered (less memory)
                    return (
                        f.result()
                        for f in futures.as_completed(executor.submit(cloc, licenses, repo) for repo in args.repos)
                    )
                else:
                    # results are ordered (more memory)
                    return executor.map(cloc, itertools.repeat(licenses), args.repos)
        else:
            return (cloc(licenses, repo) for repo in args.repos)

    with open(args.out, 'w') as fl:
        w = csv.writer(fl)
        w.writerow(['repo', 'license', 'c/c++ headers', 'c', 'c++'])
        w.writerows(out)

    return 0


if __name__ == '__main__':
    sys.exit(main())
