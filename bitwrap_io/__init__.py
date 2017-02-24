"""
bitwrap_io
"""

import os
import sys
from bitwrap_io.state_machine import StateMachine
import bitwrap_io.machine

def get(schema):
    """ load by schema name """
    return StateMachine(schema)

def put(schema, json_data):
    """ upload json """
    bitwrap_io.machine.write_schema(schema, json_data)

def rm(schema):
    """ remove json """
    bitwrap_io.machine.rm_schema(schema)
