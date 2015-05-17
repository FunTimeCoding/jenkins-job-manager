#!/bin/sh -e

getopt -o w:p:hcv -l workspace:,pythonhome:,help,clean,verbose --name "${0}" -- "$@" > /dev/null
CLEAN=0

while true; do
    case ${1} in
        -w|--workspace)
            WORKSPACE="${2-}"
            shift 2
            ;;
        -p|--pythonhome)
            PYTHONHOME="${2-}"
            shift 2
            ;;
        -h|--help)
            echo "Usage: [-h][-c|--clean][-w|--workspace WORKSPACE][-p|--pythonhome PYTHONHOME]"
            exit 0
            ;;
        -c|--clean)
            CLEAN=1
            shift
            ;;
        -v|--verbose)
            set -x
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            if [ ! "${1}" = "" ]; then
                echo "Unknown option: $1"
            fi
            break
            ;;
    esac
done

if [ "${WORKSPACE}" = "" ]; then
    DIR=$(dirname "${0}")
    SCRIPT_DIR=$(cd "${DIR}"; pwd)
    WORKSPACE="${SCRIPT_DIR}"
fi

echo "WORKSPACE: ${WORKSPACE}"

if [ "${CLEAN}" = "1" ]; then
    "${WORKSPACE}/clear-cache.sh"
fi

if [ ! "${PYTHONHOME}" = "" ]; then
    echo "PYTHONHOME: ${PYTHONHOME}"
    export PATH="${PYTHONHOME}/bin:${PATH}"
fi

echo "PATH: ${PATH}"
BUILD_DIR="${WORKSPACE}/build"

if [ -d "${BUILD_DIR}" ]; then
    rm -rf "${BUILD_DIR}"
fi

mkdir -p "${BUILD_DIR}/log"
PYVENV_HOME="${WORKSPACE}/.pyvenv"

echo "Creating pyvenv."

if [ ! -d "${PYVENV_HOME}" ]; then
    pyvenv "${PYVENV_HOME}"
fi

echo "Installing requirements."
. "${PYVENV_HOME}/bin/activate"
pip3 install --upgrade pip
pip3 install --upgrade -r "${WORKSPACE}/requirements.txt" | tee build/log/pip.log

"${WORKSPACE}/run-style-check.sh" --ci-mode
"${WORKSPACE}/run-metrics.sh" --ci-mode
"${WORKSPACE}/run-tests.sh" --ci-mode
