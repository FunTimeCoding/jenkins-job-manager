#!/bin/sh -e

mkdir -p build/log
sonar-runner | tee build/log/sonar-runner.log
rm -rf .sonar
