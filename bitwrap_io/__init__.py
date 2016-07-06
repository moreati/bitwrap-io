import os
import sys
import logging
import bitwrap
from cyclone import redis
from twisted.internet import defer
from twisted.internet.protocol import Factory
Factory.noisy = False

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
log = logging.getLogger(__package__)

redis_host = os.environ.get('REDIS_PORT_6379_TCP_ADDR', '127.0.0.1')
redis_port = os.environ.get('REDIS_PORT_6379_TCP_PORT', 6379)

machines = {}
schema_path = os.environ.get('BITWRAP_SCHEMA_PATH', os.path.join(os.path.dirname(__file__), '../tests/machine/'))

def get(schema):
    """ get machine """
    if schema in machines:
        m = machines[schema]
    else:
        m = StateMachine(schema)
        machines[schema] = m

    return m

class Txn(bitwrap.console.Session):
    """ state machine transaction """
    def __init__(self, machine):
        self.session = {
            'addresses': {},
            'signal': {}
        }

        self.machine = machine
        self.hash_keys = range(0, len(self.machine.null_action))
        self.dry_run = False

    @defer.inlineCallbacks
    def fetch(self, address):
        flag = yield self.rc.exists(address)

        if 0 == flag:
            defer.returnValue(None)
        else:
            val = yield self.rc.hmget(address, self.hash_keys)
            defer.returnValue(val)

    @defer.inlineCallbacks
    def store(self, address, val):
        hval = dict(zip(self.hash_keys, val))
        yield self.t.hmset(address, hval)

    @defer.inlineCallbacks
    def new_request(self):
        """ run the transaction without persisting state-vectors """
        self.rc = yield redis.ConnectionPool(redis_host, redis_port)

        req = self.machine.new_request(self.session)
        sender = req['message']['addresses']['sender']
        target = req['message']['addresses']['target']

        req['cache'][sender] = yield self.fetch(sender)
        req['cache'][target] = yield self.fetch(target)

        self.t = yield self.rc.watch([sender, target])
        yield self.t.multi()

        if req['cache'][sender] == None:
            del(req['cache'][sender])

        if req['cache'][target] == None:
            del(req['cache'][target])

        defer.returnValue(req)

    @defer.inlineCallbacks
    def execute(self):
        """ run the transaction without persisting state-vectors """

        self.request = yield self.new_request()
        self.response = yield self.machine.execute(self.request)

        if self.dry_run:
            x = self.t.discard()
            x.addErrback(self.on_error)
            x.addCallback(self.on_complete)
        else:
            x = self.on_commit(self.request)
            x.addErrback(self.on_error)
            x.addCallback(self.on_complete)

        defer.returnValue(self.response)

    def on_error(self, err):
        if self.t.inTransaction:
            self.t.discard()
        log.error(err.type)

    def on_complete(self, res):
        self.rc.disconnect()

    @defer.inlineCallbacks
    def on_commit(self, response):
        """ save values to redis """

        if response['errors'] == []:
            for key in response['cache']:
                if not key == 'control':
                    yield self.store(key, response['cache'][key])
            yield self.t.commit()
        else:
            yield self.t.discard()

    def rollback(self):
        """ retrieve address values without running transaction """
        self.dry_run = True
        return self.execute()

    def commit(self):
        """ run transaction and commit state to persistent storage """
        return self.execute()

class StateMachine(object):

    def __init__(self, schema):
        self.machine = bitwrap.open_json(schema.__str__(), os.path.join(schema_path, schema + '.json'))

    def console(self):
        return Txn(self.machine)

    def session(self, msg):
        return self.console().sender(
                    msg['addresses']['sender']
                ).target(
                    msg['addresses']['target']
                ).send(
                    msg['signal']['action']
                )

    def transform(self, msg):
        return self.session(msg).commit()

    def preview(self, msg):
        return self.session(msg).rollback()
