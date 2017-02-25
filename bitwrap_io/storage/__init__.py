"""
bitwrap_io.storage 
"""

from bitwrap_io.storage import sql, _lmdb

def factory(backend='lmdb'):
    """
    storage interface for either lmdb or mysql backend
    """

    if backend == 'mysql':
        return sql.Storage
    elif backend == 'lmdb':
        return _lmdb.Storage
