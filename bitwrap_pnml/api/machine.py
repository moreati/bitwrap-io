"""

"""
import os
from cyclone.jsonrpc import JsonrpcRequestHandler
import bitwrap_pnml

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
        """ list machines as json """
        pass

class Resource(JsonrpcRequestHandler):
    """

    """

    def set_default_headers(self):
        """ allow cors """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET')
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    def get(self, request):
        """ return state machine definition as json """
        pass
