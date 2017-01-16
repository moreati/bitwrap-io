"""
bitwrap_pnml
"""

import os
import sys
from bitwrap_pnml.state_machine import StateMachine
import bitwrap_pnml.machine


MACHINES = {}

def get(schema):
    """ load state_machine object by schema name """
    if schema not in MACHINES:
        MACHINES[schema] = StateMachine(schema)

    return MACHINES[schema]

def put(schema, xml_data):
    """ upload pnml """
    bitwrap_pnml.machine.write_schema(schema, xml_data)

def rm(schema):
    """ upload pnml """
    bitwrap_pnml.machine.rm_schema(schema)
    MACHINES.pop(schema, None)
