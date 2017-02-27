"""
bitwrap_io.storage.base
"""

import os
import xxhash
import ujson as json

XX_SEED = int(os.environ.get('HASH_SEED', 662607004))

class Storage(object):
    """ base.Storage """

    def __init__(self):
        self.db = None
        self.state_machine = None

    @staticmethod
    def encode_key(input_str):
        """ make sure keys are encoded for db """
        return input_str.encode('latin-1')

    @staticmethod
    def serialize(val):
        """ unserialize json from db """
        return json.dumps(val)

    @staticmethod
    def unserialize(val):
        """ unserialize json from db """
        if val is None or val == '':
            return None
        else:
            return json.loads(val)

    @staticmethod
    def hexdigest(val):
        """ use xxhash """
        return xxhash.xxh64(val, seed=XX_SEED).hexdigest()

    def commit(self, req, dry_run=False):
        """ execute transition and persist to storage on success """

        oid = self.encode_key(req['oid'])
        action = req['action']
        transition = self.state_machine.machine['transitions'][action]

        with self.db.cursor():
            output = self.state_machine.vadd(self.db.state.vector(oid), transition['delta'])
            prev = self.db.state.head(oid)

            res = {
                "oid": oid,
                "action": action,
                "state": output,
                "payload": req.get('payload', {}),
                "previous": prev,
                "endpoint": req.get('endpoint', None),
                "ip": req.get('ip', None),
                "error": 0
            }

            if not self.state_machine.is_valid(output):
                dry_run = True
                res["error"] = 1
                self.db.rollback()

            if not dry_run:
                eventid = self.hexdigest(self.serialize(res))
                self.db.events.put(eventid, body=res, prev=prev)
                self.db.state.put(oid, vector=output, head=eventid)
                self.db.commit()

                return {'id': eventid, 'event': res}
            else:
                return {'id': None, 'event': res}
