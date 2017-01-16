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
        oid = 'test_schemata.py'

        res1 = yield transformer.transform({
            "schema": "metaschema",
            "oid": oid,
            "action": "update",
            "payload": { 'xml': '<?xml version="1.0" encoding="ISO-8859-1"?><pnml></pnml>' }
        })

        assert res1['event']['error'] == 0
        assert res1['event']['state'] == [0, 1]

        res2 = yield transformer.transform({
            "schema": "metaschema",
            "oid": oid,
            "action": "enable"
        })

        assert res1['event']['error'] == 0
        assert res2['event']['state'] == [1, 1]
        
    @inlineCallbacks
    def test_view(self):
        """ retrieve schema xml """
        res = yield ApiTest.fetch('pnml/metaschema.xml')
        assert res.code == 200

    @inlineCallbacks
    def test_update(self):
        """
        upload a new PNML file
        and use it to invoke an transformation
        """
        split2 = bitwrap_pnml.get('split_join_1').machine.net.xml

        bitwrap_pnml.rm('split_join_2')
        res0 = yield ApiTest.fetch('pnml/split_join_2.xml')
        assert res0.code == 404

        res1 = yield ApiTest.fetch('pnml/split_join_2.xml', postdata = split2)
        assert res1.code == 200

        res2 = yield ApiTest.fetch('pnml/split_join_2.xml')
        assert res2.code == 200
        assert res2.body == split2

        cli = ApiTest.client('api')
        res = yield cli.transform({
            "schema": "split_join_2",
            "oid": 'fake-oid-1',
            "action": "T0",
        })

        assert res['event']['error'] == 0
        bitwrap_pnml.rm('split_join_2')
