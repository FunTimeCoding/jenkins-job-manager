#!/bin/sh -e

mkdir -p tmp/salt
cp configuration/minion.yaml tmp/salt/minion.conf

if [ ! -f tmp/bootstrap-salt.sh ]; then
    wget --output-document tmp/bootstrap-salt.sh https://bootstrap.saltstack.com
fi

touch tmp/gemrc
chmod 600 tmp/gemrc
cat "${HOME}/.gemrc" > tmp/gemrc

touch tmp/pypirc
chmod 600 tmp/pypirc
cat "${HOME}/.pypirc" > tmp/pypirc

vagrant up
