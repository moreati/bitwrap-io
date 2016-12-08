import bitwrap_io
import twisted
from twisted.trial import unittest
from twisted.internet import defer
twisted.internet.base.DelayedCall.debug = True

from bitwrap_storage_actordb import Storage

class MachineTestCase(unittest.TestCase):

    def setUp(self):
        Storage.truncate('tic-tac-toe')

    def tearDown(self):
        pass

    @defer.inlineCallbacks
    def test_machine_transaction(self):
        machine = bitwrap_io.get('tic-tac-toe')

        req = machine.session({
            'addresses': { 'sender': 'zim', 'target': 'dib' },
            'payload': {'foo': 'bar'},
            'signal': {'action': 'begin'}
        })

        req.commit()
        res = yield req.commit()
        print "\n\n", res, "\n"

        #assert res['hash'] == '63193cf0e7bbf3ea'
        assert res['event']['cache']['dib'] != None
        assert res['event']['cache']['zim'] != None
