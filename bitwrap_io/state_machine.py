import os
import json
import bitwrap_io
from cyclone import redis
from twisted.internet import defer
import bitwrap
from bitwrap_storage_pygit2 import Storage

class StateMachine(object):
    """ token driven bitwrap state machine """

    def __init__(self, schema):
        self.machine = bitwrap.open_json(
            schema.__str__(),
            os.path.join(bitwrap_io.schema_path, schema + '.json')
        )

    def console(self):
        return Transaction(self.machine)

    def session(self, msg):
        return self.console().sender(
                    msg['addresses']['sender']
                ).target(
                    msg['addresses']['target']
                ).payload(
                    msg.get('payload')
                ).send(
                    msg['signal']['action']
                )

    def transform(self, msg):
        return self.session(msg).commit()

    def preview(self, msg):
        return self.session(msg).simulate()


class Transaction(bitwrap.console.Session):
    """ state machine transaction """

    def __init__(self, machine):
        self.session = {
            'addresses': {},
            'signal': {},
            'payload': ()
        }

        self.machine = machine
        self.hash_keys = range(0, len(self.machine.null_action))
        self.dry_run = False
        self.d = defer.Deferred()

    def payload(self, val):
        self.session['payload'] = val
        return self

    @defer.inlineCallbacks
    def fetch(self, address):
        flag = yield self.rc.exists(address)

        if 0 == flag:
            defer.returnValue(None)
        else:
            val = yield self.rc.hmget(address, self.hash_keys)
            defer.returnValue(val)

    def store(self, address, val):
        hval = dict(zip(self.hash_keys, val))
        self.t.hmset(address, hval)

    @defer.inlineCallbacks
    def new_request(self):
        """ begin transaction """
        req = self.machine.new_request(self.session)
        req['actions'] = []
        sender = req['message']['addresses']['sender']
        target = req['message']['addresses']['target']

        self.t = yield self.rc.watch([sender, target])
        yield self.t.multi()

        req['cache'][sender] = yield self.fetch(sender)
        req['cache'][target] = yield self.fetch(target)

        s = Storage.open(req['message']['signal']['schema'])

        if req['cache'].get(sender) == None:
            req['cache'].pop(sender, None)
            try:
                req['cache'][sender] = s.fetch(sender)
            except:
                pass

        if req['cache'].get(target) == None:
            req['cache'].pop(target, None)
            try:
                 req['cache'][target] = s.fetch(target)
            except:
                pass

        defer.returnValue(req)

    @defer.inlineCallbacks
    def execute(self):
        """ run the transaction without persisting state-vectors """
        self.rc = yield redis.ConnectionPool(bitwrap_io.redis_host, bitwrap_io.redis_port)
        self.request = yield self.new_request()
        self.response = self.machine.execute(self.request)

        x = self.on_return()
        x.addErrback(self.on_error)

    def on_error(self, err):
        if self.t.inTransaction:
            self.t.discard()

        msg = err.type.__name__

        self.response['errors'] = [['__TRANSACTION_ERROR__', msg]]
        self.d.callback(self.response)
        self.rc.disconnect()

    def valid_action(self, action):
        """ simulate an action with the latest cached values """
        _req = json.loads(json.dumps(self.response)) # KLUDGE!
        _req['message']['signal']['action'] = action
        req = self.machine.new_request(_req['message'])
        req['cache'] = _req['cache']

        # bypass roles
        req['cache']['control'] = [1] * len(self.machine.places)

        res = self.machine.execute(req)

        return res['errors'] == []

    def valid_actions(self):
        actions = []
        for action in self.machine.transitions:
            if self.valid_action(action):
                actions.append(action)

        return actions

    @defer.inlineCallbacks
    def on_return(self):
        """ save values to redis """

        if not self.dry_run and self.response['errors'] == []:
            for key in self.response['cache']:
                if not key == 'control':
                    self.store(key, self.response['cache'][key])

            s = Storage.open(self.request['message']['signal']['schema'])
            git_response = s.commit(self.response)

            self.response['oid'] = git_response['oid'].__str__()
            self.response['hash'] = git_response['hash']


            yield self.t.commit()
        else:
            yield self.t.discard()

        self.response['actions'] = self.valid_actions()

        self.d.callback(self.response)
        self.rc.disconnect()

    def simulate(self):
        """ simulate transform and return cache values """
        self.dry_run = True
        self.execute()
        return self.d

    def commit(self):
        """ run transform and persist state to storage """
        self.execute()
        return self.d
