"""
bitwrap_io.machine
"""

from bitwrap_io.machine import pnml, _json

def factory(syntax='json'):
    """
    build a state machine model from Petri-net markup language
    """

    if syntax == 'json':
        return _json.Machine
    else:
        return pnml.Machine
