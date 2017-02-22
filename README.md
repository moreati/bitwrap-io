# Bitwrap-io

[![Build Status](https://travis-ci.org/bitwrap/bitwrap-io.svg?branch=master)](https://travis-ci.org/bitwrap/bitwrap-io)

A blockchain-style eventstore.


### Status

Developing Web App - http://bitwrap.github.io 

* completed components and prototypes
   * [stackdump/marble](https://github.com/stackdump/marble)
   * [stackdump/bitwrap-pnml](https://github.com/stackdump/bitwrap-pnml)
   * [bitwrap/bitwrap-lambda](https://github.com/bitwrap/bitwrap-lambda)
   * [bitwrap/bitwrap-ui](https://github.com/bitwrap/bitwrap-ui)
   * [bitwrap/wrapserver](https://github.com/bitwrap/wrapserver)


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

TODO: add instructions about how you'd need mysql or just use the filesystem (default)

### run

    twistd -n bitwrap --listen-address 127.0.0.1 --listen-port 8080 --io-path ./examples --lmdb-path /tmp

