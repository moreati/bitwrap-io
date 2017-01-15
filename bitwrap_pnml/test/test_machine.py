"""
test calls against the json-rpc API

"""
import ujson as json
import cyclone.httpclient
from twisted.internet.defer import inlineCallbacks
from bitwrap_pnml.test import ApiTest


class MachineTest(ApiTest):
    """
    setup rpc endpoint and invoke ping method
    """

    @inlineCallbacks
    def test_list(self):
        """
        retrieve machine def as json
        NOTE: 'metaschema' is the only machine loaded by default
        """
        res = yield ApiTest.fetch('machines.json')
        assert res.code == 200
        obj = json.loads(res.body)

        assert obj['machines'] == ['metaschema']


    @inlineCallbacks
    def test_machine(self):
        """ retrieve machine def as json """
        res = yield ApiTest.fetch('machine/counter.json')
        assert res.code == 200
        machine = json.loads(res.body)
        assert machine['state'] == [0]
