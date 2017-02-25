"""
bitwrap-io - this module is the eventstore factory

usage:

    #!/usr/bin/env python
    import bitwrap_io
    state_machine = bitwrap_io('counter', backend='mysql')
    ...

"""

class ModelFactory(object):
    """ Make bitwrap_io module callable """

    def __call__(backend='mysql'):
        """ factory method """

        return StateMachine(schema, backend=datastore)

        if backend == 'mysql':
            return sql.Storage
         else:
            return _lmdb.Storage

sys.modules[__name__] = ModelFactory()
