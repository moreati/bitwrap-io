"""
test state machine operations using python API
"""
from twisted.trial import unittest
from twisted.internet import defer
import bitwrap_pnml
from bitwrap_pnml.storage import Storage
import ujson as json

class StateMachineTestCase(unittest.TestCase):
    """ test state_machine transactions """

    def setUp(self):
        Storage.truncate()
        self.sm = bitwrap_pnml.get('tic-tac-toe')

    def tearDown(self):
        pass

    def test_inital_markings(self):
        #print json.dumps(self.sm.machine.machine['transitions']['X11'], indent=4)
        self.assertEquals(self.sm.machine.net.places['M11']['inital'], 1)
