import os
import cyclone.web
import yaml
import ujson as json
from bitwrap_pnml.api import headers

with open(os.path.abspath(__file__ + '/../swagger.yml'), 'r') as stream:
    SPEC = json.dumps(yaml.load(stream))

class Resource(headers.Mixin, cyclone.web.RequestHandler):
    """ open api specification """

    def get(self):
        """ return swagger spec """
        #self.set_header('Access-Control-Allow-Methods', 'GET')
        self.write(SPEC)
