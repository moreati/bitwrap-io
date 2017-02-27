"""
bitwrap_io.api - this module defines routes
"""

import os
import cyclone.web
from cyclone.web import RequestHandler
from bitwrap_io.api import config, headers, rpc, pnml, machine, event

VERSION = 'v3'

class Index(RequestHandler):
    """ index """

    def get(self):
        self.render("index.html")

class Version(headers.Mixin, RequestHandler):
    """ index """

    def get(self):
        """ report api version """
        self.write({__name__: VERSION})

def factory():
    """ cyclone app factory """

    _settings = config.settings()

    handlers = [
        (r"/", Index),
        (r"/api", rpc.Handler),
        (r"/version", Version),
        (r"/config/(.*).json", config.Resource),
        (r"/pnml/(.*).xml", pnml.Resource),
        (r"/pnml.json", pnml.ListResource),
        (r"/machine/(.*)", machine.Resource),
        (r"/machine", machine.ListResource),
        (r"/event/(.*)/(.*)", event.Resource),
        (r"/head/(.*)/(.*)", event.HeadResource),
        (r"/stream/(.*)/(.*)", event.ListResource)
    ]

    return cyclone.web.Application(handlers, **_settings)
