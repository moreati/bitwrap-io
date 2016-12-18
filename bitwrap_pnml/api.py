"""
bitwrap_pnml.api

this module defines a json-rpc api using cyclone.io
"""
import os
import cyclone.web
from cyclone.jsonrpc import JsonrpcRequestHandler
import bitwrap_pnml

_ALLOW_ORIGIN = os.environ.get('ALLOW_ORIGIN', '*')

def factory():
    """ build a valid cyclone app """
    return cyclone.web.Application([
        (r"/api", JsonrpcHandler)
    ])

def machine(schema):
    """ open machine by schema name """
    return bitwrap_pnml.get(schema)

class JsonrpcHandler(JsonrpcRequestHandler):
    """
    Bitwrap API resource
    """

    def set_default_headers(self):
        """ allow cors """
        self.set_header('Access-Control-Allow-Origin', _ALLOW_ORIGIN)
        self.set_header('Access-Control-Allow-Methods', 'POST')
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    @staticmethod
    def jsonrpc_ping():
        """ allow clients to test api connection """
        return True

    @staticmethod
    def jsonrpc_preview(msg):
        """ preview a state machine transformation"""
        return machine(msg['schema']).preview(msg)

    def jsonrpc_transform(self, msg):
        """ execute a state machine transformation"""
        msg['ip'] = self.request.remote_ip
        msg['endpoint'] = self.request.host

        return machine(msg['schema']).transform(msg)
