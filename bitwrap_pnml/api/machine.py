"""

"""
import os
from cyclone.web import RequestHandler
import bitwrap_pnml

class ListResource(RequestHandler):
    """
    List schemata
    """

    def get(self):
        """ list machines as json """
        self.write({ 'machines': bitwrap_pnml.MACHINES.keys() })

class Resource(RequestHandler):
    """
    Return state machine json
    """

    def get(self, name):
        """ return state machine definition as json """
        self.write( bitwrap_pnml.get(name).machine.machine )
