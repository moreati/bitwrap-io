"""
bitwrap_pnml.api

this module defines a json-rpc api using cyclone.io
"""
import os
import cyclone.web
from cyclone.web import RequestHandler
from bitwrap_pnml.api import rpc, pnml, machine

VERSION = 'v1'

def factory():
    """ build a valid cyclone app """
    return cyclone.web.Application([
        ("/", Index),
        ("/api", rpc.Handler),
        ("/machines.json", machine.ListResource),
        (r"/machine/(.*).json", machine.Resource),
        ("/pnml.json", pnml.ListResource),
        (r"/pnml/(.*).xml", pnml.Resource)
    ])

class Index(RequestHandler):
    """ index """

    def get(self):
        """ report api version """
        self.write({ __name__: VERSION})
