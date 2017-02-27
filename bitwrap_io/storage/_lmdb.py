"""
bitwrap_pnml.storage - provide state machine storage using lmdb
"""

import os
import glob
import shutil
import lmdb
from bitwrap_io.storage import base

REPO_ROOT = os.environ.get('LMDB_PATH', os.path.abspath(__file__ + '/../../'))
MAX_DB = int(os.environ.get('REPO_MAX_DB', 10))
MAP_SIZE = int(os.environ.get('DB_SIZE', 1048576000))

_POOL = {}

class Storage(base.Storage):
    """ lmdb Storage provider """

    @staticmethod
    def db_files(pattern='*.lmdb'):
        return glob.glob(REPO_ROOT + '/' + pattern)

    def __init__(self, repo_name, state_machine):
        self.state_machine = state_machine

        if repo_name in _POOL:
            self.db = _POOL[repo_name]
        else:
            self.db = Datastore(repo_name, machine=self.state_machine)
            _POOL[repo_name] = self.db

class Datastore(object):

    def __init__(self, name, conn=None, machine=None, txn=None):
        if not conn:
            self.conn = lmdb.open(
                os.path.join(REPO_ROOT, name + '.lmdb'),
                max_dbs=MAX_DB,
                map_size=MAP_SIZE
            )
        else:
            self.conn = conn

        self.schema = name
        self.state = State(self)
        self.events = Events(self)
        self.transactions = Transactions(self)
        self.state_machine = machine
        self.txn = txn

    def rollback(self):
        # FIXME
        pass
    
    def commit(self):
        # FIXME
        pass

    def open_db(self, base_name, label):
        """ open sub-db """
        key = base_name + ':' + label
        return self.conn.open_db(key)


    def cursor(self, dry_run=False):
        self.txn = self.conn.begin(write=(not dry_run))
        return self.txn


class State:
    """
    """

    def __init__(self, store):
        self.store = store
        self.table = store.open_db(store.schema, ':state')

    def get(self, oid):

        return {
            'oid': oid,
            'head': self.head(oid),
            'vector': self.vector(oid),
            'schema': self.store.schema
        }

    def put(self, oid, vector=[], head=None):
        if head:
            self.store.txn.put(oid, head, db=self.store.transactions.table)

        return self.store.txn.put(oid, Storage.serialize(vector), db=self.table)

    def head(self, oid):
        return self.store.txn.get(oid, db=self.store.transactions.table)

    def vector(self, oid):
        rec = self.store.txn.get(oid, db=self.table)

        if rec  is None:
            return self.store.state_machine.machine['state']
        else:
            return Storage.unserialize(rec)

class Transactions:
    """
    """

    def __init__(self, store):
        self.store = store
        self.table = store.open_db(store.schema, ':transactions')

class Events:
    """
    """

    def __init__(self, store):
        self.store = store
        self.table = store.open_db(store.schema, ':events')

    def put(self, eventid, body={}, **kwargs):
        return self.store.txn.put(eventid, Storage.serialize(body), db=self.table)

    def get(self, eventid):
        rec = self.store.txn.get(eventid, db=self.table)

        if rec  is None:
            return { 'id': None, 'event': None }
        else:
            event = Storage.unserialize(rec)
            return { 'id': eventid, 'event': event , 'schema': self.store.schema }

    def list(self, oid):
        """ buld list using a loop """

        events=[]

        eventid = self.store.state.head(oid)

        res = self.get(eventid)

        if not res:
            return events
        else:
            evt = res['event']

        if not evt['previous']:
            events.append(evt)
        else:
            while evt['previous']:
                events.append(evt)
                previd = Storage.encode_key(evt['previous'])
                evt = self.get(previd)['event']

            events.append(evt)

        return events

