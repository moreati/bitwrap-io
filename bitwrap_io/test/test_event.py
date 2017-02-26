"""
test calls against the json-rpc API

"""
import time
import ujson as json
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

    def test_tic_tac_toe_sequence(self):
        """ test a valid sequence of tic-tac-toe transformations """

        d = defer.Deferred()
        oid = 'trial-' + time.time().__str__()
        schema = 'octothorpe'
        seq = OrderedDict()

        def test_response(res):
            """ test event response """
            self.assertEquals(res.code, 200)
            obj = json.loads(res.body)
            #print "\n", obj
            return obj

        def test_transform(res, action):

            self.assertEqual(res['event']['error'], 0)
            self.assertEqual(res['event']['state'], seq[action])
            #print "\n", json.dumps(res)

        def test_sequence():
            """ generate a valid event stream """

            # seq[<previous_action>] = <expected_state_vector>
            seq['BEGIN'] = [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
            seq['X11']   = [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]
            seq['O00']   = [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0]

            def tx(txt):
                """ send an action event """

                d.addCallback( lambda _: self.cli.transform({"schema": schema, "oid": oid, "action": txt}))
                d.addCallback( lambda res: test_transform(res, txt))

            map(tx, seq)

        def test_stream():
            """ test stream """

            d.addCallback( lambda _: self.fetch('stream/octothorpe/'+ oid))
            d.addCallback( test_response )
            d.addCallback( lambda obj: self.assertEquals(len(obj['events']), len(seq)))

        def test_head():
            """ test head event """

            d.addCallback( lambda _: self.fetch('head/octothorpe/'+ oid))
            d.addCallback( test_response )

            d.addCallback( lambda obj: self.fetch('event/octothorpe/'+ obj['id']))
            d.addCallback( test_response )

        test_sequence()
        test_stream()
        test_head()

        d.callback(None)
        return d
