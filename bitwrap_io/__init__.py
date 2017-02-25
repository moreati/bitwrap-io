"""
bitwrap_io 

usage:

    #!/usr/bin/env python
    import bitwrap_io
    state_machine = bitwrap_io.open('counter', backend='mysql')
    ...

"""
import sys
from bitwrap_io.state_machine import StateMachine

def factory(schema, **kwargs):
    """ bitwrap_io module callable """

    return StateMachine(schema, **kwargs)

open = factory
