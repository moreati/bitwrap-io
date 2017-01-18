import os
import cyclone.web
import yaml
import ujson as json

with open(os.path.abspath(__file__ + '/../../../swagger.yml'), 'r') as stream:
    SPEC = json.dumps(yaml.load(stream))

class Resource(cyclone.web.RequestHandler):
    """ open api specification """

    def set_default_headers(self):
        """ allow cors """
        self.set_header('Access-Control-Allow-Origin', os.environ.get('ALLOW_ORIGIN', '*'))
        self.set_header('Access-Control-Allow-Methods', 'GET')
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        self.set_header('Content-Type', 'application/json')

    def get(self):
        """ return swagger spec """
        self.write(SPEC)
