#!/bin/bash

set -e

CURR_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WS_ROOT="$( dirname ${CURR_DIR} )"
DOCKER_FILE="workspace/jupyter/jupyter.Dockerfile"
REPO="repo"
NAME="jupyter-llm"
TAG="dev"

# Run docker buildx create --use before running this script
echo "Running: docker buildx build --platform=linux/amd64,linux/arm64 -t $REPO/$NAME:$TAG -f $DOCKER_FILE $WS_ROOT --push"
docker buildx build --platform=linux/amd64,linux/arm64 -t $REPO/$NAME:$TAG -f $DOCKER_FILE $WS_ROOT --push
