"""

"""
import os
from cyclone.web import RequestHandler
import bitwrap_pnml
import bitwrap_pnml.machine
from bitwrap_pnml.api import headers

class ListResource(headers.Mixin, RequestHandler):
    """
    List PNML
    """

    def get(self):
        """ list schema files """
        _list = [ os.path.basename(xml)[:-4] for xml in bitwrap_pnml.machine.schema_list()]
        self.write({'pnml': _list})

class Resource(headers.Mixin, RequestHandler):
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
