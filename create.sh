#!/bin/sh -e

mkdir -p tmp

if [ ! -f tmp/ethernet-device.txt ]; then
    echo eth0 > tmp/ethernet-device.txt
fi

touch tmp/gemrc
chmod 600 tmp/gemrc
cat "${HOME}/.gemrc" > tmp/gemrc

touch tmp/pypirc
chmod 600 tmp/pypirc
cat "${HOME}/.pypirc" > tmp/pypirc

vagrant up
