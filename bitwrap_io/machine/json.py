"""
build a state machine model from Petri-net markup language
"""

import os
import sys
import glob
import json
import bitwrap_io.machine

JSON_PATH = os.environ.get('JSON_PATH', os.path.abspath(__file__ + '/../schemata'))

def schema_to_file(name):
    """ build schema filename from name """
    return os.path.join(JSON_PATH, '%s.json' % name)

def write_schema(schema, json_str):
    """ write pnml to filesystem """
    with open(schema_to_file(schema), 'w') as pnml:
        pnml.write(json_str)

def rm_schema(schema):
    """ remove pnml from filesystem """
    try:
        os.remove(schema_to_file(schema))
    except OSError:
        pass

def schema_list():
    return glob.glob(JSON_PATH + '/*.json')

class PTNet(object):
    """
    Load bitwrap machine
    """

    def __init__(self, name):
        self.name = name
        self.filename = schema_to_file(name)

        with open(self.filename, 'r') as schema_file:
            self.data = json.load(schema_file)
            assert self.data['machine']['name'] == self.name
            self.places = self.data['machine']['places']
            self.transitions = self.data['machine']['transitions']


    def empty_vector(self):
        """ return an empty state-vector """
        return [0] * len(self.places)

    def inital_vector(self):
        """ return inital state-vector """
        vector = self.empty_vector()

        for _, place in self.places.items():
            vector[place['offset']] = place['inital']

        return vector

    def open(self, state_vector=None):
        """ open p/t-net """
        if state_vector is None:
            state_vector = self.inital_vector()

        return {'state': state_vector, 'transitions': self.transitions}

class Machine(object):
    """ Use a network as a state machine """

    def __init__(self, network_name, init_state=None):
        self.network_name = network_name
        self.net = PTNet(network_name)
        self.machine = self.net.open(init_state)

    @staticmethod
    def vadd(vector1, vector2):
        """ add 2 vectors """
        return [(vector1[i] + vector2[i]) for i in range(len(vector1))]

    @staticmethod
    def is_valid(vector):
        """
        assert input vector has no negative scalar values
        """
        for i in vector:
            if i < 0:
                return False

        return True


    def valid_actions(self):
        """ update self.vector """
        result = []

        for action, txn in self.machine['transitions'].items():
            if self.is_valid(self.vadd(self.machine['state'], txn['delta'])):
                result.append(action)

        return result
