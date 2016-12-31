""" test state machine operations """
import twisted
from twisted.trial import unittest
from twisted.internet import defer
import ujson as json
import bitwrap_pnml
from bitwrap_pnml.storage import Storage

twisted.internet.base.DelayedCall.debug = True

class StorageTestCase(unittest.TestCase):
    """ test machine transactions """

    def setUp(self):
        Storage.truncate()
        self.machine = bitwrap_pnml.get('split_join_1')
        self.store = Storage.open('split_join_1')

    def tearDown(self):
        pass

    @defer.inlineCallbacks
    def test_statevector_storage(self):
        """
        invoke state machine transformations
        and then check storage state
        """

        req = self.machine.session({
            'oid': 'fake-oid2',
            'action': 'T0',
            'payload': {'foo': 'bar'}
        })

        yield req.commit()

        res = yield self.store.fetch_str('fake-oid2')
        # pylint: disable=E1103
        assert res == json.dumps([0, 0, 0, 1, 0, 0])
        # pylint: enable=E1103

        res = yield self.store.fetch('fake-oid2')
        assert res == [0, 0, 0, 1, 0, 0]
