"""
bitwrap_io.storage 
"""

import os
from bitwrap_io.storage import sql, _lmdb


def factory(backend=None):
    """
    storage interface for either lmdb or mysql backend
    """
    if backend is None:
        backend = os.environ.get('BITWRAP_DATASTORE', 'lmdb')

    if backend == 'mysql':
        return sql.Storage
    elif backend == 'lmdb':
        return _lmdb.Storage

    raise Exception('invalid backend')
