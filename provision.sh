#!/bin/sh -e

export DEBIAN_FRONTEND=noninteractive
CODENAME=$(lsb_release --codename --short)

if [ "${CODENAME}" = jessie ]; then
    echo Europe/Berlin | tee /etc/timezone
    dpkg-reconfigure --frontend noninteractive tzdata
    #apt-get --quiet 2 install ntp
    apt-get --quiet 2 install vim multitail htop
elif [ "${CODENAME}" = stretch ]; then
    apt-get --quiet 2 install neovim multitail htop
fi

#apt-get --quiet 2 install python3
