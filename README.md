# Bitwrap-io

[![Build Status](https://travis-ci.org/bitwrap/bitwrap-io.svg?branch=master)](https://travis-ci.org/bitwrap/bitwrap-io)

A blockchain style eventsourcing service using cyclone.io and lmdb - Symas Lightning Memory-mapped Database

### Status - active development

Currently refactoring sql & lmdb storeage modules to be interchangeable.

#### Milestones


1. complete prototype[stackdump/marble](https://github.com/stackdump/marble).
   * support only PNML and elementary Petri-nets
   * support auth against Github
   * publish data only to keen.io
   * design event-stream driven models

2. refactor bitwrap-io by extending bitwrap-pnml
   * support colored Petri-nets
   * allow actions between elemetary nets
   * support colored-token protocols


### Reference

Read Martin Fowler's description of [Event Sourcing](http://martinfowler.com/eaaDev/EventSourcing.html)

Watch an event sourcing video from [Greg Young](https://www.youtube.com/watch?v=8JKjvY4etTY)

Read an article about how event sourcing compliments blockchain [ 6 Components of any Blockchain design solution ] (http://blockchain.glorat.net/2015/11/16/6-components-of-any-blockchain-design-solution/)

### PNML Tools 

see examples directory for petri-nets used for testing

* [PIPEv4](https://sourceforge.net/projects/pipe2/files/PIPEv4/PIPEv4.3.0/) - PIPEv4.3.0 (I found to be more stable than v5)
* [Platform Independent Petrinet Editor](https://github.com/sarahtattersall/PIPE) - v5 being released on github

### install

TODO: add 2 ways of running bitwrap w/ sql & w/ lmbd

### run

    twistd -n bitwrap --listen-address 127.0.0.1 --listen-port 8080 --io-path ./examples --lmdb-path /tmp

### Sample

See [examples/curl_rpc.sh](examples/curl_rpc.sh):

    request => {
        "id": 1484353985,
        "method": "transform",
        "params": [
            {
                "action": "INC",
                "oid": "000000000",
                "schema": "counter"
            }
        ]
    }
    
    
    response => {
        "error": null,
        "id": 1484353985,
        "result": {
            "event": {
                "action": "INC",
                "endpoint": "127.0.0.1:8080",
                "error": 0,
                "ip": "127.0.0.1",
                "oid": "000000000",
                "payload": {},
                "previous": "e56e9d211926d5bf",
                "state": [
                    2
                ]
            },
            "id": "398306197ef41ee9"
        }
    }
    PASS
