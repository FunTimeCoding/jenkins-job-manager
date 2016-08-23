#!/bin/sh -e

# shellcheck disable=SC2016
jjm --locator https://github.com/FunTimeCoding/jenkins-job-manager.git --build-command 'export PATH="${HOME}/opt/python-3.5.1/bin:${PATH}"
./build.sh' > job.xml
