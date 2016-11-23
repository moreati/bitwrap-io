import os
from bitwrap_io.api import JsonrpcHandler
import cyclone.web
from twisted.application import service, internet

_port = int(os.environ.get('BITWRAP_PORT', 8080))

application = service.Application("bitwrap")
io = cyclone.web.Application([(r"/api", JsonrpcHandler)])
svc = internet.TCPServer(_port, io, interface="0.0.0.0")
svc.setServiceParent(application)
