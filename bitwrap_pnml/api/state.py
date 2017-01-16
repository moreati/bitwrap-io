"""
return statevectors
"""
from cyclone.web import RequestHandler
from bitwrap_pnml.storage import Storage
import bitwrap_pnml


class Resource(RequestHandler):
    """ index """

    def get(self, schema, oid):
        """ report api version """

        try:
            bitwrap_pnml.get(schema)
            key = Storage.encode_key(oid)
            stor = Storage.encode_key(schema)
            res = Storage.open(stor).fetch_str(key)
            self.set_header('Content-Type', 'application/json')

            if res:
                self.write(res)
                return
        except:
            pass

        self.write('')
        self.set_status(404)
