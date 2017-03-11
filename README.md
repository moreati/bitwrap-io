# Bitwrap-io

[![Build Status](https://travis-ci.org/bitwrap/bitwrap-io.svg?branch=master)](https://travis-ci.org/bitwrap/bitwrap-io)
[![PyPI version](https://badge.fury.io/py/bitwrap_io.svg)](https://badge.fury.io/py/bitwrap_io)

A blockchain-style eventstore.

![tic-tac-toe state machine](https://bitwrap.github.io/image/octothorpe.png)

(above is a tic-tac-toe state machine )
### Status

* Developing Demo Apps & Widgets
  * http://bitwrap.github.io 

* Testing AWS Lambda integration

#### install

    pip install bitwrap_io

    twistd -n bitwrap \
      --listen-address 127.0.0.1 \
      --listen-port 8080 \
      --schema-path ./bitwrap_io/pnml \
      --lmdb-path /tmp

    # visit http://127.0.0.1:8080

### Roadmap

* Auth - provide authentication via Oauth2

* Contracts - api for joint event execution (think multisig transations) between statevectors
  * contracts form the basis for a Python API
  * using bitwrap to develop applications

* Analytics - archive event data to S3/Athena for warehousing & analysis

### Reference

Read Martin Fowler's description of [Event Sourcing](http://martinfowler.com/eaaDev/EventSourcing.html)

Watch an event sourcing video from [Greg Young](https://www.youtube.com/watch?v=8JKjvY4etTY)

Read an article about how event sourcing compliments blockchain [ 6 Components of any Blockchain design solution ] (http://blockchain.glorat.net/2015/11/16/6-components-of-any-blockchain-design-solution/)

### Platform Independent Petrinet Editor
see ./bitwrap_io/pnml/ directory for petri-nets included with bitwrap

Download:
* [PIPEv4](https://sourceforge.net/projects/pipe2/files/PIPEv4/PIPEv4.3.0/) - PIPEv4.3.0
* [PIPEv5](https://github.com/sarahtattersall/PIPE) - PIPEv5 being released as a jar on github

### Deployment

#### SQL w/ AWS lambda

* If you are planning using AWS-lambda:
  * configure the db connection using env vars
  * see: https://github.com/bitwrap/bitwrap-lambda

#### LMDB w/ Docker

Automated Build: https://hub.docker.com/r/bitwrap/bitwrap-io/~/dockerfile/

Run the image: ( by default uses LMDB storage )

    docker pull bitwrap/bitwrap-io

    docker run -it --name=bitwrap-io \
    -v /tmp:/repo \
    -p 127.0.0.1:8080:8080 \
    bitwrap/bitwrap-io:latest

