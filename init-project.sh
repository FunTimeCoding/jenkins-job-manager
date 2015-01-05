#!/bin/sh -e
# This tool can be used to initialise the template after making a fresh copy to get started quickly.
# The goal is to make it as easy as possible to create scripts that allow easy testing and continuous integration.

CAMEL=${1}

if [ "${CAMEL}" = "" ]; then
    echo "Usage: ${0} MyUpperCamelCaseProjectName"
    exit 1
fi

if [[ ! ${CAMEL} =~ ^([A-Z][a-z0-9]+){2,}$ ]]; then
    echo "Project name must be in UpperCamelCase."
    exit 1
fi

UNDERSCORE=$(echo ${CAMEL} | sed -E 's/([A-Za-z0-9])([A-Z])/\1_\2/g' | tr '[:upper:]' '[:lower:]')
DASH=$(echo ${UNDERSCORE} | sed -E 's/_/-/g')
INITIALS=$(echo ${CAMEL} | sed 's/\([A-Z]\)[a-z]*/\1/g' | tr '[:upper:]' '[:lower:]' )

echo "Camel: ${CAMEL}"
echo "Underscore: ${UNDERSCORE}"
echo "Dash: ${DASH}"
echo "Initials: ${INITIALS}"

sed -i "" -e "s/ec/${INITIALS}/g" bin/example-script tests/test_example_class.py
sed -i "" -e "s/example_class/${UNDERSCORE}/g" bin/example-script tests/test_example_class.py
sed -i "" -e "s/ExampleClass/${CAMEL}/g" bin/example-script tests/test_example_class.py lib/example_class.py
sed -i "" -e "s/example-project/${DASH}/g" setup.py

git mv "tests/test_example_class.py" "tests/test_${UNDERSCORE}.py"
git mv "lib/example_class.py" "lib/${UNDERSCORE}.py"
git mv "bin/example-script" "bin/${INITIALS}"

echo "Done. Files were edited and moved using git. Review those changes. You may also delete this script now."
