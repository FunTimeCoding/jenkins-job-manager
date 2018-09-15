#!/bin/sh -e

script/docker/remove.sh

# Remove image.
docker rmi funtimecoding/jenkins-job-manager

# Remove dangling image identifiers, and more.
docker system prune
