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

echo 'PATH="${HOME}/.gem/ruby/2.3.0/bin:${PATH}"' >> /home/vagrant/.profile

sudo -u vagrant touch /home/vagrant/.pypirc
chmod 600 /home/vagrant/.pypirc
cat /vagrant/tmp/pypirc > /home/vagrant/.pypirc

apt-get --quiet 2 install twine ruby-dev build-essential

sudo -u vagrant touch /home/vagrant/.gemrc
chmod 600 /home/vagrant/.gemrc
cat /vagrant/tmp/gemrc > /home/vagrant/.gemrc

sudo -u vagrant gem install fpm
