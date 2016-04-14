#!/usr/bin/env bash

if [[ "${1}x" = 'x' ]] ; then
  CONTAINER_NAME='bitwrap-io-python'
else
  CONTAINER_NAME=$1
fi
echo "building: ${CONTAINER_NAME}"

IMAGE_UUID=$(docker build . | awk '/Successfully built/ {  print $3 }')
echo "using docker image => ${IMAGE_UUID}"

docker run --name=${CONTAINER_NAME} --link redis-dev:redis -v ~/:/opt/bitwrap -p 8080:8080 -it ${IMAGE_UUID}
