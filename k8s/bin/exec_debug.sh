#!/bin/sh

exec kubectl exec -n debug "$(kubectl -o yaml get pod -n debug | pipenv run python -c 'import sys, yaml; print(yaml.load(sys.stdin)["items"][0]["metadata"]["name"])')" -c debug -i -t -- sh
