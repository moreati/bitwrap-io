"""
bitwrap_pnml.api

this module defines routes
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
        (r"/pnml/(.*).xml", pnml.Resource),
        (r"/pnml.json", pnml.ListResource),
        (r"/event/(.*)/(.*).json", event.Resource),
        (r"/(.*)/(.*).json", state.Resource)
    ])

class Index(RequestHandler):
    """ index """

    def get(self):
        """ report api version """
        self.write({ __name__: VERSION})
