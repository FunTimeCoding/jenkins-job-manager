#!/bin/sh -e

wget --quiet --output-document - cfg.shiin.org/python3.sh | sh -e
wget --quiet --output-document - cfg.shiin.org/shellcheck.sh | sh -e

OPERATING_SYSTEM=$(uname)

if [ "${OPERATING_SYSTEM}" = Linux ]; then
    apt-get -qq install libxml2-dev libxslt1-dev
fi

pip3 install --upgrade --user --requirement requirements.txt
pip3 install --user --editable .
