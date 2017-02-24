"""

"""

from twisted.application import internet
from twisted.trial.unittest import TestCase
import cyclone.httpclient
from bitwrap_pnml.storage import Storage
from marble_io.api import factory as ApiFactory

IFACE = '127.0.0.1'
PORT = 8080

class ApiTest(TestCase):
    """ setup rpc endpoint and invoke ping method """

    def setUp(self):
        Storage.truncate()
        # pylint: disable=E1103
        self.service = internet.TCPServer(PORT, ApiFactory(), interface=IFACE)
        # pylint: enable=E1103
        self.service.startService()

    def tearDown(self):
        self.service.stopService()
        
    @staticmethod
    def url(resource):
        return 'http://%s:%s/%s' % (IFACE, PORT, resource)

    @staticmethod
    def client(resource):
        return cyclone.httpclient.JsonRPC(ApiTest.url(resource))

    @staticmethod
    def fetch(resource, **kwargs):
        return cyclone.httpclient.fetch(ApiTest.url(resource), **kwargs)
