#!/bin/sh -e

touch tmp/gemrc
chmod 600 tmp/gemrc
cat "${HOME}/.gemrc" > tmp/gemrc

touch tmp/pypirc
chmod 600 tmp/pypirc
cat "${HOME}/.pypirc" > tmp/pypirc

vagrant up
