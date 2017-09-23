#!/bin/sh -e

if [ ! "${VIRTUAL_ENV}" = "" ]; then
    # Cannot run the deactivate command here.
    echo "Virtual environment must not be activated."

    exit 1
fi

# To guarantee a reproducible build, the virtual environment and build directories must be deleted.
rm -rf build .venv
# The Debian package must be deleted before fpm is run.
rm -f *.deb

./setup.sh
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
