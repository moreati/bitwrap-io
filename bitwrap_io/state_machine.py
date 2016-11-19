import os
import json
import bitwrap_io
from cyclone import redis
from twisted.internet import defer
import bitwrap
from bitwrap_storage_lmdb import Storage
import bitwrap_storage_lmdb

class StateMachine(object):
    """ token driven bitwrap state machine """

    def __init__(self, schema):
        self.machine = bitwrap.import_wrapfile(
            schema.__str__(),
            os.path.join(bitwrap_io.SCHEMA_PATH, schema + '.json')
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
        self.dry_run = False
        self.d = defer.Deferred()

    def payload(self, val):
        self.session['payload'] = val
        return self


    def execute(self):
        """ run the transaction without persisting state-vectors """
        self.request = self.machine.new_request(self.session)
        s = Storage.open(self.request['message']['signal']['schema'])
        self.response = s.commit(self.machine, self.request, dry_run=self.dry_run)
        self.response['actions'] = self.valid_actions()
        return self.response

    def valid_action(self, action):
        """ simulate an action with the latest cached values """
        return [] # FIXME: make this work an less ugly
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


    def simulate(self):
        """ simulate transform and return cache values """
        self.dry_run = True
        self.execute()
        return self.d

    def commit(self):
        """ run transform and persist state to storage """
        self.execute()
        return self.d
