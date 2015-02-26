#!/bin/sh -e
if [ "${1}" = "--ci-mode" ]; then
    shift
    mkdir -p build/log
    pep8 --statistics . | tee build/log/pep8.txt
else
    pep8 --statistics .
    echo "pep8 report clean"
fi
