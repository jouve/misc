#!/bin/sh

exec kubectl -o yaml get pod -n haproxy | pipenv run python -c 'import sys, yaml; print(yaml.load(sys.stdin)["items"][0]["metadata"]["name"])' | xargs -I{} kubectl exec -n haproxy {} -c haproxy -- kill -HUP 1

