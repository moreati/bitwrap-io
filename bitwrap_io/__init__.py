"""
bitwrap_io

load bitwrap machines with attached storage
"""

import os
import sys
from bitwrap_io.state_machine import StateMachine
from twisted.internet.protocol import Factory
Factory.noisy = False

SCHEMA_PATH = os.environ.get(
    'BITWRAP_SCHEMA_PATH',
    os.path.join(os.path.dirname(__file__), 'test/machine/')
)

MACHINES = {}

def get(schema):
    """ get machine """
    if schema not in MACHINES:
        MACHINES[schema] = StateMachine(schema)

    return MACHINES[schema]
