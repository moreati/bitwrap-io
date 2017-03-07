from zope.interface import implements

import os
from twisted.application import service, internet
from twisted.application.service import IServiceMaker, MultiService
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.plugin import IPlugin
from twisted.python import usage
Factory.noisy = False

class Options(usage.Options):

    optParameters = (
        ("listen-port", "p", int(os.environ.get('BITWRAP_PORT', 8080)), "The port number to listen on."),
        ("listen-address", "a", os.environ.get('BITWRAP_IFACE', "127.0.0.1"), "The listen address."),
        ("schema-path", "s", os.environ.get('SCHEMA_PATH', os.path.abspath(__file__ + '/../../../examples')), "Path to read *.pnml/*.json"),
        ("lmdb-path", "l", os.environ.get('LMDB_PATH', '/tmp'), "Path to write *.lmdb")
    )


class ServiceFactory(object):
    implements(IServiceMaker, IPlugin)

    tapname = "bitwrap"
    description = "statevector eventstore"
    options = Options

    def makeService(self, options):

        os.environ.get('SCHEMA_PATH', options['schema-path'])
        os.environ.get('LMDB_PATH', options['lmdb-path'])

        from bitwrap_io.api import factory as ApiFactory

        service = MultiService()

        bitwrap_node = internet.TCPServer(
            int(options['listen-port']),
            ApiFactory(),
            interface= options['listen-address'])

        service.addService(bitwrap_node)

        return service

serviceMaker = ServiceFactory()
