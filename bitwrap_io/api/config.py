"""
bitwrap_io.api.config - font end stats and config
"""

import os
from cyclone.web import RequestHandler
from bitwrap_io.api import headers
import bitwrap_io.storage._lmdb
import rds_config
import xxhash

def settings():
    """ build settings hash from env vars """

    return {
        #github_client_id=os.environ.get('GITHUB_CLIENT_ID'),
        #github_secret=os.environ.get('GITHUB_SECRET'),
        # TODO: add github auth
        #login_url="/auth/login",
        #xsrf_cookies=True, # REVIEW: is this usable w/ rpc ?
        'cookie_secret': os.environ.get('COOKIE_SECRET', ''),
        'template_path': os.path.join(os.path.dirname(__file__), '../templates'),
        'debug': True
    }

def _hash(txt):
    return xxhash.xxh64(txt, seed=bitwrap_io.storage._lmdb.XX_SEED).hexdigest()


class Resource(headers.Mixin, RequestHandler):
    """ config """

    def get(self, stage):
        """ direct web app to api """

        self.write({
            'endpoint': "http://127.0.0.1:8080",
            'stage': stage,
            'ENV': {
                'LMDB_MAP_SIZE': bitwrap_io.storage._lmdb.MAP_SIZE,
                'LMDB_PATH': bitwrap_io.storage._lmdb.REPO_ROOT,
                'SQL_DB': rds_config.db_name,
                'SQL_HOST': _hash(rds_config.rds_host)
            }
        })

