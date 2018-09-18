#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/project.sh"
ARCHIVE="${NAME}_${PROJECT_VERSION}.orig.tar.gz"
PROJECT_ROOT="${NAME}-${PROJECT_VERSION}"
mkdir -p build
tar --create --gzip --transform "s,^,${PROJECT_ROOT}/," --exclude='./build' --exclude './.venv' --exclude './.tmp' --exclude './.idea' --exclude './.git' --exclude './.vagrant' --exclude "./jenkins_job_manager.egg-info" --file "build/${ARCHIVE}" .
cd build
tar --extract --file "${ARCHIVE}"
cd "${PROJECT_ROOT}"
debuild -us -uc
