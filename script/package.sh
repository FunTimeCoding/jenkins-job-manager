#!/bin/sh -e

NAME=jenkins-job-manager
PROJECT_VERSION=0.2.0
ARCHIVE="${NAME}_${PROJECT_VERSION}.orig.tar.gz"
PROJECT_ROOT="${NAME}-${PROJECT_VERSION}"
PACKAGE_VERSION=1
COMBINED_VERSION="${PROJECT_VERSION}-${PACKAGE_VERSION}"

if [ -f debian/changelog ]; then
    echo "TODO: Release sooner than here? Can it be done non-interactively?"
    #dch --release
    #dch --newversion "${COMBINED_VERSION}"
else
    dch --create --newversion "${COMBINED_VERSION}" --package "${NAME}"
fi

mkdir -p build
tar --create --gzip --transform "s,^,${PROJECT_ROOT}/," --exclude='./build' --exclude './.venv' --exclude './.tmp' --exclude './.idea' --exclude './.git' --exclude './.vagrant' --exclude './jenkins_job_manager.egg-info' --file "build/${ARCHIVE}" .
cd build
tar --extract --file "${ARCHIVE}"
cd "${PROJECT_ROOT}"
debuild -us -uc
