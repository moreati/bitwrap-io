"""
Lambda handler for bitwrap gateway api.
This handler expects events from these routes:

POST /api - jsonrpc api 
GET  /machine - list schema names
GET  /machine/{schema} - get machine json
GET  /event/{schema}/{eventid} - get event by id
GET  /head/{schema}/{oid} - get latest event for oid
"""

import json
import bitwrap_io
from bitwrap_io.storage import factory as StorageFactory

def success(body):
    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body": json.dumps(body)
    } 

def failure(msg='__UNHANDLED__'):
    raise Exception(msg)

def transform(event):
    """ perform a state machine transformation """
    msg = json.loads(event['body'])
    _s = msg['params'][0]['schema']

    err = None
    m = bitwrap_io.open(_s)

    print '__EVENT__', msg
    preview = msg['method'] != 'transform'
    res = m.session(msg['params'][0]).commit(dry_run=preview)

    if (not preview) and (not res['id']):
        err = -1

    res['schema'] = _s

    return success({
        "result": res,
        "error": err,
        "id": msg['id']
    })

def query(event):
    """ query the eventstore """

    _p = event['pathParameters']
    _s = _p['schema']

    m = bitwrap_io.open(_s)
    s = StorageFactory(backend='mysql')(_s, m)

    if not 'eventid' in _p and not 'oid' in _p:

        # show machine definition
        return success(m.machine.net.data)

    with s.db.cursor() as txn:

        if 'eventid' in _p:
            evt = s.db.events.get(_p["eventid"])
            return success(evt)
        
        if 'oid' in _p:
            head = s.db.state.head(_p["oid"])
            evt = s.db.events.get(head)
            return success(evt)

    failure()


def handler(event, context):
    """ dispatch gateway api event """

    if event['path'] == "/machine":
        return success(bitwrap_io.MACHINES.keys())

    if event['path'] == '/api':
        return transform(event)

    return query(event)
