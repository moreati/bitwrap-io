import os
import sys
from bitwrap_io.state_machine import StateMachine
from twisted.internet.protocol import Factory
Factory.noisy = False

redis_host = os.environ.get('REDIS_PORT_6379_TCP_ADDR', '127.0.0.1')
redis_port = int(os.environ.get('REDIS_PORT_6379_TCP_PORT', 6379))

schema_path = os.environ.get(
    'BITWRAP_SCHEMA_PATH',
    os.path.join(os.path.dirname(__file__), 'test/machine/')
)

machines = {}

def get(schema):
    """ get machine """
    if schema in machines:
        m = machines[schema]
    else:
        m = StateMachine(schema)
        machines[schema] = m

    return m
