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
        pass
    
    def commit(self):
        pass

    def open_db(self, base_name, label):
        """ open sub-db """
        key = base_name + label
        return self.conn.open_db(key)


    def cursor(self, dry_run=False):
        self.txn = self.conn.begin(write=(not dry_run))
        return self.txn

    def fetch_str(self, key, db_name='state'):
        """ fetch raw json string from address keystore"""
        with self.conn.begin(write=False) as txn:
            return txn.get(key, db=getattr(self, db_name))

    def fetch(self, key, db_key='state'):
        """ fetch and load json """
        return self.unserialize(self.fetch_str(key, db_name=db_key))


class State:
    """
    """

    def __init__(self, store):
        self.store = store
        self.table = store.open_db(store.schema, ':state')
        self.schema = self.store.schema

    def get(self, oid):
        return store.txn.get(oid, db=self.table)

    def put(self, oid, vector=[], head=None):
        pass

    def head(self, oid, vector=[], prev=None):
        pass

    def vector(self, oid):
        rec = self.store.txn.get(oid, db=self.table)

        if rec  is None:
            return self.store.state_machine.machine['state']
        else:
            return self.unserialize(rec[0])

class Transactions:
    """
    """

    def __init__(self, store):
        self.store = store
        self.table = store.open_db(store.schema, ':transactions')
        self.schema = self.store.schema

    def get(self, oid):
        pass

class Events:
    """
    """

    def __init__(self, store):
        self.store = store
        self.table = store.open_db(store.schema, ':events')
        self.schema = self.store.schema

    def put(self, eventid, body, prev):
        pass

    def get(self, eventid):
        pass

    def list(self, oid):
        pass

