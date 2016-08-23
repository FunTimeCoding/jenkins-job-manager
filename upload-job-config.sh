#!/bin/sh -e

~/Code/Personal/jenkins-tools/bin/delete-job.sh jenkins-job-manager || true
~/Code/Personal/jenkins-tools/bin/put-job.sh jenkins-job-manager job.xml
