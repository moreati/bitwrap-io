"""
test tic-tac-toe events with bitwrap_io
using bitwrap schema file named "octothorpe"
"""

import time
import json
from twisted.internet import defer
from bitwrap_io.test import ApiTest
import bitwrap_io
from collections import OrderedDict


class EventTest(ApiTest):
    """
    --------------------------
    How 'octothorpe' state_machine
     lets you play tic-tac-toe:
    --------------------------
    move('BEGIN')

          |  |  
        --+--+--
          |  |  
        --+--+--
          |  |  

    'BEGIN' sets up the empty board
    --------------------------
    move(<action>)

    subsequent moves use a 3 char encoding

        00|01|02
        --+--+--
        10|11|12
        --+--+--
        20|21|22

    string: '(X|O)[0-2][0-2]'
    to specify token placment
    --------------------------
    move('X11')

          |  |  
        --+--+--
          |X |  
        --+--+--
          |  |  

    'X' takes middle center
    --------------------------
    move('O01')

          |O |  
        --+--+--
          |X |  
        --+--+--
          |  |  

    'O' takes top center

    """

    cli = ApiTest.client('api')

    def test_tic_tac_toe_sequence(self):
        """ test a sequence of tic-tac-toe transformations """
        d = defer.Deferred()
        oid = 'trial-' + time.time().__str__()
        schema = 'octothorpe'

        def test_response(res, code=200):
            """ test event response """
            print "\n", res.body
            self.assertEquals(res.code, code)
            obj = json.loads(res.body)
            return obj

        def test_transform(res, action):

            self.assertEqual(res['event']['error'], seq[action][1])
            self.assertEqual(res['event']['state'], seq[action][0])
            print "\n", json.dumps(res)

        def test_sequence(seq):
            """ generate a valid event stream """

            # seq[<previous_action>] = ([<expected_state_vector>], <error_code_int>)
            seq['BEGIN'] = ([0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0], 0)
            seq['X11']   = ([1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0], 0)
            seq['O11']   = ([0, 0, 0, 2, 0, 1, 1, 1, 0, -1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0], 1) # invalid
            seq['O00']   = ([0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0], 0)

            def tx(txt):
                """ send an action event """

                def _test(_):
                    print "\n* tx-response\n", 
                    return self.cli.transform({"schema": schema, "oid": oid, "action": txt})

                d.addCallback( _test)
                d.addCallback( lambda res: test_transform(res, txt))

            map(tx, seq)

        def test_stream(seq, count=0):
            """ test stream """

            def _test(_):
                print "\n* event-stream"
                return self.fetch('stream/octothorpe/'+ oid)

            d.addCallback( _test)
            d.addCallback( test_response )
            d.addCallback( lambda obj: self.assertEquals(len(obj['events']), count))

        def test_head():
            """ test head event """
            def _test(_):
                print "\n* event -", 0
                return self.fetch('head/octothorpe/'+ oid)

            d.addCallback( _test)
            d.addCallback( test_response )

        def test_prev(i):
            """ test event has previous"""

            def _test(obj):
              print "\n* event -", i
              self.assertTrue(obj['event']['previous'])
              return obj

            d.addCallback( _test)
            d.addCallback( lambda obj: self.fetch('event/octothorpe/'+ obj['event']['previous']))
            d.addCallback( test_response )

        def test_tail():
            """ test prev is empty """
            d.addCallback( lambda obj: self.assertFalse(obj['event']['previous']))
            d.callback(None) # kick off chain of defers

        seq = OrderedDict()
        test_sequence(seq)

        valid_event_count = len(filter(lambda x: x[1] == 0, seq.values()))
        test_stream(seq, count=valid_event_count)

        test_head()
        [ test_prev(i) for i in range(1, valid_event_count) ]
        test_tail()

        return d
