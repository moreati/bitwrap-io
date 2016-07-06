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

    @defer.inlineCallbacks
    def fetch(self, address):
        flag = yield self.rc.exists(address)

        if 0 == flag:
            defer.returnValue(None)
        else:
            val = yield self.rc.hmget(address, self.hash_keys)
            defer.returnValue(val)

    @defer.inlineCallbacks
    def new_request(self):
        """ run the transaction without persisting state-vectors """
        self.rc = yield redis.Connection(redis_host, redis_port)

        req = self.machine.new_request(self.session)
        sender = req['message']['addresses']['sender']
        target = req['message']['addresses']['target']

        req['cache'][sender] = yield self.fetch(sender)
        req['cache'][target] = yield self.fetch(target)

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

        defer.returnValue(self.response)

    @defer.inlineCallbacks
    def on_commit(self, response):
        """ save values to redis """

        if len(response['errors']) == 0:
            for key in response['cache']:
                if key == 'control':
                    continue

                r = response['cache'][key]
                h = dict(zip(range(0, len(r)), r))

                yield self.rc.hmset(key, h)

    def rollback(self):
        """ retrieve address values without running transaction """
        return self.execute()

    def commit(self):
        """ run transaction and commit state to persistent storage """
        x = self.execute()
        x.addCallback(self.on_commit)

        return x

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
