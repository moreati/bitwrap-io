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

    def get(self, schema, key):
        """ return event json """

        m = bitwrap_io.open(schema)
        oid = m.storage.encode_key(key)

        with m.storage.db.cursor() as txn:
            eventid = m.storage.db.state.head(oid)
            evt = m.storage.db.events.get(eventid)
            self.write(evt)

class ListResource(headers.Mixin, RequestHandler):
    """ index """

    def get(self, schema, key):
        """ return event json """
        m = bitwrap_io.open(schema)
        oid = m.storage.encode_key(key)

        with m.storage.db.cursor() as txn:
            self.write(m.storage.db.events.list(oid))
