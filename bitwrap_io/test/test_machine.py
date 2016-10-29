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
        Storage.truncate('tic-tac-toe')
        self.rc = yield redis.ConnectionPool(bitwrap_io.redis_host, bitwrap_io.redis_port)
        self.rc.flushall()

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.rc.disconnect()

    @defer.inlineCallbacks
    def test_with_and_without_redis(self):
        machine = bitwrap_io.get('tic-tac-toe')
        self.maxDiff=None

        response = {
           'cache': {
           },
           'actions': [],
           'context': {
               'action': [],
               'control': [],
               'target': [],
               'sender': []
            },
            'errors': [],
            'hash': '402604e1c0d0f1b84a3329543f9cb99e41bac51f',
            'message': {
               'addresses': {'sender': 'zim', 'target': 'dib'},
               'signal': {'action': 'begin', 'role': 1, 'schema': 'tic-tac-toe'},
               'payload': { 'foo': 'bar'}
            }
        }

        res = yield machine.console().sender('zim').target('dib').send('begin').payload({'foo': 'bar'}).commit()


        print "\n\n", res, "\n"
