#!/bin/sh

exec kubectl exec -n haproxy "$(kubectl -o yaml get pod -n haproxy | pipenv run python -c 'import sys, yaml; print(yaml.load(sys.stdin)["items"][0]["metadata"]["name"])')" -c haproxy -i -t -- sh
