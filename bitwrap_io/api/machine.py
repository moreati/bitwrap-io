"""

"""
import os
from cyclone.web import RequestHandler
from bitwrap_io.api import headers
import bitwrap_io

class ListResource(headers.Mixin, RequestHandler):
    """
    List schemata
    """

    def get(self):
        """ list machines that are loaded into memory """
        self.write({'machines': bitwrap_io.MACHINES.keys()})

class Resource(headers.Mixin, RequestHandler):
    """
    Return state machine json
    """

    def get(self, name):
        """ return state machine definition as json """

        sm = bitwrap_io.get(name).machine

        self.write({
            'machine': {
                'name': name,
                'places': sm.net.places,
                'transitions': sm.net.transitions
            }
        })
