#!/bin/sh -e

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

. .venv/bin/activate
pip3 install --requirement requirements.txt
pip3 install --editable .
