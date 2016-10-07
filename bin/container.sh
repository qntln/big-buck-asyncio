#!/bin/bash
#
# This is simple wrapper when you have no python 3.5 installed
# It will run our main.py in docker container with python 3.5 image
# Usage:
#   ./bin/container.sh
#

function abspath() {
    cd "$(dirname "$1")"
    printf "%s/%s\n" "$(pwd)" "$(basename "$1")"
    cd "$OLDPWD"
}

# Get path to root of project
ROOT=$(abspath "$(dirname $(dirname "${0}"))")

# run our applications in python:3.5.2 container
docker run \
    --rm \
    --volume "${ROOT}:/usr/src/app/" \
    -p '8800:8800' \
    --name player \
    python:3.5.2 \
    python3.5 -u /usr/src/app/bin/main.py /usr/src/app/data/bigBuckBunny-small.asci.bz2
