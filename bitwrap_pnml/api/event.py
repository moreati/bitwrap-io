"""
return statevectors
"""
from cyclone.web import RequestHandler
from bitwrap_pnml.storage import Storage
from bitwrap_pnml.api import headers
import bitwrap_pnml


class Resource(headers.Mixin, RequestHandler):
    """ index """

    def get(self, schema, eventid):
        """ return event json """

        try:
            bitwrap_pnml.get(schema)
            key = Storage.encode_key(eventid)
            stor = Storage.encode_key(schema)
            res = Storage.open(stor).fetch_str(key, db_name='events')
            
            if res:
                self.write('{ "event": ' + res + ', "id": "' + eventid +'" }')
                return
        except:
            pass

        self.write({ 'event': None })
        self.set_status(404)

class HeadResource(headers.Mixin, RequestHandler):
    """ index """

    def get(self, schema, oid):
        """ return event json """

        try:
            bitwrap_pnml.get(schema)
            key = Storage.encode_key(oid)
            stor = Storage.encode_key(schema)
            storage = Storage.open(stor)
            head_event = storage.fetch_str(key, db_name='transactions')

            res = storage.fetch_str(head_event, db_name='events')
            
            if res:
                self.write('{ "event": ' + res + ', "id": "' + head_event +'" }')
                return
        except:
            pass

        self.write({ 'event': None })
        self.set_status(404)
