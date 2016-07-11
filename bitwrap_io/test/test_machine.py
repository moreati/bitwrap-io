import bitwrap_io
from twisted.trial import unittest
from cyclone import redis
from twisted.internet import defer, reactor
import twisted

#twisted.internet.base.DelayedCall.debug = True

class MachineTestCase(unittest.TestCase):

    @defer.inlineCallbacks
    def setUp(self):
        self.rc = yield redis.ConnectionPool(bitwrap_io.redis_host, bitwrap_io.redis_port)
        self.rc.flushall()
        self.d = defer.Deferred()

        # add a delay so reactor has time to empty
        reactor.callLater(1, self.d.callback, None)

    @defer.inlineCallbacks
    def tearDown(self):
        self.rc.disconnect()
        yield self.d

    @defer.inlineCallbacks
    def test_console(self):
        karmanom = bitwrap_io.get('karmanom.com')

        response = {
           'cache': {
               'control': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               'dib': [0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 1],
               'zim': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
            },
           'context': {
               'action': [0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, -1],
               'control': [ 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
               'target': [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0 ],
               'sender': [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1 ],
            },
            'errors': [],
            'message': {
               'addresses': {'sender': 'zim', 'target': 'dib'},
               'signal': {'action': 'positive_tip', 'role': 1, 'schema': 'karmanom.com'}
            }
        }

        res = yield karmanom.console().sender('zim').target('dib').send('positive_tip').commit()
        print "\n\n", res, "\n"
        self.assertEqual(res, response)
