""" helper methods for converting petrinet arcs and transitions to vectors """

from bitwrap_pnml.machine.petrinet import Transition, Place

def append_roles(net):
    """ build roles from edge list """
    for e in net.edges:
        if e.inhibitor and ('_role' in e.source):
            role_name = e.source.replace('_role', '')

            if role_name not in net.roles:
                net.roles.append(role_name)

            e.role = role_name # set required role

def places(net):
    """ build place vector """
    places = {}
    offset = 0

    for p in net.places:
        # KLUDGE: refactor these conventions to be more explicit
        if not '_role' in p:
            if p == 'BEGIN':
                inital = 1
            else:
                inital = 0 # FIXME: use initial markings from pnml

            places[p] = {'inital': inital, 'offset': offset}
            offset += 1

    return places

def empty_vector(size):
    """ return an empty vector of given size """
    return [0] * size

def transitions(net, places):
    """ build set of transitions from network """
    transitions = {}

    for action in net.transitions:
        transitions[action] = {'delta': empty_vector(len(places)), 'role': 'default'}

    return transitions

def apply_edges(net, places, transitions):
    """ re-index edges and places """
    for edge in net.edges:
        source = edge.find_source()
        target = edge.find_target()

        if isinstance(source, Transition):
            if edge.inhibitor == True:
                raise Exception('Roles cannot be targets')
            else:
                offset = places[target.id]['offset']
                transitions[source.id]['delta'][offset] = 1

        elif isinstance(source, Place):
            if edge.inhibitor == True:
                transitions[target.id]['role'] = edge.role
            else:
                offset = places[source.id]['offset']
                transitions[target.id]['delta'][offset] = -1
        else:
            raise Exception('invalid edge %s' % edge.id)
