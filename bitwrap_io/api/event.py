"""
return statevectors
"""
from cyclone.web import RequestHandler
import bitwrap_io.storage
from bitwrap_io.api import headers
import bitwrap_io
import ujson as json

class Resource(headers.Mixin, RequestHandler):
    """ /event/{schema}/{eventid} """

    def get(self, schema, key):
        """ get event by eventid """

        m = bitwrap_io.open(schema)
        eventid = m.storage.encode_key(key)

        with m.storage.db.cursor() as txn:
            evt = m.storage.db.events.get(eventid)
            self.write(evt)

class HeadResource(headers.Mixin, RequestHandler):
    """ /head/{schema}/{oid} """

    def get(self, schema, key):
        """ get head event by oid"""

        m = bitwrap_io.open(schema)
        oid = m.storage.encode_key(key)

        with m.storage.db.cursor() as txn:
            eventid = m.storage.db.state.head(oid)
            evt = m.storage.db.events.get(eventid)
            self.write(evt)

class ListResource(headers.Mixin, RequestHandler):
    """ /stream/{schema}/{oid} """

    def get(self, schema, key):
        """ return event stream """
        m = bitwrap_io.open(schema)
        oid = m.storage.encode_key(key)

        with m.storage.db.cursor() as txn:
            self.write(m.storage.db.events.list(oid))
