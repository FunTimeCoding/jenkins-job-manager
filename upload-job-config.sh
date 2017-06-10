#!/bin/sh -e

~/src/jenkins-tools/bin/delete-job.sh jenkins-job-manager || true
~/src/jenkins-tools/bin/put-job.sh jenkins-job-manager job.xml
