"""
bitwrap_pnml machine

build a state machine model from Petri-net markup language
"""

import os
import sys
from bitwrap_pnml.machine import dsl, petrinet

PNML_PATH = os.environ.get('PNML_PATH', os.path.abspath(__file__ + '/../../../examples'))

def open_xml(network_name):
    """ parse file """
    path = os.path.join(PNML_PATH, '%s.xml' % network_name)
    return petrinet.parse_pnml_file(path)[0]

class Network(object):
    """
    Load PNML as a matrix of places and transitions
    """

    def __init__(self, name):
        self.name = name
        self.net = open_xml(name)
        self.reindex()

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

        for key in self.places:
            place = self.places[key]
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
        self.machine = Network(network_name).open(init_state)

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

    def transform(self, action):
        """ update self.vector """
        vsum = self.vadd(self.machine['state'], self.machine['transitions'][action]['delta'])

        if self.is_valid(vsum):
            self.machine['state'] = vsum
            return True
        else:
            return False
