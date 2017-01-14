"""

"""
import cyclone.web
from cyclone.jsonrpc import JsonrpcRequestHandler
import bitwrap_pnml

MACHINE = bitwrap_pnml.get('metaschema')

class ListResource(JsonrpcRequestHandler):
    """
    List PNML
    """

    def set_default_headers(self):
        """ allow cors """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET')
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    def get(schema_name):
        """ list schema as xml """
        pass

class Resource(JsonrpcRequestHandler):
    """
    REST for PNML
    """

    def set_default_headers(self):
        """ allow cors """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST')
        self.set_header('Access-Control-Allow-Methods', 'GET')
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    def get(self, request):
        """ read schema xml """
        pass

    def post(self, request):
        """ update schema xml """
        # TODO: load bitwra
        pass
