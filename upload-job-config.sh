#!/bin/sh -e

~/Code/Personal/jenkins-tools/bin/delete-job.sh jenkins-job-manager
~/Code/Personal/jenkins-tools/bin/put-job.sh jenkins-job-manager job.xml
