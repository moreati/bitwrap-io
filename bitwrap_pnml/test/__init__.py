"""

"""

from twisted.application import internet
from twisted.trial.unittest import TestCase
import cyclone.httpclient
from bitwrap_pnml.storage import Storage
from bitwrap_pnml.api import factory as ApiFactory

IFACE = '127.0.0.1'
PORT = 8080

def url(resource):
    return 'http://%s:%s/%s' % (IFACE, PORT, resource)

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
    def client(resource):
        return cyclone.httpclient.JsonRPC(url(resource))

    @staticmethod
    def fetch(resource):
        return cyclone.httpclient.fetch(url(resource))
