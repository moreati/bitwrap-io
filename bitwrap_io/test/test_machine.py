import bitwrap_io
from twisted.trial import unittest
from cyclone import redis
from twisted.internet import defer, reactor
import twisted

from bitwrap_storage_pygit2 import Storage

#twisted.internet.base.DelayedCall.debug = True

class MachineTestCase(unittest.TestCase):

    @defer.inlineCallbacks
    def setUp(self):
        Storage.truncate('karmanom.com')
        self.rc = yield redis.ConnectionPool(bitwrap_io.redis_host, bitwrap_io.redis_port)
        self.rc.flushall()

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.rc.disconnect()

    @defer.inlineCallbacks
    def test_with_and_without_redis(self):
        karmanom = bitwrap_io.get('karmanom.com')
        self.maxDiff=None

        response = {
           'cache': {
               'control': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               'dib': [0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 1],
               'zim': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
            },
           'actions': [u'refund',
                       u'recall',
                       u'pay_user',
                       u'vote',
                       u'deposit',
                       u'deposit_donation',
                       u'deposit_system',
                       u'withdraw_system'],
           'context': {
               'action': [0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, -1],
               'control': [ 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
               'target': [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0 ],
               'sender': [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1 ],
            },
            'errors': [],
            'hash': '402604e1c0d0f1b84a3329543f9cb99e41bac51f',
            'message': {
               'addresses': {'sender': 'zim', 'target': 'dib'},
               'signal': {'action': 'positive_tip', 'role': 1, 'schema': 'karmanom.com'},
               'payload': { 'foo': 'bar'}
            }
        }

        res = yield karmanom.console().sender('zim').target('dib').send('positive_tip').payload({'foo': 'bar'}).commit()


        print "\n\n", res, "\n"

        res.pop('oid') # ditch :oid since it is unique per commit
        self.assertEqual(res, response)

        # simulate a loss of redis storage
        self.rc.flushall()

        # run another transaction 
        res2 = yield karmanom.console().sender('zim').target('dib').send('deposit_system').payload({'baz': 'qux'}).commit()
        print res2['cache']
        self.assertEqual(res2['cache']['dib'], [0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 3, 1])



