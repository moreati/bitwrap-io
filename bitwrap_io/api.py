import sys
import cyclone.jsonrpc
import bitwrap_io

def machine(schema):
    return bitwrap_io.get(schema)

class JsonrpcHandler(cyclone.jsonrpc.JsonrpcRequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST')        
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    def jsonrpc_transform(self, msg):
        return machine(msg['signal']['schema']).transform(msg)

    def jsonrpc_preview(self, msg):
        return machine(msg['signal']['schema']).preview(msg)
