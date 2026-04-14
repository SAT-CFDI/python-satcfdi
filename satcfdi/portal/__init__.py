import re

import uuid

import base64

import json
import pickle
from time import time

import requests
from requests.structures import CaseInsensitiveDict

from .utils import get_form, generate_token, request_ref_headers, request_verification_token, random_ajax_id
from ..exceptions import ResponseError
from ..models import Signer
from ..sat_requests_utils import SSLAdapter


class PortalManager(requests.Session):
    def __init__(self, signer: Signer):
        super().__init__()
        self.mount('https://', SSLAdapter())
        self.signer = signer

        self.headers = CaseInsensitiveDict(
            {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
                "Accept-Encoding": 'gzip, deflate, br',
                "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                "Connection": "keep-alive",
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
            }
        )

    def save_session(self, target):
        pickle.dump(self.cookies, target)

    def load_session(self, source):
        self.cookies.update(pickle.load(source))

    def form(self, action, referer_url, data):
        res = self.post(
            url=action,
            headers=request_ref_headers(referer_url),
            data=data,
            allow_redirects=True
        )
        assert res.status_code == 200
        return res

    def fiel_login(self, login_response):
        action, data = get_form(login_response, id='certform')
        return self.form(
            action,
            login_response.url,
            data | {
                'token': generate_token(self.signer, code=data['guid']),
                'fert': self.signer.certificate.get_notAfter()[2:].decode(),
            }
        )


class SATPortal(PortalManager):
    BASE_URL = 'https://loginda.siat.sat.gob.mx'

    def login(self):
        res = self.get(
            url=f'{self.BASE_URL}/nidp/app/login?id=fiel'
        )
        assert res.status_code == 200
        action, data = get_form(res)

        return self.fiel_login(
            login_response=self.form(action, res.url, data)
        )

    def home_page(self):
        return self.get(
            url=f'{self.BASE_URL}/nidp/app?sid=0'
        )

    def logout(self):
        return self.get(
            url=f'{self.BASE_URL}/nidp/app/logout',
            headers={
                'referer': f'{self.BASE_URL}/nidp/app?sid=0'
            },
            allow_redirects=False
        )

    def declaraciones_provisionales_login(self):
        res = self.get(
            url='https://ptscdecprov.clouda.sat.gob.mx',
            allow_redirects=True
        )
        assert res.status_code == 200

        action, data = get_form(res)
        res = self.form(action, res.url, data)
        return res


