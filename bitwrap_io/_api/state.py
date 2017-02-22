"""
return statevectors
"""
from cyclone.web import RequestHandler
from bitwrap_pnml.storage import Storage
from bitwrap_pnml.api import headers
import bitwrap_pnml


class Resource(headers.Mixin, RequestHandler):
    """ index """

    def get(self, schema, oid):
        """ report api version """

        try:
            bitwrap_pnml.get(schema)
            key = Storage.encode_key(oid)
            stor = Storage.encode_key(schema)
            storage = Storage.open(stor)
            res = storage.fetch_str(key)
            head = storage.fetch_str(key, db_name='transactions')

            if res:
                self.write('{ "state": { "vector":' + res + ', "head": "' + head + '" } }')
                return
        except:
            pass

        self.write('')
        self.set_status(404)
