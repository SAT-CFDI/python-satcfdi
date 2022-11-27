import pickle
from urllib.parse import urlparse, urlunparse

import requests
import urllib3

from .utils import get_post_form, generate_token, request_ref_headers
from .. import Signer, __version__

CONSTANCIA_URL = 'https://rfcampc.siat.sat.gob.mx/PTSC/IdcSiat/IdcGeneraConstancia.jsf'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

DEFAULT_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': USER_AGENT
}


def debug_response(res):
    print('-- RESPONSE DEBUG --')
    print(res.status_code)
    for k, v in res.request.headers.items():
        print(k, v)
    print(res.request.body)
    print('results')
    print(res.text)
    print('-- RESPONSE DEBUG END --')


class SATSession:
    def __init__(self, signer: Signer):
        urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH'
        self.signer = signer
        self.session = requests.session()

    def login(self):
        LOGIN_URL = 'https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel'

        res = self.session.get(
            url=LOGIN_URL,
            headers=DEFAULT_HEADERS
        )
        assert res.status_code == 200

        action, data = get_post_form(res)
        ref_headers = request_ref_headers(res)
        res = self.session.post(
            url=action,
            headers=DEFAULT_HEADERS | ref_headers,
            data=data
        )
        assert res.status_code == 200

        action, data = get_post_form(res, id='certform')
        ref_headers = request_ref_headers(res)
        res = self.session.post(
            url=action,
            headers=DEFAULT_HEADERS | ref_headers,
            data=data | {
                'token': generate_token(self.signer, code=data['guid']),
                'fert': self.signer.certificate.get_notAfter()[2:].decode(),
            }
        )
        assert res.status_code == 200

        return res

    def home_page(self):
        return self.session.get(
            url='https://loginda.siat.sat.gob.mx/nidp/app?sid=0',
            headers=DEFAULT_HEADERS
        )

    def logout(self):
        return self.session.get(
            url='https://loginda.siat.sat.gob.mx/nidp/app/logout',
            headers=DEFAULT_HEADERS | {
                'referer': 'https://loginda.siat.sat.gob.mx/nidp/app?sid=0'
            },
            allow_redirects=False
        )

    def declaraciones_provisionales_login(self):
        res = self.session.get(
            url='https://ptscdecprov.clouda.sat.gob.mx',
            headers=DEFAULT_HEADERS,
            allow_redirects=True
        )
        assert res.status_code == 200

        action, data = get_post_form(res)
        res = self.session.post(
            url=action,
            headers=DEFAULT_HEADERS | {
                # 'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://loginda.siat.sat.gob.mx',
                'referer': 'https://loginda.siat.sat.gob.mx/',
            },
            data=data
        )
        return res

    def save_session(self, target):
        pickle.dump(self.session.cookies, target)

    def load_session(self, source):
        self.session.cookies.update(pickle.load(source))


class SATCfdiAUSession:
    def __init__(self, signer: Signer):
        urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH'
        self.signer = signer
        self.session = requests.session()

    def login(self):
        LOGIN_URL = 'https://portal.facturaelectronica.sat.gob.mx'

        res = self.session.get(
            url=LOGIN_URL,
            headers=DEFAULT_HEADERS
        )
        assert res.status_code == 200

        action, data = get_post_form(res)
        parts = urlparse(action)
        action = urlunparse((
            parts.scheme,
            parts.netloc,
            '/nidp/app/login',
            None,
            parts.query.replace('id=SATUPCFDiCon', 'id=SATx509Custom'),
            None
        ))
        ref_headers = request_ref_headers(res)
        res = self.session.post(
            url=action,
            headers=DEFAULT_HEADERS | ref_headers,
            data=data
        )
        assert res.status_code == 200

        # action, data = get_post_form(res, id='certform')
        # ref_headers = request_ref_headers(res)
        # res = self.session.post(
        #     url=action,
        #     headers=DEFAULT_HEADERS | ref_headers,
        #     data=data | {
        #         'token': generate_token(self.signer, code=data['guid']),
        #         'fert': self.signer.certificate.get_notAfter()[2:].decode(),
        #     }
        # )
        # assert res.status_code == 200

        return res

    def validate_rfc(self, rfc, razon_social):
        res = self.session.post(
            url='https://portal.facturaelectronica.sat.gob.mx/Clientes/ValidaRazonSocialRFC',
            headers=DEFAULT_HEADERS | {
                'origin': 'https://portal.facturaelectronica.sat.gob.mx',
                'authority': 'https://portal.facturaelectronica.sat.gob.mx',
            },
            data={
                'rfcValidar': rfc.upper(),
                'razonSocial': razon_social.upper(),
            }
        )
        assert res.status_code == 200
        return res

    def save_session(self, target):
        pickle.dump(self.session.cookies, target)

    def load_session(self, source):
        self.session.cookies.update(pickle.load(source))
