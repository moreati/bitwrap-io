"""
test calls against the json-rpc API

"""
import time
import json
import cyclone.httpclient
from twisted.internet.defer import inlineCallbacks
from twisted.internet import defer
from bitwrap_io.test import ApiTest
import bitwrap_io
from collections import OrderedDict


class EventTest(ApiTest):
    """
    Test tic-tac-toe state machine: #octothorpe
    """

    cli = ApiTest.client('api')

    def test_tic_tac_toe_events(self):
        """ test a valid sequence of tic-tac-toe transformations """

        d = defer.Deferred()
        oid = 'trial-' + time.time().__str__()
        schema = 'octothorpe'

        def test_sequence():
            """ generate a valid event stream """

            seq = OrderedDict()

            # seq[<previous_action>] = <expected_state_vector>
            seq['BEGIN'] = [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
            seq['X11']   = [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]
            seq['O00']   = [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0]

            def tx(txt):
                """ send an action event """

                def _test(res, action):

                    self.assertEqual(res['event']['error'], 0)
                    self.assertEqual(res['event']['state'], seq[action])
                    #print json.dumps(res, indent=4)

                d.addCallback( lambda _: self.cli.transform({"schema": schema, "oid": oid, "action": txt}))
                d.addCallback( lambda res: _test(res, txt))

            for action in seq:
                tx(action)


        def test_stream():
            """ test event stream output """

            def _test(res):
                # FIXME
                #self.assertEquals(res.code, 200)
                print res.body

            d.addCallback( lambda _: self.fetch('stream/octothorpe/'+ oid))
            d.addCallback( lambda res: _test(res) )

        test_sequence()
        test_stream()
        d.callback(None)

        return d
