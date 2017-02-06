"""
test calls against the json-rpc API

"""
import cyclone.httpclient
from twisted.internet.defer import inlineCallbacks
import bitwrap_pnml
from bitwrap_pnml.test import ApiTest
import ujson as json


class StateTest(ApiTest):
    """
    setup rpc endpoint and invoke ping method
    """

    @inlineCallbacks
    def test_view(self):
        """ retrieve schema xml """
        oid = '000000000'
        transformer = bitwrap_pnml.get('counter')

        ex = yield transformer.transform({
            "schema": "counter",
            "oid": oid,
            "action": "INC"
        })
        res = yield ApiTest.fetch('state/counter/' + oid + '.json')

        obj = json.loads(res.body)
        assert res.code == 200

        # KLUDGE: dirty tests [1] or [2]
        assert obj['state']['vector'][0] > 0


