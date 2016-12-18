""" ping the API """
from twisted.trial.unittest import TestCase
from twisted.application import internet
from twisted.internet import defer
import bitwrap_pnml.api as api
import cyclone.httpclient

IFACE = '127.0.0.1'
PORT = 8080
ENDPOINT = 'http://%s:%s/api' % (IFACE, PORT)

class PingTest(TestCase):
    """ setup rpc endpoint and invoke ping method """

    def setUp(self):
        self.service = internet.TCPServer(PORT, api.factory(), interface=IFACE)
        self.service.startService()

    def tearDown(self):
        self.service.stopService()

    @defer.inlineCallbacks
    def test_ping(self):
        """ ping the rpc api """
        cli = cyclone.httpclient.JsonRPC(ENDPOINT)
        flag = yield cli.ping()
        assert flag
