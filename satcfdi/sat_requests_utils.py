# Ciphers compatible with SAT Services
from requests.adapters import HTTPAdapter
from urllib3.util import create_urllib3_context

CIPHERS = (
    'ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:ECDH+AESGCM:'
    'DH+AESGCM:ECDH+AES:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!eNULL:!MD5:!DSS'
    ':HIGH:!DH'
)


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = create_urllib3_context(ciphers=CIPHERS)
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = create_urllib3_context(ciphers=CIPHERS)
        return super().proxy_manager_for(*args, **kwargs)
