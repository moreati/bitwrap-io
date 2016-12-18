# Bitwrap-pnml

[![Build Status](https://travis-ci.org/stackdump/bitwrap-pnml.svg?branch=master)](https://travis-ci.org/stackdump/bitwrap-pnml)

A port of bitwrap-io that uses Petri-Net Markup Language (PNML) to construct state machines that model resources and events.

See [getbitwrap.com](http://getbitwrap.com) for more info.

### PNML Tools 

see examples directory for petri-nets used for testing

* [PIPEv4](https://sourceforge.net/projects/pipe2/files/PIPEv4/PIPEv4.3.0/) - PIPEv4.3.0 (I found to be more stable than v5)
* [Platform Independent Petrinet Editor](https://github.com/sarahtattersall/PIPE) - v5 being released on github


### Sample

request:

    curl 'http://127.0.0.1:8080/api' \
           -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
           --data '{"id":2,"method":"transform","params":[{"oid": "fake-oid7", "schema": "counter", "action": "INC" }]}'


response:

    {
      "error": null,
       "id": 2,
       "result": {
         "id": "3939f6b3b16f70dc",
         "event": { "oid": "fake-oid7",
                    "state": [1],
                    "error": 0,
                    "action": "INC",
                    "payload": {},
                    "previous": "830121e8a6bb3b6d" }
       }
    }
