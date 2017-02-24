"""
statevector storage using mysql

NOTE: this module expects the db config to be in a module called rds_config
"""

import sys
import pymysql
import json
import base64
import rds_config # get db creds

def open_db(cfg):
    return pymysql.connect(
        cfg.rds_host,
        user=cfg.db_username,
        passwd=cfg.db_password,
        db=cfg.db_name,
        connect_timeout=5
    )

class Datastore:

    def __init__(self, name, conn=None, machine=None, txn=None):
        if not conn:
            self.conn = open_db(rds_config)
        else:
            self.conn = conn

        self.schema = name
        self.state = State(self)
        self.events = Events(self)
        self.state_machine = machine
        self.txn = txn

    def cursor(self):
        self.txn = self.conn.cursor()
        return self.txn

class State:
    """
    StateModel get and set state by oid
    """

    def __init__(self, store):
        self.store = store
        self.table = store.schema + '_' + 'state';
        self.schema = self.store.schema

    def put(self, oid, vector=[], head=None):

        if head is None:
            head = 'null'
        else:
            head = '"' + head + '"'

        body = json.dumps(vector)
        sql = 'UPDATE bitwrap.state SET `vector` = "%s", `head` = %s WHERE `oid` = "%s" AND `schema` = "%s"' % ( body, head, oid, self.schema )

        res = self.store.txn.execute(sql);
        if res == 0:
            res = self.store.txn.execute(
                'INSERT INTO bitwrap.state VALUES ( "%s", "%s", "%s", %s)' % (self.schema, oid, body, head)
            )

        return res

    def head(self, oid, vector=[], prev=None):
        sql = 'SELECT `head` FROM bitwrap.state WHERE `oid` = "%s" AND `schema` = "%s"' % ( oid, self.schema )

        if 0 == self.store.txn.execute(sql):
            return None
        else:
            return self.store.txn.fetchone()[0]

    def vector(self, oid):
        sql = 'SELECT `vector` FROM bitwrap.state WHERE `oid` = "%s" AND `schema` = "%s"' % (oid, self.schema)

        if 0 == self.store.txn.execute(sql):
            return self.store.state_machine.machine['state']
        else:
            rec = self.store.txn.fetchone()
            return json.loads(rec[0])

    def get(self, oid):
        sql = 'SELECT `oid`, `vector`, `head` FROM bitwrap.state WHERE `oid` = "%s" AND `schema` = "%s"' % (oid, self.schema)

        if 0 == self.store.txn.execute(sql):
            # use default state
            return self.store.state_machine.machine['state']
        else:
            rec = self.store.txn.fetchone()

            return {
                'oid': rec[0],
                'vector': json.loads(rec[1]),
                'head': rec[2],
                'schema': self.schema
            }

class Events:
    """
    EventsModel Create and view events
    """

    def __init__(self, store):
        self.store = store
        self.table = store.schema + '_' + 'events';
        self.schema = self.store.schema

    def put(self, eventid, body, prev):

        oid = body.get('oid', None)

        body = base64.b64encode(json.dumps(body))
        _sql = 'INSERT INTO bitwrap.events( `oid`, `schema`, `eventid`, `body`, `previous`) VALUES ( "%s", "%s", "%s", "%s", "%s")'
        sql = _sql % (oid, self.schema, eventid, body, prev)
        return self.store.txn.execute(sql)

    def get(self, eventid):
        sql = 'SELECT `body`, `id` FROM bitwrap.events WHERE `eventid` = "%s" and `schema` = "%s"' % (eventid, self.schema)

        if 0 == self.store.txn.execute(sql):
            return { 'id': None, 'event': {}, 'schema': self.schema, 'seq': None }
        else:
            rec = self.store.txn.fetchone()
            return { 'id': eventid, 'event': json.loads(base64.b64decode(rec[0])), 'schema': self.schema, 'seq': rec[1] }

    def list(self, oid):
        sql = 'SELECT `body`, `eventid`, `id` FROM bitwrap.events WHERE `oid` = "%s" and `schema` = "%s" ORDER BY id DESC' % (oid, self.schema)

        if 0 == self.store.txn.execute(sql):
            return { 'events': [] }
        else:
            result = []
            for rec in self.store.txn.fetchall():
                e = json.loads(base64.b64decode(rec[0]))
                e['id'] = rec[1]
                e['seq'] = rec[2]
                result.append(e)

            return { 'events': result, 'oid': oid, 'schema': self.schema }


#TODO: make database name configurable instead of hardcoding 'bitwrap'
if __name__ == '__main__':

    print 'migrating database'

    conn = pymysql.connect(
        rds_config.rds_host,
        user=rds_config.db_username,
        passwd=rds_config.db_password,
        db='mysql',
        connect_timeout=5
    )

    with conn.cursor() as txn:
        #txn.execute("DROP DATABASE bitwrap")
        txn.execute("CREATE DATABASE bitwrap")
        txn.execute("use bitwrap ; CREATE TABLE `state` ( `schema` varchar(255) NOT NULL, `oid` varchar(255) NOT NULL, `vector` text, `head` varchar(255) DEFAULT NULL, PRIMARY KEY (`schema`, `oid`));")
        txn.execute("use bitwrap ; CREATE TABLE `events` ( `id` int NOT NULL AUTO_INCREMENT, `oid` varchar(255), `schema` varchar(255), `eventid` varchar(255) NOT NULL, `body` text, `previous` varchar(255) DEFAULT NULL, PRIMARY KEY (`id`, `oid`, `schema`, `eventid`) );")

    conn.commit()

