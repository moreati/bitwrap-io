import sys
import cyclone.jsonrpc
from twisted.python import log
from twisted.internet import defer, reactor
import bitwrap_io

class JsonrpcHandler(cyclone.jsonrpc.JsonrpcRequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST')        
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    def jsonrpc_transform(self, msg):
        machine = bitwrap_io.get(msg['signal']['schema'])
        return machine.transform(msg)

    def jsonrpc_preview(self, msg):
        machine = bitwrap_io.get(msg['signal']['schema'])
        return machine.transform(msg)

    # REVIEW: perform async call on bitwrap machine
    # @defer.inlineCallbacks
    # def jsonrpc_geoip(self, address):
    #     result = yield cyclone.httpclient.fetch(
    #         "http://freegeoip.net/json/%s" % address.encode("utf-8"))
    #     defer.returnValue(result.body)


def main():
    log.startLogging(sys.stdout)
    application = cyclone.web.Application([
        (r"/api", JsonrpcHandler),
    ])

    reactor.listenTCP(8080, application)
    reactor.run()

if __name__ == "__main__":
    main()
