import os
import cyclone.web
import yaml
import ujson as json


class Resource(cyclone.web.RequestHandler):
    """ open api specification """

    def set_default_headers(self):
        """ allow cors """
        self.set_header('Access-Control-Allow-Origin', os.environ.get('ALLOW_ORIGIN', '*'))
        self.set_header('Access-Control-Allow-Methods', 'GET')
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    def get(self):
        """ return swagger spec """
        self.set_header('Content-Type', 'application/json')
        with open(os.path.abspath(__file__ + '/../../../swagger.yml'), 'r') as stream:
            spec = json.dumps(yaml.load(stream))

        self.write(spec)
