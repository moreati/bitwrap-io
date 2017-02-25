"""
bitwrap_io.state_machine

Storage and Machine modules are combined to provide a persistent state machine.
StateMachine Schemata are expressed in Petri-Net Markup Language (xml) or using Bitwrap's internal DSL (json).
"""
from bitwrap_io.storage import factory as StorageFactory
from bitwrap_io.machine import factory as MachineFactory

class StateMachine(object):
    """
    State Machine object with persistent storage
    """

    def __init__(self, schema, **kwargs):
        self.schema = schema.__str__()
        self.machine = MachineFactory(**kwargs)(self.schema)
        self.storage = StorageFactory(**kwargs)

    def session(self, request):
        """ start a session """
        return Transaction(
            request,
            machine=self.machine,
            schema=self.schema,
            StorageProvider=self.storage
        )

    def transform(self, msg):
        """ execute a transformation """
        return self.session(msg).commit()

    def preview(self, msg):
        """ simulate a transformation """
        return self.session(msg).simulate()


class Transaction(object):
    """ state machine transaction """

    def __init__(self, request, schema=None, machine=None, StorageProvider=None):
        self.schema = schema
        self.request = request
        self.machine = machine
        self.dry_run = None
        self.response = None
        self.storage = StorageProvider(self.schema, self.machine)

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

        self.response = self.storage.commit(
            self.request,
            dry_run=self.dry_run
        )
