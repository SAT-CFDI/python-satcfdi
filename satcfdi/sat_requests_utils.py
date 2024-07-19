# Ciphers compatible with SAT Services
import ssl

import certifi
from requests.adapters import HTTPAdapter

CIPHERS = (
    'ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:ECDH+AESGCM:'
    'DH+AESGCM:ECDH+AES:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!eNULL:!MD5:!DSS'
    ':HIGH:!DH'
)

ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.set_ciphers(CIPHERS)


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = ssl_context
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = ssl_context
        return super().proxy_manager_for(*args, **kwargs)
