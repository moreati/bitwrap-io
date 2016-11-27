import os
import json
from txrdq.rdq import ResizableDispatchQueue
from twisted.internet import defer

import bitwrap
import bitwrap_io
from bitwrap_storage_lmdb import Storage
import bitwrap_storage_lmdb
from bitwrap_storage_arangodb import Storage as EventStore

POOL_SIZE = int(os.environ.get('BITWRAP_EVENTSTORE_POOL', 20))
LOCK=defer.DeferredLock()

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

    @defer.inlineCallbacks
    def execute(self):
        """ run the transaction without persisting state-vectors """
        self.request = self.machine.new_request(self.session)
        self.response = yield LOCK.run(self._exec)
        __dispatch__(self)
        defer.returnValue(self.response)

    def _exec(self, tries=0):
        stor = Storage.open(self.schema)
        return stor.commit(self.machine, self.request, dry_run=self.dry_run)

    def simulate(self):
        """ simulate transform and return cache values """
        self.dry_run = True
        return self.execute()

    def commit(self):
        """ run transform and persist state to storage """
        return self.execute()
