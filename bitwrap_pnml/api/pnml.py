"""

"""
from cyclone.web import RequestHandler
import bitwrap_pnml

class ListResource(RequestHandler):
    """
    List PNML
    """

    def get(schema_name):
        """ list schema files """
        # FIXME 
        pass

class Resource(RequestHandler):
    """
    REST for PNML
    """

    def get(self, name):
        """ read schema xml """
        try:
            self.set_header('Content-Type', 'application/xml')
            self.write(bitwrap_pnml.get(name).machine.net.xml)
        except:
            self.set_status(404)

    def post(self, name):
        """ update schema xml """
        bitwrap_pnml.put(name, self.request.body)
