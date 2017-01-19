"""
bitwrap_pnml.api

this module defines routes
"""
import os
import cyclone.web
from cyclone.web import RequestHandler
from bitwrap_pnml.api import headers, spec, rpc, pnml, state, machine, event

VERSION = 'v1'

VENDOR_PATH = os.path.abspath(__file__ + '/../../../vendor')

def factory():
    """ build a valid cyclone app """
    return cyclone.web.Application([
        (r"/", Index),
        (r"/api", rpc.Handler),
        (r"/swagger.json", spec.Resource),
        (r"/ui/?", cyclone.web.RedirectHandler, {"url": "/ui/index.html"}),
        (r"/ui/(.+)", cyclone.web.StaticFileHandler, {"path": VENDOR_PATH + '/swagger-ui'}),
        (r"/machine/(.*).json", machine.Resource),
        (r"/machines.json", machine.ListResource),
        (r"/pnml/(.*).xml", pnml.Resource),
        (r"/pnml.json", pnml.ListResource),
        (r"/head/(.*)/(.*).json", event.HeadResource),
        (r"/event/(.*)/(.*).json", event.Resource),
        (r"/(.*)/(.*).json", state.Resource)
    ])

class Index(headers.Mixin, RequestHandler):
    """ index """

    def get(self):
        """ report api version """
        self.write({ __name__: VERSION})
