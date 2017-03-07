""" bitwrap_io.api.pnml """
import os
from cyclone.web import RequestHandler
from bitwrap_io.machine import pnml
from bitwrap_io.api import headers

class ListResource(headers.Mixin, RequestHandler):
    """ list PNML """

    def get(self, *args):
        """ list schema files """
        res = [os.path.basename(xml)[:-4] for xml in pnml.schema_list()]
        self.write({'pnml': res})

class Resource(headers.Mixin, RequestHandler):
    """ view PNML """

    def get(self, name, *args):
        """ read schema xml """
        self.set_header('Content-Type', 'application/xml')
        self.write(pnml.Machine(name).net.xml)
