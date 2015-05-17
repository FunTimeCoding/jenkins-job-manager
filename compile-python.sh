#!/bin/sh

# On Debian Wheezy systems, make sure you're on the staff group.
# To uninstall, simply delete the PREFIX directory.
export VERSION=3.4.3
export NAME=Python-${VERSION}
export FILE=${NAME}.tgz
export PREFIX=/usr/local/opt/python-${VERSION}
cd /tmp
wget https://www.python.org/ftp/python/${VERSION}/${FILE}
tar -zxf /tmp/${FILE}
cd ${NAME}
./configure --prefix=${PREFIX}
make
make install
rm /tmp/${FILE}
rm -rf /tmp/${NAME}
cd
