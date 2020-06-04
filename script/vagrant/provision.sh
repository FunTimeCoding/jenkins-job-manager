#!/bin/sh -e

export DEBIAN_FRONTEND=noninteractive
apt-get --quiet 2 install neovim multitail htop tree git shellcheck hunspell devscripts ruby-ronn twine build-essential python3-dev python3-venv libenchant-dev python3-all libyaml-dev libxml2-dev libxslt-dev python3-lxml python3-yaml

sudo -u vagrant touch /home/vagrant/.pypirc
chmod 600 /home/vagrant/.pypirc
cat /vagrant/tmp/pypirc > /home/vagrant/.pypirc
