#!/bin/sh -e

VENDOR_NAME='FunTimeCoding'
export VENDOR_NAME

PROJECT_NAME='jenkins-job-manager'
export PROJECT_NAME

PROJECT_VERSION='0.3.0'
export PROJECT_VERSION

PACKAGE_VERSION='1'
export PACKAGE_VERSION

MAINTAINER='Alexander Reitzel'
export MAINTAINER

EMAIL='funtimecoding@gmail.com'
export EMAIL

COMBINED_VERSION="${PROJECT_VERSION}-${PACKAGE_VERSION}"
export COMBINED_VERSION

VENDOR_NAME_LOWER=$(echo "${VENDOR_NAME}" | tr '[:upper:]' '[:lower:]')
export VENDOR_NAME_LOWER

PROJECT_NAME_UNDERSCORE=$(echo "${PROJECT_NAME}" | tr - _)
export PROJECT_NAME_UNDERSCORE

# vendor is in here to not break php-skeleton based projects when synchronizing with them.
# .venv is for jenkins-job-manager.
# node_modules is for java-script-skeleton
# target is for java-skeleton
EXCLUDE_FILTER='^.*\/(build|tmp|vendor|node_modules|target|\.venv|\.git|\.vagrant|\.idea|\.tox|\.scannerwork|\.cache|__pycache__|[a-z_]+\.egg-info)\/.*$'
export EXCLUDE_FILTER

EXCLUDE_FILTER_WITH_INIT='^.*\/((build|tmp|vendor|node_modules|target|\.venv|\.git|\.vagrant|\.idea|\.tox|\.scannerwork|\.cache|__pycache__|[a-z_]+\.egg-info)\/.*|__init__\.py)$'
export EXCLUDE_FILTER_WITH_INIT
