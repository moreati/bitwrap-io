"""
bitwrap_lambda
"""

import os
import sys
from bitwrap_lambda.state_machine import StateMachine
import bitwrap_lambda.machine


def get(schema):
    """ load state_machine object by schema name """
    return StateMachine(schema)

def put(schema, json_data):
    """ upload pnml """
    bitwrap_lambda.machine.write_schema(schema, json_data)

def rm(schema):
    """ remove pnml """
    bitwrap_lambda.machine.rm_schema(schema)
