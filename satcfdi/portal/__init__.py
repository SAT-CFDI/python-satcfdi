import pickle
import requests
import urllib3

from .utils import get_post_form, generate_token
from .. import Signer, __version__

CONSTANCIA_URL = 'https://rfcampc.siat.sat.gob.mx/PTSC/IdcSiat/IdcGeneraConstancia.jsf'
USER_AGENT = __version__.__user_agent__

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
        LOGIN_URL_ORIGIN = 'https://loginda.siat.sat.gob.mx'

        res = self.session.get(
            url=LOGIN_URL,
            headers=DEFAULT_HEADERS
        )
        assert res.status_code == 200

        action, data = get_post_form(res)
        res = self.session.post(
            url=action,
            headers=DEFAULT_HEADERS | {
                'origin': LOGIN_URL_ORIGIN,
                'referer': LOGIN_URL,
            },
            data=data
        )
        assert res.status_code == 200

        action, data = get_post_form(res, id='certform')
        res = self.session.post(
            url=action,
            headers=DEFAULT_HEADERS | {
                'origin': LOGIN_URL_ORIGIN,
                'referer': LOGIN_URL,
            },
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
            url='https://ptscdecprov.clouda.sat.gob.mx/',
            headers=DEFAULT_HEADERS,
            allow_redirects=True
        )
        assert res.status_code == 200

        action, data = get_post_form(res)
        res = self.session.post(
            url=action,
            headers=DEFAULT_HEADERS | {
                'content-type': 'application/x-www-form-urlencoded',
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
