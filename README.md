# Bitwrap-io

[![Build Status](https://travis-ci.org/bitwrap/bitwrap-io.svg?branch=master)](https://travis-ci.org/bitwrap/bitwrap-io)

A blockchain style eventsourcing service using cyclone.io, redis, and libgit2.

### Reference

Read Martin Fowler's description of [Event Sourcing](http://martinfowler.com/eaaDev/EventSourcing.html)

Watch an event sourcing video from [Greg Young](https://www.youtube.com/watch?v=8JKjvY4etTY)

Read an article about how event sourcing compliments blockchains [ 6 Components of any Blockchain design solution ] (http://blockchain.glorat.net/2015/11/16/6-components-of-any-blockchain-design-solution/)

#### Development & Testing

    python -m pytest

start redis

    docker run -d --name redis-dev -p 127.0.0.1:6379:6379 redis

start linked container

    docker run --name=bitwrap-io --link redis-dev:redis -v ${HOME}/:/opt/bitwrap -it ${IMAGE_NAME}

use redis-cli

    docker exec -it redis-dev redis-cli
