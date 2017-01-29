"""
return statevectors
"""
from cyclone.web import RequestHandler
from bitwrap_pnml.storage import Storage
from bitwrap_pnml.api import headers
import bitwrap_pnml
import ujson as json


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

class ListResource(headers.Mixin, RequestHandler):
    """ index """

    @staticmethod
    def _get_recurse(storage, eventid, events=[]):
        key = Storage.encode_key(eventid)
        evt = storage.fetch(key, db_key='events')
        evt['id'] = eventid

        events.append(evt)

        if evt['previous']:
          return ListResource._get_recurse(storage, evt['previous'], events=events)
        else:
          return events

    def get(self, schema, oid):
        """ return event json """

        try:
            bitwrap_pnml.get(schema)
            key = Storage.encode_key(oid)
            stor = Storage.encode_key(schema)
            storage = Storage.open(stor)
            head_event = storage.fetch_str(key, db_name='transactions')

            _list = self._get_recurse(storage, head_event)
            
            if head_event:
                return self.write({
                    'events': _list,
                    'oid': oid,
                    'head': head_event
                })
        except:
            pass

        self.write({ 'events': [] })
        self.set_status(404)
