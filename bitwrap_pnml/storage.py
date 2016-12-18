"""
bitwrap_pnml.storage - provide state machine storage using lmdb
"""
import os
import shutil
import lmdb
import xxhash
import ujson as json

REPO_ROOT = os.environ.get('BITWRAP_REPO_PATH', os.path.abspath(__file__ + '/../../'))
MAX_DB = int(os.environ.get('BITWRAP_REPO_MAX_DB', 10))
XX_SEED = int(os.environ.get('BITWRAP_HASH_SEED', 662607004))
MAP_SIZE = int(os.environ.get('BITWRAP_DB_SIZE', 1048576000))
DB_PATH = os.path.join(REPO_ROOT, 'bitwrap.lmdb')

_DB = lmdb.open(DB_PATH, max_dbs=MAX_DB, map_size=MAP_SIZE)

def open_db(base_name, label):
    """ open sub-db """
    key = base_name + label
    return _DB.open_db(key)

class Storage(object):
    """ lmdb Storage provider """

    @staticmethod
    def truncate():
        """ delete lmdb folder """
        if os.path.isdir(DB_PATH):
            shutil.rmtree(DB_PATH)

    @staticmethod
    def open(repo_name):
        """ open storage db """
        return Storage(repo_name)

    @staticmethod
    def encode_key(input_str):
        """ make sure keys are safe for lmdb """
        return input_str.encode('latin-1')

    @staticmethod
    def decode(val):
        """ unserialize json from lmdb """
        if val is None:
            return None
        else:
            return json.loads(val)

    def __init__(self, repo_name):
        self.state = open_db(repo_name, ':db')
        self.events = open_db(repo_name, ':events')
        self.transactions = open_db(repo_name, ':transactions')


    def commit(self, state_machine, req, dry_run=False):
        """ execute transition and persist to storage on success """

        with _DB.begin(write=(not dry_run)) as txn:
            oid = self.encode_key(req['oid'])
            state = self.decode(txn.get(oid, db=self.state)) or state_machine.machine['state']
            action = req['action']

            transition = state_machine.machine['transitions'][action]
            output = state_machine.vadd(state, transition['delta'])

            res = {
                "oid": oid,
                "action": action,
                "state": output,
                "payload": req.get('payload', {}),
                "previous": txn.get(oid, db=self.transactions),
                "error": 0
            }

            if dry_run or not state_machine.is_valid(output):
                res["error"] = 1
                return {'event': res}
            else:
                event_str = json.dumps(res)
                txnid = xxhash.xxh64(event_str, seed=XX_SEED).hexdigest()

                txn.put(oid, json.dumps(output), db=self.state)
                txn.put(txnid, event_str, db=self.events)
                txn.put(oid, txnid, db=self.transactions)

                return {'id': txnid, 'event': res}

    def fetch_str(self, key, database='state'):
        """ fetch raw json string from address keystore"""
        with _DB.begin(write=False) as txn:
            return txn.get(key, db=getattr(self, database))

    def fetch(self, key, database='state'):
        """ fetch and load json """
        return self.decode(self.fetch_str(key, database=getattr(self, database)))
