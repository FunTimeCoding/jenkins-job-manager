#!/bin/sh -e

EXCLUDE_FILTER='^.*\/(build|tmp|\.git|\.vagrant|\.idea|\.venv|\.tox|\.cache|\.pytest_cache|__pycache__|[a-z_]+\.egg-info)\/.*$'
export EXCLUDE_FILTER
EXCLUDE_FILTER_WITH_INIT='^.*\/((build|tmp|\.git|\.vagrant|\.idea|\.venv|\.tox|\.cache|\.pytest_cache|__pycache__|[a-z_]+\.egg-info)\/.*|__init__\.py)$'
export EXCLUDE_FILTER_WITH_INIT
