import os
import sys
import logging
import bitwrap
import twisted
from twisted.python.failure import Failure

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
log = logging.getLogger(__package__)

machines = {}

# FIXME make this configable via env var
_schema_path = os.path.join(os.path.dirname(__file__), '../tests/machine/')

def get(schema):
    """ get machine """
    return bitwrap.open_json(schema.__str__(), os.path.join(_schema_path, schema + '.json'))

# TODO: add transform, preview, maybe ?commit?
