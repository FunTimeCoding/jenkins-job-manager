#!/bin/sh -e

wget --quiet --output-document - cfg.shiin.org/python3.sh | sh -e
wget --quiet --output-document - cfg.shiin.org/shellcheck.sh | sh -e
pip3 install --upgrade --user --requirement requirements.txt
pip3 install --user --editable .

# Do not use pyenchant on OS X, because it appears to be broken and will likely be fixed soon.
OPERATING_SYSTEM=$(uname)

if [ "${OPERATING_SYSTEM}" = Darwin ]; then
    pip3 uninstall pyenchant
else
    apt-get -qq install libxml2-dev libxslt1-dev
fi
