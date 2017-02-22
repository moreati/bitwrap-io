"""

"""
import os
from cyclone.web import RequestHandler
from bitwrap_pnml.api import headers
import bitwrap_pnml

class ListResource(headers.Mixin, RequestHandler):
    """
    List schemata
    """

    def get(self):
        """ list machines that are loaded into memory """
        self.write({'machines': bitwrap_pnml.MACHINES.keys()})

class Resource(headers.Mixin, RequestHandler):
    """
    Return state machine json
    """

    def get(self, name):
        """ return state machine definition as json """

        sm = bitwrap_pnml.get(name).machine

        self.write({
            'machine': {
                'name': name,
                'places': sm.net.places,
                'transitions': sm.net.transitions
            }
        })
