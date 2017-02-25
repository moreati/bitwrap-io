"""
bitwrap_io.api - this module defines routes
"""
import os
import cyclone.web
from cyclone.web import RequestHandler
from bitwrap_io.api import headers, rpc, pnml, state, machine, event

VERSION = 'v3'

class Index(RequestHandler):
    """ index """

    def get(self):
        self.render("index.html")

class Version(headers.Mixin, RequestHandler):
    """ index """

    def get(self):
        """ report api version """
        self.write({ __name__: VERSION})

class Config(headers.Mixin, RequestHandler):
    """ config """

    def get(self, stage):
        """ direct web app to api """

        self.write({
            'endpoint': "http://127.0.0.1:8080",
            'stage': stage
        })

def factory():
    """ cyclone app factory """

    settings = {
        #github_client_id=os.environ.get('GITHUB_CLIENT_ID'),
        #github_secret=os.environ.get('GITHUB_SECRET'),
        # TODO: add github auth
        #login_url="/auth/login",
        #xsrf_cookies=True, # REVIEW: is this usable w/ rpc ?
        'cookie_secret': os.environ.get('COOKIE_SECRET', ''),
        'template_path': os.path.join(os.path.dirname(__file__), '../templates'),
        'debug': True
    }

    return cyclone.web.Application([
        (r"/", Index),
        (r"/api", rpc.Handler),
        (r"/version", Version),
        (r"/config/(.*).json", Config),
        (r"/pnml/(.*).xml", pnml.Resource),
        (r"/pnml.json", pnml.ListResource),
        (r"/event/(.*)/(.*)", event.Resource),
        (r"/machine/(.*)", machine.Resource),
        (r"/machine", machine.ListResource),
        (r"/head/(.*)/(.*)", event.HeadResource),
        (r"/stream/(.*)/(.*)", event.ListResource)
    ], **settings)
