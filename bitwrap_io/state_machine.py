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

    def __init__(self, schema, backend=None, syntax=None):
        self.schema = schema.__str__()
        self.machine = MachineFactory(syntax=syntax)(self.schema)
        self.storage = StorageFactory(backend=backend)(self.schema, self.machine)

    def __call__(self, **request):
        """ execute a transformation """
        return self.session(request).commit()

    def session(self, request):
        """ start a session """
        request['schema'] = self.schema
        return Transaction( request, schema=self.schema, machine=self.machine, storage=self.storage)

    def preview(self, **request):
        """ simulate a transformation """
        return self.session(request).commit(dry_run=True)

class Transaction(object):
    """ state machine transaction """

    def __init__(self, request, schema=None, machine=None, storage=None):
        self.schema = schema
        self.request = request
        self.machine = machine
        self.storage = storage
        self.dry_run = None
        self.response = None

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
