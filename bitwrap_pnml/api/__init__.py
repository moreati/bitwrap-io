"""
bitwrap_pnml.api

this module defines a json-rpc api using cyclone.io
"""
import os
import cyclone.web
from cyclone.web import RequestHandler
from bitwrap_pnml.api import rpc, pnml, state, machine, event

VERSION = 'v1'

def factory():
    """ build a valid cyclone app """
    return cyclone.web.Application([
        (r"/", Index),
        (r"/api", rpc.Handler),
        (r"/machine/(.*).json", machine.Resource),
        (r"/machines.json", machine.ListResource),
        (r"/event/(.*).json", event.Resource),
        (r"/pnml/(.*).xml", pnml.Resource),
        (r"/pnml.json", pnml.ListResource),
        (r"/(.*)/(.*).json", state.Resource)
    ])

class Index(RequestHandler):
    """ index """

    def get(self):
        """ report api version """
        self.write({ __name__: VERSION})
