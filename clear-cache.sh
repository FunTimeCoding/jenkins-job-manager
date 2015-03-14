#!/bin/sh -e

SCRIPT_DIR=$(cd $(dirname ${0}); pwd)

echo "Deleting python cache files and directories and the .egg-info directory."

FILES="build .pyvenv .coverage"

for FILE in ${FILES}; do
    if [ -e "${FILE}" ]; then
        echo "rm -rf ${FILE}"
        rm -rf "${SCRIPT_DIR}/${FILE}"
    fi
done

find "${SCRIPT_DIR}" -name "__pycache__" | xargs -I {} rm -rfv "{}"
find "${SCRIPT_DIR}" -name "*.egg-info" | xargs -I {} rm -rfv "{}"
find "${SCRIPT_DIR}" -name "*.pyc" | xargs -I {} rm -fv "{}"
