"""
test calls against the json-rpc API

"""
from twisted.internet.defer import inlineCallbacks
from bitwrap_pnml.test import ApiTest


class RpcTest(ApiTest):
    """ invoke rpc methods """

    cli = ApiTest.client('api')

    @inlineCallbacks
    def test_transform(self):
        """ call transform api """

        req = {
            "schema": "counter",
            "oid": "fakeoid-trial0",
            "action": "INC"
        }

        res = yield self.cli.transform(req)
        assert res['event']['state'] == [1]
        assert res['event']['error'] == 0

        res = yield self.cli.transform(req)
        assert res['event']['oid'] == 'fakeoid-trial0'
        assert res['event']['state'] == [2]
        assert res['event']['error'] == 0

    @inlineCallbacks
    def test_preview(self):
        """ call transform api """

        req = {
            "schema": "counter",
            "oid": "fakeoid-trial1",
            "action": "INC"
        }

        res = yield self.cli.preview(req)
        assert res['event']['error'] == 0
        assert res['event']['state'] == [1]

        res = yield self.cli.preview(req)
        assert res['event']['state'] == [1]
        assert res['event']['error'] == 0
