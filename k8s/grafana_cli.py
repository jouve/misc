import argparse
import logging
import sys
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('filter')
    args = parser.parse_args()

    logging.basicConfig(
        level=[logging.WARNING, logging.INFO, logging.DEBUG][min(args.verbose, 2)],
        stream=sys.stderr
    )

    response = requests.get(
        'https://grafana.com/api/dashboards',
        params={
            'orderBy': 'name',
            'includeLogo': 1,
            'page': 1,
            'pageSize': 100,
            'dataSourceSlugIn': 'prometheus',
            'filter': args.filter
        })
    items = response.json()['items']
    items = sorted(items, key=lambda i: i['downloads'], reverse=True)

    for i in items[:10]:
        print(i['downloads'], i['name'], i['datasource'])

if __name__ == "__main__":
    sys.exit(main())
