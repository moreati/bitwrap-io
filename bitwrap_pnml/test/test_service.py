"""
test calls against the json-rpc API

"""
from twisted.trial.unittest import TestCase
from twisted.application import internet
from twisted.internet.defer import inlineCallbacks
import cyclone.httpclient
from bitwrap_pnml.storage import Storage
from bitwrap_pnml.api import factory as ApiFactory

IFACE = '127.0.0.1'
PORT = 8080

class PingTest(TestCase):
    """ setup rpc endpoint and invoke ping method """

    def setUp(self):
        Storage.truncate()
        self.service = internet.TCPServer(PORT, ApiFactory(), interface=IFACE)
        self.service.startService()
        self.cli = cyclone.httpclient.JsonRPC('http://%s:%s/api' % (IFACE, PORT))

    def tearDown(self):
        self.service.stopService()

    @inlineCallbacks
    def test_ping(self):
        """ ping the rpc api """
        flag = yield self.cli.ping()
        assert flag

    @inlineCallbacks
    def test_transform(self):
        """ call transform api """

        req = {
            "schema": "counter",
            "oid": "fakeoid-trial0",
            "action": "INC"
        }

        res = yield self.cli.transform(req)
        assert [1] == res['event']['state']
        assert 0 == res['event']['error']

        res = yield self.cli.transform(req)
        assert 'fakeoid-trial0' == res['event']['oid']
        assert [2] == res['event']['state']
        assert 0 == res['event']['error']
