#!/bin/sh -e

export DEBIAN_FRONTEND=noninteractive
apt-get --quiet 2 install neovim multitail htop git tree twine ruby-dev build-essential python3-wheel python3-venv libyaml-dev libxml2-dev libxslt-dev libenchant-dev hunspell shellcheck

echo 'PATH="${HOME}/.gem/ruby/2.3.0/bin:${PATH}"' >> /home/vagrant/.profile

sudo -u vagrant touch /home/vagrant/.pypirc
chmod 600 /home/vagrant/.pypirc
cat /vagrant/tmp/pypirc > /home/vagrant/.pypirc

sudo -u vagrant touch /home/vagrant/.gemrc
chmod 600 /home/vagrant/.gemrc
cat /vagrant/tmp/gemrc > /home/vagrant/.gemrc

sudo -u vagrant gem install fpm
