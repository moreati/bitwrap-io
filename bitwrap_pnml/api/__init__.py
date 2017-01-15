"""
bitwrap_pnml.api

this module defines a json-rpc api using cyclone.io
"""
import os
import cyclone.web
from bitwrap_pnml.api import transformer, schema, machine

def factory():
    """ build a valid cyclone app """
    return cyclone.web.Application([
        (r"/api", transformer.Handler),
        (r"/schemata", schema.ListResource),
        (r"/schema/(.*)", schema.Resource),
        (r"/machines.json", machine.ListResource),
        (r"/machine/(.*).json", machine.Resource)
    ])
