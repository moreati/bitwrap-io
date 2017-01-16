"""
test calls against the json-rpc API

"""
import ujson as json
import cyclone.httpclient
from twisted.internet.defer import inlineCallbacks
import bitwrap_pnml
from bitwrap_pnml.test import ApiTest


# preload some schemata
bitwrap_pnml.get('metaschema')
bitwrap_pnml.get('counter')

class MachineTest(ApiTest):
    """ test machine resources"""

    @inlineCallbacks
    def test_list(self):
        """
        retrieve machine def as json
        NOTE: 'metaschema' is the only machine loaded by default
        """
        res = yield ApiTest.fetch('machines.json')
        assert res.code == 200
        obj = json.loads(res.body)


        assert obj['machines'] == ['metaschema', 'counter']


    @inlineCallbacks
    def test_machine(self):
        """
        retrieve machine def as json
        'state' represents the default state for a machine
        """
        res = yield ApiTest.fetch('machine/counter.json')
        assert res.code == 200
        obj = json.loads(res.body)
        assert obj['machine']['name'] == 'counter'
