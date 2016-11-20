import bitwrap_io
from twisted.trial import unittest

from bitwrap_storage_lmdb import Storage

class MachineTestCase(unittest.TestCase):

    def setUp(self):
        Storage.truncate('tic-tac-toe')

    def tearDown(self):
        pass

    def test_machine_transaction(self):
        machine = bitwrap_io.get('tic-tac-toe')

        req = machine.session({
            'addresses': { 'sender': 'zim', 'target': 'dib' },
            'payload': {'foo': 'bar'},
            'signal': {'action': 'begin'}
        })

        res = req.commit()
        print "\n\n", res, "\n"

        assert res['hash'] == 'a12a03d7e8bf422e30cabac4581e49c212588a10'
        assert res['event']['cache']['dib'] != None
        assert res['event']['cache']['zim'] != None
