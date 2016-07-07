import sys
import cyclone.jsonrpc
from twisted.python import log
from twisted.internet import defer, reactor
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

def main():
    log.startLogging(sys.stdout)
    application = cyclone.web.Application([
        (r"/api", JsonrpcHandler),
    ])

    reactor.listenTCP(8080, application)
    reactor.run()

if __name__ == "__main__":
    main()
