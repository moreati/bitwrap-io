import os
import json
from txrdq.rdq import ResizableDispatchQueue

import bitwrap
import bitwrap_io
from bitwrap_storage_lmdb import Storage
import bitwrap_storage_lmdb
from bitwrap_storage_arangodb import Storage as EventStore

POOL_SIZE = int(os.environ.get('BITWRAP_EVENTSTORE_POOL', 100))

def __handler__(txn):
    eventstore = EventStore.open(txn.schema)
    eventstore.commit(txn.machine, txn.response, dry_run=txn.dry_run)

_QUEUE = ResizableDispatchQueue(__handler__, POOL_SIZE)

def __dispatch__(txn):
    _QUEUE.put(txn)

class StateMachine(object):
    """ token driven bitwrap state machine """

    def __init__(self, schema):
        self.schema = schema.__str__()

        self.machine = bitwrap.import_wrapfile(
            self.schema,
            os.path.join(bitwrap_io.SCHEMA_PATH, schema + '.json')
        )

    def session(self, msg):
        txn = Transaction(self.machine, self.schema)

        return txn.sender(
                    msg['addresses']['sender']
                ).target(
                    msg['addresses']['target']
                ).payload(
                    msg.get('payload', {})
                ).send(
                    msg['signal']['action']
                )

    def transform(self, msg):
        return self.session(msg).commit()

    def preview(self, msg):
        return self.session(msg).simulate()


class Transaction(bitwrap.console.Session):
    """ state machine transaction """

    def __init__(self, machine, schema):
        self.schema = schema
        self.session = {
            'addresses': {},
            'signal': {},
            'payload': {},
        }

        self.machine = machine
        self.dry_run = False

    def payload(self, val):
        self.session['payload'] = val
        return self

    def execute(self):
        """ run the transaction without persisting state-vectors """
        self.request = self.machine.new_request(self.session)

        storage = Storage.open(self.request['message']['signal']['schema'])
        self.response = storage.commit(self.machine, self.request, dry_run=self.dry_run)
        __dispatch__(self)

        self.response['valid_actions'] = self.valid_actions()
        return self.response

    def valid_action(self, action):
        """ simulate an action with the latest cached values """
        _req = json.loads(json.dumps(self.response['event'])) # FIXME find better way to deepcopy request
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
        return self.execute()

    def commit(self):
        """ run transform and persist state to storage """
        return self.execute()
