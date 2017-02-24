"""
bitwrap_io machine

build a state machine model from Petri-net markup language
"""

from bitwrap_io.machine import pnml, _json

def factory(syntax='json'):
    if syntax == 'json':
        return _json.Machine
    else:
        return pnml.Machine
