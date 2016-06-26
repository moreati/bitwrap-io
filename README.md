# Bitwrap-io-python

[![Build Status](https://travis-ci.org/bitwrap/bitwrap-io-python.svg?branch=master)](https://travis-ci.org/bitwrap/bitwrap-io-python)

A bitwrapp appserver written in python using flask, twisted, redis, and sock.js

#### run tests

    python -m pytest

#### start redis

    docker run --name redis-dev --detach redis

#### start linked container

    docker run --name=bitwrap-io-python --link redis-dev:redis -v ${HOME}/:/opt/bitwrap -it ${IMAGE}

#### use redis-cli

    docker exec -it redis-dev redis-cli
