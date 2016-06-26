# Bitwrap-io-python

A bitwrapp appserver written in python using redis and flask-socketio

#### run tests

    python -m pytest

#### start redis

    docker run --name redis-dev --detach redis

#### start linked container

    docker run --name=bitwrap-io-python --link redis-dev:redis -v ${HOME}/:/opt/bitwrap -it ${IMAGE}

#### use redis-cli

    docker exec -it redis-dev redis-cli
