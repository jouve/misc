import argparse
import logging
import sys
import gitlab


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('group')
    args = parser.parse_args()

    logging.basicConfig(level=[logging.WARNING, logging.INFO, logging.DEBUG][min(args.verbose, 2)])

    with gitlab.Gitlab.from_config() as gl:
        for p in gl.groups.get(args.group, lazy=True).projects.list(as_list=False):
            gl.projects.update(
                p.id,
                new_data=dict(
                    issues_enabled=False,
                    wiki_enabled=False,
                    lfs_enabled=False,
                    merge_method='ff',
                    only_allow_merge_if_pipeline_succeeds=True
                )
            )


if __name__ == '__main__':
    sys.exit(main())
