"""
bitwrap_pnml
"""

import os
import sys
from bitwrap_pnml.state_machine import StateMachine

MACHINES = {}

def get(schema):
    """ get machine """
    if schema not in MACHINES:
        MACHINES[schema] = StateMachine(schema)

    return MACHINES[schema]
