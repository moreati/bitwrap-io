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

class SchemaTest(TestCase):
    """ setup rpc endpoint and invoke ping method """

    def setUp(self):
        Storage.truncate()
        # pylint: disable=E1103
        self.service = internet.TCPServer(PORT, ApiFactory(), interface=IFACE)
        # pylint: enable=E1103
        self.service.startService()
        self.cli = cyclone.httpclient.JsonRPC('http://%s:%s/api' % (IFACE, PORT))

    def tearDown(self):
        self.service.stopService()

    @inlineCallbacks
    def test_schema_tranformation(self):
        """ call transform api """

        req = {
            "schema": "metaschema",
            "oid": "metaschema",
            "action": "update",
            "payload": { 'xml': '<?xml version="1.0" encoding="ISO-8859-1"?><pnml></pnml>' }
        }

        res = yield self.cli.transform(req)
        assert res['event']['state'] == [0, 1]
        assert res['event']['error'] == 0
        
    def test_schema_upload(self):
        # TODO: add routes that allow PNML schemata to be uploaded via the API
        assert False
    test_schema_upload.skip = True
