import os
import json
from txrdq.rdq import ResizableDispatchQueue
from twisted.internet import defer

import bitwrap
import bitwrap_io
from bitwrap_storage_actordb import Storage

QUEUE_WIDTH = int(os.environ.get('BITWRAP_QUEUE_WIDTH', 20))
LOCK=defer.DeferredLock()

def __handler__(txn):
    d = LOCK.run(txn._exec)

    def _return(res):
        txn.response.callback(res)

    d.addCallback(_return)


_QUEUE = ResizableDispatchQueue(__handler__, QUEUE_WIDTH)

def __dispatch__(txn):
    return _QUEUE.put(txn)

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
        self.response = defer.Deferred()
        job = __dispatch__(self)

        return self.response

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
