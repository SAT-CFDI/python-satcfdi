import base64
import random
import string
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util import create_urllib3_context

from ..models import Signer, Certificate


# Ciphers compatible with SAT Services
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



def generate_token(signer: Signer, code: str) -> bytes:
    rfc = signer.rfc
    num_serie = signer.certificate_number

    co = code + "|" + rfc + "|" + num_serie

    signature = signer.sign_sha1(data=co.encode())

    return base64.b64encode(
        base64.b64encode(co.encode()) + b"#" + base64.b64encode(signature.encode())
    )


def verify_token(certificate: Certificate, token: bytes) -> str:
    decoded_token = base64.b64decode(token)
    code, signature = decoded_token.split(b"#", maxsplit=2)

    code = base64.b64decode(code)
    signature = base64.b64decode(signature)

    assert certificate.verify_sha1(
        data=code,
        signature=base64.b64decode(signature)
    )

    code, rfc, num_serie = code.decode().split("|", maxsplit=3)

    assert rfc == certificate.rfc
    assert num_serie == certificate.certificate_number

    return code


def action_url(action: str | None, url: str):
    if not action:
        return url

    if action.startswith('/'):
        parts = urlparse(url)
        return urlunparse((parts.scheme, parts.netloc, action, None, None, None))

    return action


def get_form(res: Response, id=None):
    html = BeautifulSoup(res.text, 'html.parser')
    if id:
        form = html.find(id=id)
    else:
        form = html.select('form')[0]

    data = {
        i.attrs['name']: i.attrs.get('value')
        for i in form.findChildren('input')
        if 'name' in i.attrs
    }

    assert form.attrs['method'].upper() == "POST"
    return action_url(form.attrs.get('action'), res.url), data


def request_ref_headers(url):
    parts = urlparse(url)
    return {
        'origin': urlunparse((parts.scheme, parts.netloc, '', '', '', '')),
        'referer': url
    }


def request_verification_token(res: Response):
    html = BeautifulSoup(res.text, 'html.parser')
    return html.find(name='input', attrs={'name': '__RequestVerificationToken'}).attrs['value']


def random_ajax_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
