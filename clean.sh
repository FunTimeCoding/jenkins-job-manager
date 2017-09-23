#!/bin/sh -e

if [ ! "${VIRTUAL_ENV}" = "" ]; then
    echo "Virtual environment is still active."

    exit 1
fi

FILES="build
dist
.venv
.coverage
.cache
.tox"

for FILE in ${FILES}; do
    rm -rf "${FILE}"
done

find . \( -name '__pycache__' -or -name '*.pyc' \) -delete
