"""
return statevectors
"""
from cyclone.web import RequestHandler
import bitwrap_io.storage
from bitwrap_io.api import headers
import bitwrap_io
import ujson as json

Storage = bitwrap_io.storage.factory(backend='mysql')


class Resource(headers.Mixin, RequestHandler):
    """ index """

    def get(self, schema, eventid):
        """ return event json """

        try:
            bitwrap_io.get(schema)
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
            bitwrap_io.get(schema)
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
    def _get_list(storage, eventid):
        events=[]

        def _get_event(eventid):
            key = Storage.encode_key(eventid)
            evt = storage.fetch(key, db_key='events')
            if evt is None:
                return None
            else:
                evt['id'] = eventid
                return evt

        evt = _get_event(eventid)

        if not evt:
            return events

        if not evt['previous'] and len(events) == 0:
          events.append(evt)
          return events

        while evt['previous']:
            events.append(evt)
            evt = _get_event(evt['previous'])

        events.append(evt)

        return events

    def get(self, schema, oid):
        """ return event json """

        assert bitwrap_io.get(schema)
        key = Storage.encode_key(oid)
        stor = Storage.encode_key(schema)
        storage = Storage.open(stor)

        head_event = storage.fetch_str(key, db_name='transactions')

        if head_event:

            self.write({
                'events': self._get_list(storage, head_event),
                'oid': oid,
                'head': head_event
            })

        else:
            self.write({ 'events': [] })
            self.set_status(404)
