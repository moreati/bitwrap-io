"""
bitwrap_io.machine
"""

from bitwrap_io.machine import pnml, _json

def factory(syntax=None):
    """
    build a state machine model from Petri-net markup language
    """

    if syntax == 'pnml':
        return pnml.Machine
    else:
        return _json.Machine
