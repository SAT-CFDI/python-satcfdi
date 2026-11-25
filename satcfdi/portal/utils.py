import base64
import random
import string
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup
from requests import Response

from ..models import Signer, Certificate


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


def get_form(res: Response, **kwargs):
    html = BeautifulSoup(res.text, 'html.parser')
    form = html.find('form', **kwargs)
    if form is None:
        return None, {}

    data = {
        str(i.attrs['name']): i.attrs.get('value')
        for i in form.find_all('input')
        if 'name' in i.attrs
    }

    assert form.attrs['method'].upper() == "POST"
    return action_url(form.attrs.get('action'), res.url), data


_NON_FIELD_INPUTS = ('submit', 'button', 'image', 'reset', 'file')


def get_form_fields(res: Response, **kwargs) -> dict[str, str]:
    """
    Fields a browser would submit from the form: its inputs, except buttons and
    unchecked boxes, plus the selected option of each select.
    """
    html = BeautifulSoup(res.text, 'html.parser')
    form = html.find('form', **kwargs)
    if form is None:
        return {}

    data = {}
    for i in form.find_all('input'):
        name = i.attrs.get('name')
        kind = i.attrs.get('type', 'text').lower()
        if not name or kind in _NON_FIELD_INPUTS:
            continue
        if kind in ('checkbox', 'radio') and 'checked' not in i.attrs:
            continue
        data[str(name)] = i.attrs.get('value') or ''

    for select in form.find_all('select'):
        name = select.attrs.get('name')
        if not name:
            continue
        option = select.find('option', selected=True) or select.find('option')
        data[str(name)] = (option.attrs.get('value') or '') if option else ''

    return data


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
