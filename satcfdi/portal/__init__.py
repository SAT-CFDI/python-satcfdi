import json
import pickle
from time import time

import requests
import urllib3

from .utils import get_post_form, generate_token, request_ref_headers, request_verification_token, random_ajax_id
from .. import Signer, ResponseError

CONSTANCIA_URL = 'https://rfcampc.siat.sat.gob.mx/PTSC/IdcSiat/IdcGeneraConstancia.jsf'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': USER_AGENT
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


class PortalManager(requests.Session):
    def save_session(self, target):
        pickle.dump(self.cookies, target)

    def load_session(self, source):
        self.cookies.update(pickle.load(source))

    def form_request(self, action, referer_url, data):
        ref_headers = request_ref_headers(referer_url)
        res = self.post(
            url=action,
            headers=DEFAULT_HEADERS | ref_headers,
            data=data
        )
        assert res.status_code == 200
        return res


class SATPortal(PortalManager):
    def __init__(self, signer: Signer):
        super().__init__()
        urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH'
        self.signer = signer

    def login(self):
        LOGIN_URL = 'https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel'

        res = self.get(
            url=LOGIN_URL,
            headers=DEFAULT_HEADERS
        )
        assert res.status_code == 200

        action, data = get_post_form(res)
        res = self.form_request(action, res.request.url, data)

        action, data = get_post_form(res, id='certform')
        res = self.form_request(
            action,
            res.request.url,
            data | {
                'token': generate_token(self.signer, code=data['guid']),
                'fert': self.signer.certificate.get_notAfter()[2:].decode(),
            }
        )
        return res

    def home_page(self):
        return self.get(
            url='https://loginda.siat.sat.gob.mx/nidp/app?sid=0',
            headers=DEFAULT_HEADERS
        )

    def logout(self):
        return self.get(
            url='https://loginda.siat.sat.gob.mx/nidp/app/logout',
            headers=DEFAULT_HEADERS | {
                'referer': 'https://loginda.siat.sat.gob.mx/nidp/app?sid=0'
            },
            allow_redirects=False
        )

    def declaraciones_provisionales_login(self):
        res = self.get(
            url='https://ptscdecprov.clouda.sat.gob.mx',
            headers=DEFAULT_HEADERS,
            allow_redirects=True
        )
        assert res.status_code == 200

        action, data = get_post_form(res)
        res = self.form_request(action, res.request.url, data)
        return res


class SATFacturaElectronica(PortalManager):
    BASE_URL = 'https://portal.facturaelectronica.sat.gob.mx'
    REQUEST_CONTEXT = 'appId=cid-v1:20ff76f4-0bca-495f-b7fd-09ca520e39f7'

    def __init__(self, signer: Signer):
        super().__init__()
        urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH'
        self.signer = signer
        self._ajax_id = random_ajax_id()
        self._request_verification_token = None

    def login(self):
        res = self.get(
            url=self.BASE_URL,
            headers=DEFAULT_HEADERS
        )
        assert res.status_code == 200

        action, data = get_post_form(res)
        if action.startswith('https://cfdiau.sat.gob.mx/'):
            assert 'nidp/wsfed/ep?id=SATUPCFDiCon' in action
            action = action.replace('nidp/wsfed/ep?id=SATUPCFDiCon', 'nidp/app/login?id=SATx509Custom')
            res = self.form_request(action, res.request.url, data)

            action, data = get_post_form(res, id='certform')
            res = self.form_request(
                action,
                res.request.url,
                data | {
                    'token': generate_token(self.signer, code=data['guid']),
                    'fert': self.signer.certificate.get_notAfter()[2:].decode(),
                }
            )

            action, data = get_post_form(res)
            res = self.form_request(action, res.request.url, data)

            action, data = get_post_form(res)

        res = self.form_request(action, res.request.url, data)

        self._request_verification_token = request_verification_token(res)
        self._ajax_id = random_ajax_id()
        return res

    def _reload_verification_token(self):
        res = self.get(
            url=f'{self.BASE_URL}/Factura/GeneraFactura',
            headers=DEFAULT_HEADERS,
            allow_redirects=False
        )
        if res.status_code == 200:
            self._request_verification_token = request_verification_token(res)
        else:
            raise ValueError('Please Login Again')

    def reactivate_session(self):
        res = self.post(
            url=f'{self.BASE_URL}/Home/ReActiveSession',
            headers=DEFAULT_HEADERS | {
                'Origin': f'{self.BASE_URL}',
                'Request-Context': self.REQUEST_CONTEXT,
                'Request-Id': f'|{self._ajax_id}.{random_ajax_id()}'
            },
            allow_redirects=False
        )
        return res

    def _request(self, method, path, data=None, params=None):
        if self._request_verification_token is None:
            self._reload_verification_token()

        if method.upper() == 'POST':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        else:
            headers = {}

        res = self.request(
            method=method,
            url=f'{self.BASE_URL}/{path}',
            headers=DEFAULT_HEADERS | headers | {
                'Origin': self.BASE_URL,
                'Authority': self.BASE_URL,
                'Request-Context': self.REQUEST_CONTEXT,
                '__RequestVerificationToken': self._request_verification_token,
                'Request-Id': f'|{self._ajax_id}.{random_ajax_id()}'  # |pR4Px.o0yAS
            },
            data=data,
            params=params,
            allow_redirects=False
        )
        if res.status_code == 200:
            return res.json()
        else:
            raise ResponseError(res)

    def validate_legal_name(self, rfc, legal_name):
        res = self._request(
            method='POST',
            path='Clientes/ValidaRazonSocialRFC',
            data={
                'rfcValidar': rfc.upper(),
                'razonSocial': legal_name.upper(),
            })
        return res

    def exists_rfc(self, rfc):
        res = self._request(
            method='POST',
            path='Clientes/ExisteLrfc',
            data={
                'rfcValidar': rfc.upper()
            }
        )
        return res

    def validate_lco(self, rfc, apply_border_region=True):
        res = self._request(
            method='GET',
            path='Clientes/ValidaLco',
            params={
                'rfcValidar': rfc.upper(),
                'aplicaRegionFronteriza': apply_border_region,
                "_": int(time() * 1000)
            }
        )
        return json.loads(res)

# https://sc1-fi-pro-net-busqueda-avanzada-v3.azurewebsites.net/api/catalogos/tipos
# https://sc1-fi-pro-net-busqueda-avanzada-v3.azurewebsites.net/api/unidades/tipo
