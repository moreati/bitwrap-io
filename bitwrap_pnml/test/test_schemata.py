"""
test calls against the json-rpc API

"""
import cyclone.httpclient
from twisted.internet.defer import inlineCallbacks
import bitwrap_pnml
from bitwrap_pnml.test import ApiTest


class SchemaTest(ApiTest):
    """
    setup rpc endpoint and invoke ping method
    """

    @inlineCallbacks
    def test_schema_transform(self):
        """ call transform python api """
        transformer = bitwrap_pnml.get('metaschema')

        res1 = yield transformer.transform({
            "schema": "metaschema",
            "oid": "metaschema",
            "action": "update",
            "payload": { 'xml': '<?xml version="1.0" encoding="ISO-8859-1"?><pnml></pnml>' }
        })

        assert res1['event']['error'] == 0
        assert res1['event']['state'] == [0, 1]

        res2 = yield transformer.transform({
            "schema": "metaschema",
            "oid": "metaschema",
            "action": "enable"
        })

        assert res1['event']['error'] == 0
        assert res2['event']['state'] == [1, 1]
        
    @inlineCallbacks
    def test_view(self):
        """ retrieve schema xml """
        res = yield ApiTest.fetch('schema/metaschema.xml')
        assert res.code == 200

    def test_update(self):
        """ upload a new PNML file """
        assert False
    test_update.skip = True
