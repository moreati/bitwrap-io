"""
bitwrap_pnml.api

this module defines a json-rpc api using cyclone.io
"""
import os
from cyclone.jsonrpc import JsonrpcRequestHandler
import bitwrap_pnml

class Handler(JsonrpcRequestHandler):
    """
    Invoke transform actions on PNML state machines
    """

    def set_default_headers(self):
        """ allow cors """
        self.set_header('Access-Control-Allow-Origin', os.environ.get('ALLOW_ORIGIN', '*'))
        self.set_header('Access-Control-Allow-Methods', 'POST')
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    @staticmethod
    def jsonrpc_ping():
        """ allow clients to test api connection """
        return True

    @staticmethod
    def jsonrpc_preview(msg):
        """ preview a state machine transformation"""
        return bitwrap_pnml.get(msg['schema']).preview(msg)

    def jsonrpc_transform(self, msg):
        """ execute a state machine transformation"""
        msg['ip'] = self.request.remote_ip
        msg['endpoint'] = self.request.host

        return bitwrap_pnml.get(msg['schema']).transform(msg)
