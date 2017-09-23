#!/bin/sh -e

rm -rf build

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

. .venv/bin/activate
pip3 install wheel
pip3 install --requirement requirements.txt
pip3 install --editable .
# shellcheck source=/dev/null
. .venv/bin/activate
./spell-check.sh --ci-mode
./style-check.sh --ci-mode
#./metrics.sh --ci-mode
./tests.sh --ci-mode
./setup.py bdist_wheel --dist-dir build
SYSTEM=$(uname)

if [ "${SYSTEM}" = Linux ]; then
    fpm --input-type python --output-type deb --python-pip /usr/bin/pip3 --python-bin /usr/bin/python3 .
    mv *.deb build
fi
