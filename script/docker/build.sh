#!/bin/sh -e

docker images | grep --quiet funtimecoding/jenkins-job-manager && FOUND=true || FOUND=false

if [ "${FOUND}" = true ]; then
    docker rmi funtimecoding/jenkins-job-manager
fi

docker build --tag funtimecoding/jenkins-job-manager .
