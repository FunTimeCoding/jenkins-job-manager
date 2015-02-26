#!/bin/sh -e
echo "Deleting python cache files and directories and the .egg-info directory."
find . -name "__pycache__" | xargs -I {} rm -rfv "{}"
find . -name "*.egg-info" | xargs -I {} rm -rfv "{}"
find . -name "*.pyc" | xargs -I {} rm -v "{}"
rm -rfv build
rm -f .coverage
