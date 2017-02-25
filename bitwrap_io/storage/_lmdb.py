"""
bitwrap_pnml.storage - provide state machine storage using lmdb
"""

import os
import glob
import shutil
import lmdb
import xxhash
import ujson as json

REPO_ROOT = os.environ.get('LMDB_PATH', os.path.abspath(__file__ + '/../../'))
MAX_DB = int(os.environ.get('REPO_MAX_DB', 10))
XX_SEED = int(os.environ.get('HASH_SEED', 662607004))
MAP_SIZE = int(os.environ.get('DB_SIZE', 1048576000))

_POOL = {}

class Storage(object):
    """ lmdb Storage provider """

    def open_db(self, base_name, label):
        """ open sub-db """
        key = base_name + label
        return self.db.open_db(key)

    @staticmethod
    def db_files(pattern='*.lmdb'):
        return glob.glob(REPO_ROOT + '/' + pattern)

    @staticmethod
    def truncate(pattern='*.lmdb'):
        """ delete all lmdb folders """
        for d in db_files(pattern):
            shutil.rmtree(d)

    @staticmethod
    def open(repo_name):
        """ open storage db """
        return Storage(repo_name)

    @staticmethod
    def encode_key(input_str):
        """ make sure keys are safe for lmdb """
        return input_str.encode('latin-1')

    @staticmethod
    def serialize(val):
        """ unserialize json from lmdb """
        return json.dumps(val)

    @staticmethod
    def unserialize(val):
        """ unserialize json from lmdb """
        if val is None:
            return None
        else:
            return json.loads(val)

    def __init__(self, repo_name):
        if _POOL.has_key(repo_name):
            self.db = _POOL[repo_name]
        else:
            self.db = lmdb.open(os.path.join(REPO_ROOT, repo_name + '.lmdb'), max_dbs=MAX_DB, map_size=MAP_SIZE)
            _POOL[repo_name] = self.db

        self.state = self.open_db(repo_name, ':state')
        self.events = self.open_db(repo_name, ':events')
        self.transactions = self.open_db(repo_name, ':transactions')


    def commit(self, state_machine, req, dry_run=False):
        """ execute transition and persist to storage on success """

        with self.db.begin(write=(not dry_run)) as txn:
            oid = self.encode_key(req['oid'])
            state = self.unserialize(txn.get(oid, db=self.state)) or state_machine.machine['state']
            action = req['action']

            transition = state_machine.machine['transitions'][action]
            output = state_machine.vadd(state, transition['delta'])

            res = {
                "oid": oid,
                "action": action,
                "state": output,
                "payload": req.get('payload', {}),
                "previous": txn.get(oid, db=self.transactions),
                "endpoint": req.get('endpoint', None),
                "ip": req.get('ip', None),
                "error": 0
            }

            if not state_machine.is_valid(output):
                dry_run = True
                res["error"] = 1

            if not dry_run:
                event_str = self.serialize(res)
                txnid = xxhash.xxh64(event_str, seed=XX_SEED).hexdigest()
                txn.put(txnid, event_str, db=self.events)
                txn.put(oid, self.serialize(output), db=self.state)
                txn.put(oid, txnid, db=self.transactions)

                return {'id': txnid, 'event': res}
            else:
                return {'event': res}

    def fetch_str(self, key, db_name='state'):
        """ fetch raw json string from address keystore"""
        with self.db.begin(write=False) as txn:
            return txn.get(key, db=getattr(self, db_name))

    def fetch(self, key, db_key='state'):
        """ fetch and load json """
        return self.unserialize(self.fetch_str(key, db_name=db_key))
