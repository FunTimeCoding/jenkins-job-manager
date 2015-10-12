#!/bin/sh -e

CI_MODE=0

if [ "${1}" = "--ci-mode" ]; then
    shift
    CI_MODE=1
    mkdir -p build/log
fi

echo "================================================================================"
echo
echo "Running PEP8."

if [ "${CI_MODE}" = "1" ]; then
    pep8 --exclude=.git,.pyvenv,__pycache__ --statistics . | tee build/log/pep8.txt || true
else
    pep8 --exclude=.git,.pyvenv,__pycache__ --statistics . || true
fi

echo
echo "================================================================================"
echo
echo "Running PyLint."
FIND=$(find . -name '*.py' -and -not -path '*/.pyvenv/*')

if [ "${CI_MODE}" = "1" ]; then
    # TODO: Fix this warning. It's tricky. Adding quotes will break pylint.
    # shellcheck disable=SC2086
    pylint --rcfile=.pylintrc ${FIND} | tee build/log/pylint.txt
else
    # shellcheck disable=SC2086
    pylint --rcfile=.pylintrc ${FIND}
fi

echo "================================================================================"
echo
echo "Running ShellCheck."
find . -name '*.sh' -exec sh -c 'shellcheck ${1} || true' '_' '{}' \;
echo
echo "================================================================================"
