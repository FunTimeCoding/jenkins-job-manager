#!/bin/sh -e

export DEBIAN_FRONTEND=noninteractive
CODENAME=$(lsb_release --codename --short)

if [ "${CODENAME}" = jessie ]; then
    echo Europe/Berlin >/etc/timezone
    dpkg-reconfigure --frontend noninteractive tzdata
    apt-get --quiet 2 install vim multitail htop tree git dos2unix
elif [ "${CODENAME}" = stretch ]; then
    cp /vagrant/configuration/backports.txt /etc/apt/sources.list.d/backports.list
    apt-get --quiet 2 update
    apt-get --quiet 2 install neovim multitail htop tree git shellcheck hunspell devscripts ruby-ronn dos2unix
    apt-get --quiet 2 install ansible --target-release stretch-backports

    apt-get --quiet 2 install twine build-essential python3-dev python3-venv libenchant-dev python3-all
    apt-get --quiet 2 install libyaml-dev libxml2-dev libxslt-dev python3-lxml python3-yaml
elif [ "${CODENAME}" = buster ]; then
    apt-get --quiet 2 install neovim multitail htop tree git shellcheck hunspell devscripts ronn dos2unix ansible
fi
