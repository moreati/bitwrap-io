#!/usr/bin/env bash

if [[ "${1}x" = 'x' ]] ; then
  CONTAINER_NAME='bitwrap-pnml-dev'
else
  CONTAINER_NAME=$1
fi
echo "rebuilding: ${CONTAINER_NAME}"

docker rm --force $CONTAINER_NAME &>/dev/null
docker build . -t stackdump/bitwrap-pnml:dev

docker run -it --name=${CONTAINER_NAME} \
-e "VIRTUAL_HOST=api.bitwrap.io" \
-v ${HOME}:/opt/bitwrap stackdump/bitwrap-pnml:dev
