"""

"""
import os
from cyclone.web import RequestHandler
import bitwrap_io
import bitwrap_io.machine
from bitwrap_io.api import headers

class ListResource(headers.Mixin, RequestHandler):
    """
    List PNML
    """

    def get(self):
        """ list schema files """
        _list = [ os.path.basename(xml)[:-4] for xml in bitwrap_io.machine.schema_list()]
        self.write({'pnml': _list})

class Resource(headers.Mixin, RequestHandler):
    """
    View for PNML
    """

    def get(self, name):
        """ read schema xml """
        try:
            self.set_header('Content-Type', 'application/xml')
            self.write(bitwrap_io.get(name).machine.net.xml)
        except:
            self.set_status(404)
