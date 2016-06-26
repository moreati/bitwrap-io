import os
import sys
import logging
import bitwrap
import twisted
from twisted.python.failure import Failure
from crochet import wait_for, run_in_reactor, setup

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
log = logging.getLogger(__package__)

machines = {}

# FIXME make this configable via env var
_schema_path = os.path.join(os.path.dirname(__file__), '../tests/machine/')

def start():
    """ start twisted reactor """
    observer = twisted.python.log.PythonLoggingObserver(__package__)
    observer.start()
    setup()

def get(schema):
    """ get machine """
    return bitwrap.open_json(schema, os.path.join(_schema_path, schema + '.json'))
