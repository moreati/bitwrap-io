"""
bitwrap_pnml machine

build a state machine model from Petri-net markup language
"""

import os
import sys
from bitwrap_pnml.machine import dsl, petrinet

PNML_PATH = os.environ.get('PNML_PATH', os.path.abspath(__file__ + '/../../../examples'))

def schema_to_file(name):
    return os.path.join(PNML_PATH, '%s.xml' % name)

def write_schema(schema, xml_str):
    with open(schema_to_file(schema), 'w') as pnml:
        pnml.write(xml_str)

def rm_schema(schema):
    try:
        os.remove(schema_to_file(schema))
    except OSError:
        pass

class PTNet(object):
    """
    Load PNML as a matrix of places and transitions
    """

    def __init__(self, name):
        self.name = name
        self.places = None
        self.transitions = None
        self.filename = schema_to_file(name)
        self.net = petrinet.parse_pnml_file(self.filename)[0]
        self.reindex()

        with open(self.filename, 'r') as pnml:
            self.xml = pnml.read()

    def reindex(self):
        """ rebuild network from pnml """
        dsl.append_roles(self.net)
        self.places = dsl.places(self.net)
        self.transitions = dsl.transitions(self.net, self.places)
        dsl.apply_edges(self.net, self.places, self.transitions)

    def empty_vector(self):
        """ return an empty state-vector """
        return dsl.empty_vector(len(self.places))

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
