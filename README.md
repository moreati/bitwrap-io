# Bitwrap-io-python

A bitwrapp appserver written in python using redis and flask-socketio

### install 
    sudo apt-get install libpython-dev python3-all-dev 

    # use python3 
    virtualenv  -p python3 .env

#### run tests

    python -m pytest

### Docker

#### start redis

    docker run -d --name redis-dev redis

#### start linked container

    docker run --name=bitwrap-io-python --link redis-dev:redis -v ~/:/opt/bitwrap -it ${IMAGE}

#### use redis-cli

    docker exec -it redis-dev redis-cli
