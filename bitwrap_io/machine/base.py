"""
bitwrap_io.machine.base - state machine mixin
"""

class Machine(object):
    """ Use a network as a state machine """

    @staticmethod
    def vadd(vector1, vector2):
        """ add 2 vectors """
        return [(vector1[i] + vector2[i]) for i in range(len(vector1))]

    @staticmethod
    def is_valid(vector):
        """ assert input vector has no negative scalar values """

        for i in vector:
            if i < 0:
                return False

        return True

class PTNet(object):
    """ p/t net """

    def __init__(self):
        self.places = None
        self.transitions = None

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
