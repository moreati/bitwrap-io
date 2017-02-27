"""
json - load bitwrap machines from json files
"""

import os
import glob
import json
from bitwrap_io.machine import base

JSON_PATH = os.environ.get('JSON_PATH', os.path.abspath(__file__ + '/../../schemata'))

def schema_to_file(name):
    """ build schema filename from name """
    return os.path.join(JSON_PATH, '%s.json' % name)

def schema_list():
    """ list schema files """
    return glob.glob(JSON_PATH + '/*.json')

class Machine(base.Machine):
    """ state machine """

    def __init__(self, name, init_state=None):
        self.net = PTNet(name)
        self.machine = self.net.open(init_state)

class PTNet(base.PTNet):
    """ p/t net """

    def __init__(self, name):
        self.name = name
        self.filename = schema_to_file(name)

        with open(self.filename, 'r') as schema_file:
            self.data = json.load(schema_file)
            assert self.data['machine']['name'] == self.name
            self.places = self.data['machine']['places']
            self.transitions = self.data['machine']['transitions']

