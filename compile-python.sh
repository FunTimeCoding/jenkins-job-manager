#!/bin/sh -e
# To uninstall, delete the PREFIX directory.

USER_ID=$(id -u)

if [ ! "${USER_ID}" = "0" ]; then
    NOT_IN_STAFF=false
    groups | grep staff > /dev/null || NOT_IN_STAFF=true

    if [ "${NOT_IN_STAFF}" = true ]; then
        echo "You must be in the staff group."

        exit 1
    fi
fi

VERSION=3.4.3
NAME=Python-${VERSION}
FILE=${NAME}.tgz
cd /tmp

if [ ! -f "${FILE}" ]; then
    wget https://www.python.org/ftp/python/${VERSION}/${FILE}
fi

if [ ! -d "${NAME}" ]; then
    tar -zxf /tmp/${FILE}
fi

PREFIX=/usr/local/opt/python-${VERSION}

if [ ! -d "${PREFIX}" ]; then
    cd "${NAME}"
    ./configure --prefix=${PREFIX}
    make
    make install
fi

if [ "${1}" = "--clean" ]; then
    rm /tmp/${FILE}
    rm -rf /tmp/${NAME}
fi

echo "Done."
