"""
bitwrap_io 

usage:

    In [1]: import bitwrap_io
    
    In [2]: m = bitwrap_io.open('counter')
    
    In [3]: m
    Out[3]: <bitwrap_io.state_machine.StateMachine at 0x7f30da88b710>
    
    In [4]: m(oid='foo', action='INC')
    Out[4]:
            {'event': {'action': 'INC',
              'endpoint': None,
              'error': 0,
              'oid': 'foo',
              'payload': {},
              'previous': None,
              'state': [1]},
             'id': '01a49f6d2ccc4f52'}

"""
import sys
from bitwrap_io.state_machine import StateMachine

MACHINES = {}

def factory(schema, backend='lmdb', syntax='json'):
    """ bitwrap_io module callable """

    if not schema in MACHINES:
        MACHINES[schema] = StateMachine(schema, backend=backend, syntax=syntax)

    return MACHINES[schema]

open = factory
