"""
test calls against the json-rpc API

"""
import cyclone.httpclient
from twisted.internet.defer import inlineCallbacks
import bitwrap_pnml
from bitwrap_pnml.test import ApiTest
import ujson as json


class EventTest(ApiTest):
    """
    setup rpc endpoint and invoke ping method
    """

    @inlineCallbacks
    def test_view(self):
        """ retrieve schema xml """
        oid = '000000000'
        transformer = bitwrap_pnml.get('counter')

        txn = yield transformer.transform({
            "schema": "counter",
            "oid": oid,
            "action": "INC",
            "payload": { 'foo': 'bar' }
        })

        url = 'event/' + txn['id'] + '.json'
        res = yield ApiTest.fetch('event/counter/' + txn['id'] + '.json')
        obj = json.loads(res.body)
        assert res.code == 200
        assert obj['event']['payload'] == { 'foo': 'bar' }

