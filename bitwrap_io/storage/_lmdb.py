"""
bitwrap_pnml.storage - provide state machine storage using lmdb
"""

import os
import glob
import lmdb
from bitwrap_io.storage import base

REPO_ROOT = os.environ.get('LMDB_PATH', os.path.abspath(__file__ + '/../../'))
MAX_DB = int(os.environ.get('REPO_MAX_DB', 10))
MAP_SIZE = int(os.environ.get('DB_SIZE', 1048576000))

_POOL = {}

class Storage(base.Storage):
    """ lmdb.Storage """

    @staticmethod
    def db_files(pattern='*.lmdb'):
        """ list all lmdb files """
        return glob.glob(REPO_ROOT + '/' + pattern)

    def __init__(self, repo_name, state_machine):
        self.state_machine = state_machine

        if repo_name in _POOL:
            self.db = _POOL[repo_name]
        else:
            self.db = Datastore(repo_name, machine=self.state_machine)
            _POOL[repo_name] = self.db

class Datastore(object):
    """ lmdb.Datastore """

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
        """ rollback txn """
        pass

    def commit(self):
        """ commit txn """
        pass

    def open_db(self, base_name, label):
        """ open sub-db """
        key = base_name + ':' + label
        return self.conn.open_db(key)


    def cursor(self, dry_run=False):
        """ start db transaction """
        self.txn = self.conn.begin(write=(not dry_run))
        return self.txn


class State(object):
    """ lmdb.State"""

    def __init__(self, store):
        self.store = store
        self.table = store.open_db(store.schema, ':state')

    def get(self, oid):
        """ read state """

        return {
            'oid': oid,
            'head': self.head(oid),
            'vector': self.vector(oid),
            'schema': self.store.schema
        }

    def put(self, oid, vector=None, head=None):
        """ write state """
        if head:
            self.store.txn.put(oid, head, db=self.store.transactions.table)

        return self.store.txn.put(oid, Storage.serialize(vector), db=self.table)

    def head(self, oid):
        """ get head eventid by oid """
        return self.store.txn.get(oid, db=self.store.transactions.table)

    def vector(self, oid):
        """ get statevector by oid """
        rec = self.store.txn.get(oid, db=self.table)

        if rec  is None:
            return self.store.state_machine.machine['state']
        else:
            return Storage.unserialize(rec)

class Transactions(object):
    """ lmdb.Transactions """

    def __init__(self, store):
        self.store = store
        self.table = store.open_db(store.schema, ':transactions')

class Events(object):
    """ lmdb.Events """

    def __init__(self, store):
        self.store = store
        self.table = store.open_db(store.schema, ':events')

    def put(self, eventid, **kwargs):
        """ write event """
        return self.store.txn.put(eventid, Storage.serialize(kwargs['body']), db=self.table)

    def get(self, eventid):
        """ read event """
        rec = self.store.txn.get(eventid, db=self.table)

        if rec  is None:
            return {'id': None, 'event': None}
        else:
            event = Storage.unserialize(rec)
            return {'id': eventid, 'event': event, 'schema': self.store.schema}

    def list(self, oid):
        """ buld list using a loop """

        result = []
        eventid = self.store.state.head(oid)
        res = self.get(eventid)

        if not res:
            return result

        evt = dict(res['event'])

        if not evt['previous']:
            result.append(evt)
        else:
            while evt['previous']:
                result.append(evt)
                previd = Storage.encode_key(evt['previous'])
                evt = self.get(previd)['event']

            result.append(evt)

        return {'events': result, 'oid': oid, 'schema': self.store.schema}
