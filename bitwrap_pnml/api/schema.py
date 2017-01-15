"""

"""
from cyclone.web import RequestHandler
import bitwrap_pnml

MACHINE = bitwrap_pnml.get('metaschema')

class ListResource(RequestHandler):
    """
    List PNML
    """

    def get(schema_name):
        """ list schema as xml """
        pass

class Resource(RequestHandler):
    """
    REST for PNML
    """

    def get(self, name):
        """ read schema xml """
        self.set_header('Content-Type', 'application/xml')
        self.write(bitwrap_pnml.get(name).machine.net.xml)

    def post(self, request):
        """ update schema xml """
        # TODO: add event for schema modification
        # and overwrite the xml file in filesystem
        pass
