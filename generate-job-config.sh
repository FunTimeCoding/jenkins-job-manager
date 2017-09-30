#!/bin/sh -e

# shellcheck disable=SC2016
jjm --locator https://github.com/FunTimeCoding/jenkins-job-manager.git --build-command ./build.sh --junit build/junit.xml --checkstyle 'build/log/checkstyle-*' --recipients funtimecoding@gmail.com > job.xml
