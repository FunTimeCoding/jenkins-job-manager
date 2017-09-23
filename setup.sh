#!/bin/sh -e

SYSTEM=$(uname)

if [ "${SYSTEM}" = Darwin ]; then
    brew install python3 shellcheck
else
    sudo apt-get --quiet 2 install shellcheck libenchant-dev hunspell libyaml-dev libxml2-dev libxslt-dev
fi

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

. .venv/bin/activate
pip3 install --requirement requirements.txt
pip3 install --editable .
