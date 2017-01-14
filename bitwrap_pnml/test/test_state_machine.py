"""
test state machine operations using python API
"""
from twisted.trial import unittest
from twisted.internet import defer
import bitwrap_pnml
from bitwrap_pnml.storage import Storage

class StateMachineTestCase(unittest.TestCase):
    """ test state_machine transactions """

    def setUp(self):
        Storage.truncate()
        self.machine = bitwrap_pnml.get('split_join_1')

    def tearDown(self):
        pass

    @defer.inlineCallbacks
    def test_machine_transaction(self):
        """ invoke state_machine transformations """

        req = self.machine.session({
            'oid': 'fake-oid',
            'action': 'T0',
            'payload': {'foo': 'bar'}
        })

        res = yield req.commit()
        assert res['event']['state'] == [0, 0, 0, 1, 0, 0]

        req = self.machine.session({
            'oid': 'fake-oid',
            'action': 'T1'
        })

        res = yield req.commit()
        assert res['event']['state'] == [1, 1, 0, 0, 0, 0]
