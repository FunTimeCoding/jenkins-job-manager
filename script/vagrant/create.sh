#!/bin/sh -e

mkdir -p tmp/salt
cp configuration/minion.yaml tmp/salt/minion.conf

if [ ! -f tmp/bootstrap-salt.sh ]; then
    wget --output-document tmp/bootstrap-salt.sh https://bootstrap.saltstack.com
fi

if [ -f "${HOME}/.gitconfig" ]; then
    cp "${HOME}/.gitconfig" tmp/gitconfig.txt
fi

if [ -f "${HOME}/.gitignore_global" ]; then
    cp "${HOME}/.gitignore_global" tmp/gitignore_global.txt
fi

vagrant up
vagrant ssh --command /vagrant/script/vagrant/vagrant.sh
