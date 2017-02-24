"""
bitwrap_io.state_machine

Combine storage and machine modules to provide a persistent state machine object
"""
from bitwrap_io.storage import Storage
from bitwrap_io.machine import factory as MachineFactory

class StateMachine(object):
    """
    State Machine object with persistent storage
    """

    def __init__(self, schema, **kwargs):
        self.schema = schema.__str__()
        self.machine = MachineFactory(**kwargs)(self.schema)

    def session(self, request):
        """ start a session """
        return Transaction(self.machine, self.schema, request)

    def transform(self, msg):
        """ execute a transformation """
        return self.session(msg).commit()

    def preview(self, msg):
        """ simulate a transformation """
        return self.session(msg).simulate()


class Transaction(object):
    """ state machine transaction """

    def __init__(self, machine, schema, request):
        self.schema = schema
        self.request = request
        self.machine = machine
        self.dry_run = None
        self.response = None

    def simulate(self):
        """ simulate transform and return cache values """
        return self.commit(dry_run=True)

    def commit(self, dry_run=False):
        """ transform and persist state to storage """
        self.dry_run = dry_run
        self.persist()
        return self.response

    def persist(self):
        """ persist to storage """

        self.response = Storage(
            self.schema,
            self.machine
        ).commit(
            self.request,
            dry_run=self.dry_run
        )
