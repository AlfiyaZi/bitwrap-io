"""
bitwrap_io.api.config - font end stats and config
"""

import os
from cyclone.web import RequestHandler
from bitwrap_io.api import headers
from bitwrap_io.storage import rds_config
import bitwrap_io.storage._lmdb as _lmdb

def settings():
    """ build settings hash from env vars """

    return {
        #github_client_id=os.environ.get('GITHUB_CLIENT_ID'),
        #github_secret=os.environ.get('GITHUB_SECRET'),
        #login_url="/auth/login",
        #xsrf_cookies=True, # REVIEW: is this usable w/ rpc ?
        'cookie_secret': os.environ.get('COOKIE_SECRET', ''),
        'template_path': os.path.join(os.path.dirname(__file__), '../templates'),
        'debug': True
    }


class Resource(headers.Mixin, RequestHandler):
    """ config """

    def get(self, stage, *args):
        """ direct web app to api """

        _db_files = [os.path.basename(f) for f in _lmdb.Storage.db_files()]

        self.write({
            'endpoint': os.environ.get('ENDPOINT', 'http://127.0.0.1:8080'),
            'wrapserver': os.environ.get('WRAPSERVER', 'http://127.0.0.1:8001'),
            'stage': stage,
            'ENV': {
                'LMDB_MAP_SIZE': _lmdb.MAP_SIZE,
                'SQL_DB': rds_config.db_name,
                'SQL_HOST': _lmdb.Storage.hexdigest(rds_config.rds_host),
                'LMDB_DB': _db_files
            }
        })