class SATFacturaElectronica(PortalManager):
    BASE_URL = 'https://portal.facturaelectronica.sat.gob.mx'
    REQUEST_CONTEXT = 'appId=cid-v1:20ff76f4-0bca-495f-b7fd-09ca520e39f7'

    def __init__(self, signer: Signer):
        super().__init__(signer)
        self._ajax_id = random_ajax_id()
        self._request_verification_token = None

    def login(self):
        res = self.get(
            url=self.BASE_URL
        )
        assert res.status_code == 200
        try:
            action, data = get_form(res)
        except IndexError as ex:
            raise ValueError("Login form not found, please try again") from ex

        if action.startswith('https://cfdiau.sat.gob.mx/'):
            assert 'nidp/wsfed/ep?id=SATUPCFDiCon' in action

            res = self.fiel_login(
                login_response=self.form(
                    action.replace('nidp/wsfed/ep?id=SATUPCFDiCon', 'nidp/app/login?id=SATx509Custom'),
                    res.url,
                    data
                )
            )

            action, data = get_form(res)
            res = self.form(action, res.url, data)

            action, data = get_form(res)

        res = self.form(action, res.url, data)

        self._request_verification_token = request_verification_token(res)
        self._ajax_id = random_ajax_id()
        return res

    def _reload_verification_token(self):
        res = self.get(
            url=f'{self.BASE_URL}/Factura/GeneraFactura',
            allow_redirects=False
        )
        if res.status_code == 200:
            self._request_verification_token = request_verification_token(res)
        else:
            raise ValueError('Please Login Again')

    def reactivate_session(self):
        res = self.post(
            url=f'{self.BASE_URL}/Home/ReActiveSession',
            headers={
                'Origin': self.BASE_URL,
                'Request-Context': self.REQUEST_CONTEXT,
                'Request-Id': f'|{self._ajax_id}.{random_ajax_id()}'
            },
            allow_redirects=False
        )
        return res

    def _request(self, method, path, data=None, params=None):
        if self._request_verification_token is None:
            self._reload_verification_token()

        res = self.request(
            method=method,
            url=f'{self.BASE_URL}/{path}',
            headers={
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

    def legal_name_valid(self, rfc, legal_name):
        res = self._request(
            method='POST',
            path='Clientes/ValidaRazonSocialRFC',
            data={
                'rfcValidar': rfc.upper(),
                'razonSocial': legal_name.upper(),
            })
        if not res['exitoso']:
            raise ResponseError(res)
        return res['resultado']

    def rfc_valid(self, rfc):
        res = self._request(
            method='POST',
            path='Clientes/ExisteLrfc',
            data={
                'rfcValidar': rfc.upper()
            }
        )
        if not res['exitoso']:
            raise ResponseError(res)
        return res['resultado']

    def lco_details(self, rfc, apply_border_region=True):
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


class SATPortalConstancia(PortalManager):
    BASE_URL = 'https://login.siat.sat.gob.mx'

    def login(self):
        res = self.get(
            url=f'{self.BASE_URL}/nidp/idff/sso?id=fiel_Aviso'
        )
        assert res.status_code == 200
        action, data = get_form(res)
        if action is None:
            return res

        return self.fiel_login(
            login_response=self.form(action, res.url, data)
        )

    def generar_constancia(self):
        self.login()
        res = self.get(
            url="https://rfcampc.siat.sat.gob.mx/app/seg/SessionBroker?url=/PTSC/IdcSiat/autc/ReimpresionTramite/ConsultaTramite.jsf&parametro=c&idSessionBit=&idSessionBit=null",
            allow_redirects=True
        )
        assert res.status_code == 200

        # Execute Authentication Request
        action, data = get_form(res)
        if action == "https://login.siat.sat.gob.mx/nidp/saml2/sso":
            res = self.form(action, res.url, data)
            assert res.status_code == 200

            # Execute Authentication Response
            action, data = get_form(res)
            assert action == "https://rfcampc.siat.sat.gob.mx/saml2/sp/acs/post"
            res = self.form(action, res.url, data)
            assert res.status_code == 200

        # Execute formReimpAcuse
        action, data = get_form(res)
        if action == "https://rfcampc.siat.sat.gob.mx/PTSC/IdcSiat/autc/ReimpresionTramite/ConsultaTramite.jsf":
            data = {
                'javax.faces.partial.ajax': "true",
                'javax.faces.source': 'formReimpAcuse:j_idt50',
                'javax.faces.partial.execute': '@all',
                'formReimpAcuse:j_idt50': 'formReimpAcuse:j_idt50',
                'formReimpAcuse': 'formReimpAcuse',
                'formReimpAcuse:tipoTramite_input': '0',
                'formReimpAcuse:tipoTramite_focus': '',
                'formReimpAcuse:fechaInicio_input:': '',
                'formReimpAcuse:fechaFin_input': '',
                'formReimpAcuse:folio': '',
                'javax.faces.ViewState': data['javax.faces.ViewState']
            }
            res = self.form(action, res.url, data)
            assert res.status_code == 200

        res = self.get(
            url='https://rfcampc.siat.sat.gob.mx/PTSC/IdcSiat/IdcGeneraConstancia.jsf'
        )
        assert res.status_code == 200
        return res.content


class SATPortalOpinionCumplimiento(PortalManager):
    BASE_URL = 'https://login.mat.sat.gob.mx'

    def descargar_opinion_cumplimiento(self) -> bytes:
        """Download Opinión de Cumplimiento (32-D) from SAT portal.

        Returns:
            bytes: PDF content of the Opinión de Cumplimiento
        """

        # Step 1: Navigate to portal → redirects to CIEC login
        res = self.get(
            "https://ptsc32d.clouda.sat.gob.mx/?/reporteOpinion32DContribuyente",
            allow_redirects=True,
        )
        assert res.status_code == 200

        # Step 2: Switch to FIEL login (Referer required for non-empty response)
        action, data = get_form(res)
        if action.startswith("https://loginda.siat.sat.gob.mx/nidp/app/login"):
            fiel_action = action.replace("id=ciec", "id=fiel")
            res = self.form(fiel_action, res.url, data)
            assert res.status_code == 200 and len(res.text) > 0, "FIEL login page empty"

            # Step 3: FIEL authentication
            res = self.fiel_login(res)
            assert res.status_code == 200

        # Step 4: Follow JS redirect (top.location.href = OAuth2 authz URL)
        for location in re.finditer(r"location\.href=['\"]([^'\"]+)['\"]", res.text):
            res = self.get(location, allow_redirects=True)
            assert res.status_code == 200
            break

        # Step 5: Follow remaining SAML/OAuth form redirects
        for _ in range(10):
            try:
                action, data = get_form(res)
                if not action:
                    break
                res = self.form(action, res.url, data)
            except Exception as ex:
                break

        # Step 6: Download the PDF via POST
        rfc = self.signer.rfc
        pdf_res = self.post(
            "https://ptsc32d.clouda.sat.gob.mx/RespuestaCompleta/ObtenerRespuestaCompletaPdf",
            json={
                "canal": "G",
                "curp": "",
                "idCorrelacion": str(uuid.uuid4()),
                "ip": "127.0.0.1",
                "rfc": rfc,
                "tipoConsulta": "COMPLETA",
                "tipoReporte": "32D",
                "usuario": rfc,
                "rfcCorto": rfc,
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Origin": "https://ptsc32d.clouda.sat.gob.mx",
                "Referer": "https://ptsc32d.clouda.sat.gob.mx/",
            },
        )
        assert pdf_res.status_code == 200, f"ObtenerPdf returned {pdf_res.status_code}"

        json_data = pdf_res.json()
        b64_content = json_data.get("ContenidoBase64")
        if not b64_content:
            raise RuntimeError("SAT no retornó el PDF de la opinión 32-D")

        return base64.b64decode(b64_content)
