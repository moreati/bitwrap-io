#!/usr/bin/env bash

if [[ "${1}x" = 'x' ]] ; then
  CONTAINER_NAME='bitwrap-pnml-dev'
else
  CONTAINER_NAME=$1
fi
echo "rebuilding: ${CONTAINER_NAME}"

docker kill $CONTAINER_NAME &>/dev/null
docker rm $CONTAINER_NAME &>/dev/null
docker build .

IMAGE_UUID=$(docker build . | awk '/Successfully built/ {  print $3 }')
echo "using docker image => ${IMAGE_UUID}"

docker run -it --name=${CONTAINER_NAME} \
--entrypoint=/bin/bash \
-p 127.0.0.1:8080:8080 \
-v ${HOME}:/opt/bitwrap ${IMAGE_UUID}
