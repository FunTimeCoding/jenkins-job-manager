#!/bin/sh -e
if [ "${1}" = "--ci-mode" ]; then
    shift
    mkdir -p "build/log"
    pylint --rcfile=.pylintrc $(find . -name '*.py' -and -not -path '*/.pyvenv/*' -print) | tee "build/log/pylint.txt"
else
    pylint --rcfile=.pylintrc $(find . -name '*.py' -and -not -path '*/.pyvenv/*' -print)
fi
