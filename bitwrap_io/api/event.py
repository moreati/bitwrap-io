"""
return statevectors
"""
from cyclone.web import RequestHandler
import bitwrap_io.storage
from bitwrap_io.api import headers
import bitwrap_io
import ujson as json

class Resource(headers.Mixin, RequestHandler):
    """ index """

    def get(self, schema, key):
        """ return event json """

        m = bitwrap_io.open(schema)
        eventid = m.storage.encode_key(key)
        stor = m.storage.encode_key(schema)
        storage = m.storage(stor, m)

        res = storage.store.events.get(eventid)
        
        if res:
            return self.write(json.dumps(res))

        self.write({ 'event': None })
        self.set_status(404)

class HeadResource(headers.Mixin, RequestHandler):
    """ index """

    def get(self, schema, oid):
        """ return event json """

        m = bitwrap_io.open(schema)
        key = m.storage.encode_key(oid)
        stor = m.storage.encode_key(schema)
        storage = m.storage(stor, m)

        # FIXME: fetch_str isn't interchangable b/t sql and lmdb storage providers
        head_event = storage.fetch_str(key, db_name='transactions')

        res = storage.fetch_str(head_event, db_name='events')
        
        if res:
            self.write('{ "event": ' + res + ', "id": "' + head_event +'" }')
        else:
            self.write({ 'event': None })
            self.set_status(404)

class ListResource(headers.Mixin, RequestHandler):
    """ index """

    def get(self, schema, key):
        """ return event json """
        m = bitwrap_io.open(schema)
        oid = m.storage.encode_key(key)

        with m.storage.db.cursor() as txn:
            self.write(m.storage.serialize(m.storage.db.events.list(oid)))
