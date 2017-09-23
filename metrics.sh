#!/bin/sh -e

SYSTEM=$(uname)

if [ "${SYSTEM}" = Darwin ]; then
    TEE=gtee
else
    TEE=tee
fi

mkdir -p build/log
sonar-runner | "${TEE}" build/log/sonar-runner.log
rm -rf .sonar
