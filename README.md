# Bitwrap-io-python

A bitwrapp appserver written in python using redis and flask-socketio

### install 
    sudo apt-get install libpython-dev python3-all-dev 

    # use python3 
    virtualenv  -p python3 .env

#### run tests

    python -m pytest

### Docker

#### start neo4j

    docker run  --name neo4j-dev --detach --publish=7474:7474 --volume=${HOME}/neo4j/data:/data neo4j

#### start redis

    docker run --name redis-dev --detach redis

#### start linked container

    docker run --name=bitwrap-io-python --link redis-dev:redis -v ${HOME}/:/opt/bitwrap -it ${IMAGE}

#### use redis-cli

    docker exec -it redis-dev redis-cli
