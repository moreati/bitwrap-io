"""
pnml - load xml definitions and convert to bitwrap machines
"""
import os
import glob
from bitwrap_io.machine import _xml as petrinet
from bitwrap_io.machine import base, dsl

PNML_PATH = os.environ.get('PNML_PATH', os.path.abspath(__file__ + '/../../pnml'))

def schema_to_file(name):
    """ build schema filename from name """
    return os.path.join(PNML_PATH, '%s.xml' % name)

def schema_list():
    """ list schema files """
    return glob.glob(PNML_PATH + '/*.xml')

class Machine(base.Machine):
    """ Use a network as a state machine """

    def __init__(self, name, init_state=None):
        self.net = PTNet(name)
        self.machine = self.net.open(init_state)

class PTNet(base.PTNet):
    """ p/t net """

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
        """ rebuild net """

        dsl.append_roles(self.net)
        self.places = dsl.places(self.net)
        self.transitions = dsl.transitions(self.net, self.places)
        dsl.apply_edges(self.net, self.places, self.transitions)
