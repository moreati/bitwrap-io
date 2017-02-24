"""
bitwrap_io.api - this module defines routes
"""
import os
import cyclone.web
from cyclone.web import RequestHandler
from bitwrap_pnml.api import headers, spec, rpc, pnml, state, machine, event

VERSION = 'v2'

VENDOR_PATH = os.path.abspath(__file__ + '/../../vendor')

class Index(RequestHandler):
    """ index """

    def get(self):
        self.render("index.html")

def factory():

    settings = {
        'cookie_secret': os.environ.get('COOKIE_SECRET', ''),
        #github_client_id=os.environ.get('GITHUB_CLIENT_ID'),
        #github_secret=os.environ.get('GITHUB_SECRET'),
        'template_path': os.path.dirname(__file__),
        #login_url="/auth/login",
        #xsrf_cookies=True, # REVIEW: is this usable via api ?
        'debug': True
    }

    """ build a valid cyclone app """
    return cyclone.web.Application([
        (r"/", cyclone.web.RedirectHandler, {"url": "/ui/index.html"}),
        (r"/api", rpc.Handler),
        (r"/version", Version),
        (r"/pnml/(.*).xml", pnml.Resource),
        (r"/pnml.json", pnml.ListResource),
        (r"/event/(.*)/(.*)", event.Resource),
        (r"/machine/(.*)", machine.Resource),
        (r"/machine", machine.ListResource),
        (r"/head/(.*)/(.*)", event.HeadResource),
        (r"/stream/(.*)/(.*)", event.ListResource)
    ])

class Version(headers.Mixin, RequestHandler):
    """ index """

    def get(self):
        """ report api version """
        self.write({ __name__: VERSION})
