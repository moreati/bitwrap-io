"""
bitwrap_io.storage - storage interface for either lmdb or mysql backend
"""
import os
import glob
import shutil
import xxhash
import json

# FIXME should support lmdb backend also
from bitwrap_io.storage.sql import Datastore

_POOL = {}
XX_SEED = 662607004 

class Storage(object):
    """ dynamo Storage provider """

    @staticmethod
    def truncate(pattern='*'):
        """ drop and recreate database """
        pass

    @staticmethod
    def encode_key(input_str):
        """ make sure keys are safe """
        return input_str.encode('latin-1')

    @staticmethod
    def serialize(val):
        """ unserialize json from db """
        return json.dumps(val)

    @staticmethod
    def unserialize(val):
        """ unserialize json from db """
        if val is None:
            return None
        else:
            return json.loads(val)


    def __init__(self, repo_name, state_machine):
        self.state_machine = state_machine

        if repo_name in _POOL:
            self.db = _POOL[repo_name]
        else:
            # TODO: conditionally open either LMDB or sql
            self.db = Datastore(repo_name, machine=self.state_machine)
            _POOL[repo_name] = self.db



    # TODO: refactor to call mysql or lmdb commit
    def commit(self, req, dry_run=False):
        """ execute transition and persist to storage on success """

        oid = self.encode_key(req['oid'])
        action = req['action']
        transition = self.state_machine.machine['transitions'][action]

        with self.db.cursor() as txn:

            output = self.state_machine.vadd(self.db.state.vector(oid), transition['delta'])
            prev = self.db.state.head(oid)

            res = {
                "oid": oid,
                "action": action,
                "state": output,
                "payload": req.get('payload', {}),
                "previous": prev,
                "endpoint": req.get('endpoint', None),
                "error": 0
            }

            if not self.state_machine.is_valid(output):
                dry_run = True
                res["error"] = 1
                self.db.conn.rollback()

            if not dry_run:
                eventid = xxhash.xxh64(self.serialize(res), seed=XX_SEED).hexdigest()
                self.db.events.put(eventid, body=res, prev=prev)
                self.db.state.put(oid, vector=output, head=eventid)
                self.db.conn.commit()

                return {'id': eventid, 'event': res}
            else:
                return {'id': None, 'event': res}

    def fetch(self, key, db_name='state'):
        """ fetch raw json string from address keystore"""
        with self.db.begin(write=False) as txn:
            return txn.get(key, db=getattr(self, db_name))
