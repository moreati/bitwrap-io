# Bitwrap-io

[![Build Status](https://travis-ci.org/bitwrap/bitwrap-io.svg?branch=master)](https://travis-ci.org/bitwrap/bitwrap-io)

A blockchain-style eventstore.

### Status

Developing Web App - http://bitwrap.github.io 

* completed components and prototypes
   * [stackdump/marble](https://github.com/stackdump/marble) - use bitwrap with keen.io
   * [stackdump/marble-ui](https://github.com/stackdump/marble-ui) - a single page web-app
   * [stackdump/bitwrap-pnml](https://github.com/stackdump/bitwrap-pnml) - an eventstore prototype based solely on PNML
   * [stackdump/lambda-test](https://github.com/stackdump/lambda-test) - test deploying bitwrap-lambda to AWS lambda
   * [bitwrap/bitwrap-lambda](https://github.com/bitwrap/bitwrap-lambda) - bitwrap with sql backend suitable for lambda
   * [bitwrap/wrapserver](https://github.com/bitwrap/wrapserver) - npm module for rendering state-machines as .svg images
   * [gitwrap-dot-com/gitwrap-io](https://github.com/gitwrap-dot-com/gitwrap-io) - bitwrap using git commit messages as an eventstore


### Roadmap

WIP - Refactoring sql & lmdb storeage modules to be interchangeable

* support all pnml functions when creating/reading json definitions
* support colored tokens
  * colors allow expressions of roles and transient properties
* support inhibitor arcs
  * inhibitors provide basic boolean operations 
* allow cross-net interaction between elementary nets
  * existing: Event(oid)
  * new: Event(oid, sender=<oid>)

### Reference

Read Martin Fowler's description of [Event Sourcing](http://martinfowler.com/eaaDev/EventSourcing.html)

Watch an event sourcing video from [Greg Young](https://www.youtube.com/watch?v=8JKjvY4etTY)

Read an article about how event sourcing compliments blockchain [ 6 Components of any Blockchain design solution ] (http://blockchain.glorat.net/2015/11/16/6-components-of-any-blockchain-design-solution/)

### PNML Tools 

see examples directory for petri-nets used for testing

* [PIPEv4](https://sourceforge.net/projects/pipe2/files/PIPEv4/PIPEv4.3.0/) - PIPEv4.3.0 (simulator seems more stable than v5)
* [Platform Independent Petrinet Editor](https://github.com/sarahtattersall/PIPE) - v5 being released on github

### install

* CI/CD: this package is built and deployed to pypi
* Another github project deploys the build to aws lambda using travis.ci:
  *  see [stackdump/lambda-test](https://github.com/stackdump/lambda-test) as an example of how to do this.

#### LMDB

make sure to set the REPO environment vars to manage database file location

NOTE: LMDB is not supported when deploying to lambda due to local filesystem restrictions.

#### sql w/ AWS lambda

* If you are not planning using AWS-lambda:
  * You may provide the database credentials when invoking the twisted plugin at runtime,
  * or by setting environment variables.


* If you are building a package to upload to lambda:
  * create a python script called rds_config.py
  * and make sure you add it to your python library

    # ./rds_config.py
    db_username = "bitwrap"
    db_password = "5eGPelW8r8ea"
    db_name = "bitwrap" 
    rds_host  = "bitwrap-prod01.cplrgtpb61fz.us-east-1.rds.amazonaws.com"

### run

    twistd -n bitwrap --listen-address 127.0.0.1 --listen-port 8080 --io-path ./examples --lmdb-path /tmp

