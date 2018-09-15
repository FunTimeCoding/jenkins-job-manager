#!/bin/sh -e

EXCLUDE_FILTER='^.*\/(build|tmp|\.git|\.vagrant|\.idea|\.venv|\.tox|\.cache|__pycache__|[a-z_]+\.egg-info)\/.*$'
export EXCLUDE_FILTER
EXCLUDE_FILTER_WITH_INIT='^.*\/((build|tmp|\.git|\.vagrant|\.idea|\.venv|\.tox)\/.*|__init__\.py)$'
export EXCLUDE_FILTER_WITH_INIT
