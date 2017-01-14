"""
test calls against the json-rpc API

"""
import cyclone.httpclient
from twisted.internet.defer import inlineCallbacks
from bitwrap_pnml.test import ApiTest


class SchemaTest(ApiTest):
    """
    setup rpc endpoint and invoke ping method
    """

    transformer = ApiTest.client('api')

    @inlineCallbacks
    def test_schema_tranformation(self):
        """ call transform api """

        req = {
            "schema": "metaschema",
            "oid": "metaschema",
            "action": "update",
            "payload": { 'xml': '<?xml version="1.0" encoding="ISO-8859-1"?><pnml></pnml>' }
        }

        res = yield self.transformer.transform(req)
        assert res['event']['state'] == [0, 1]
        assert res['event']['error'] == 0
        
    def test_schema_post(self):
        """ upload a new PNML file """
        assert False
    test_schema_post.skip = True

    def test_schema_get(self):
        """ retrieve schema xml """
        assert False
    test_schema_get.skip = True
