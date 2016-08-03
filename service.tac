import marble_io
import cyclone.web
from twisted.application import service, internet

application = service.Application("bitwrap")
io = cyclone.web.Application([(r"/api", marble_io.ApiHandler)])
svc = internet.TCPServer(8080, io, interface="0.0.0.0")
svc.setServiceParent(application)
