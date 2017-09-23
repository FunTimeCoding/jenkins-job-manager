#!/bin/sh -e

./setup.sh
# shellcheck source=/dev/null
. .venv/bin/activate
./spell-check.sh
./style-check.sh --ci-mode
#./metrics.sh --ci-mode
./tests.sh --ci-mode
./setup.py bdist_wheel
SYSTEM=$(uname)

if [ "${SYSTEM}" = Linux ]; then
    fpm --input-type python --output-type deb --python-pip /usr/bin/pip3 --python-bin /usr/bin/python3 .
fi
