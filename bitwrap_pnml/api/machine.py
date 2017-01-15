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

        sm = bitwrap_pnml.get(name).machine
        m = sm.machine

        self.write({
            'machine': {
                'schema': name,
                'state': sm.machine['state'],
                'places': sm.net.places,
                'transitions': m['transitions']
            }
        })
