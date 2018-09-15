#!/bin/sh -e

# Development mode mounts the project root so it can be edited and re-ran without rebuilding the image and recreating the container.

if [ "${1}" = --development ]; then
    DEVELOPMENT=true
else
    DEVELOPMENT=false
fi

docker ps --all | grep --quiet jenkins-job-manager && FOUND=true || FOUND=false

if [ "${FOUND}" = false ]; then
    WORKING_DIRECTORY=$(pwd)

    if [ "${DEVELOPMENT}" = true ]; then
        docker create --name jenkins-job-manager --volume "${WORKING_DIRECTORY}:/jenkins-job-manager" funtimecoding/jenkins-job-manager
    else
        docker create --name jenkins-job-manager funtimecoding/jenkins-job-manager
    fi

    # TODO: Specifying the entry point overrides CMD in Dockerfile. Is this useful, or should all sub commands go through one entry point script? I'm inclined to say one entry point script per project.
    #docker create --name jenkins-job-manager --volume "${WORKING_DIRECTORY}:/jenkins-job-manager" --entrypoint /jenkins-job-manager/bin/other.sh funtimecoding/jenkins-job-manager
    #docker create --name jenkins-job-manager funtimecoding/jenkins-job-manager /jenkins-job-manager/bin/other.sh
    # TODO: Run tests this way?
    #docker create --name jenkins-job-manager funtimecoding/jenkins-job-manager /jenkins-job-manager/script/docker/test.sh
fi

docker start --attach jenkins-job-manager
