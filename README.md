# Bitwrap-pnml

[![Build Status](https://travis-ci.org/stackdump/bitwrap-pnml.svg?branch=master)](https://travis-ci.org/stackdump/bitwrap-pnml)

A port of bitwrap-io that uses Petri-Net Markup Language (PNML) to construct state machines that model resources and events.

See [getbitwrap.com](http://getbitwrap.com) for more info.

### PNML Tools 

see examples directory for petri-nets used for testing

* [PIPEv4](https://sourceforge.net/projects/pipe2/files/PIPEv4/PIPEv4.3.0/) - PIPEv4.3.0 (I found to be more stable than v5)
* [Platform Independent Petrinet Editor](https://github.com/sarahtattersall/PIPE) - v5 being released on github

### install

    pip install bitwrap_pnml

### run

    twistd -n bitwrap --listen-address 127.0.0.1 --listen-port 8080 --pnml-path ./examples --lmdb-path /tmp

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
