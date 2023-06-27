import base64
import time

import requests
from lxml import etree

from . import PAC, Environment, Accept, Document, CancelReason, CancelationAcknowledgment, AcceptRejectAcknowledgment, TaxpayerStatus
from ..exceptions import ResponseError
from .. import __version__
from ..models import Signer
from ..xelement import XElement
from ..cfdi import CFDI
from ..create.cancela import cancelacionretencion
from ..create.cancela.aceptacionrechazo import SolicitudAceptacionRechazo
from ..create.cancela.cancelacion import Cancelacion


class SWSapien(PAC):
    """
    Luna Soft, S.A. de C.V.
    SW sapien-SmarterWEB
    """
    RFC = "LSO1306189R5"

    def __init__(self, token=None, user=None, password=None, environment=Environment.PRODUCTION):
        super().__init__(environment)
        if token:
            def get_token():
                return "Bearer " + token
        else:
            def get_token():
                if not self.token or time.time() > self.expires_in:
                    auth_obj = self._authenticate(user, password)
                    self.token = auth_obj["token"]
                    self.expires_in = auth_obj["expires_in"]
                return "Bearer " + self.token

        self.token_fn = get_token

    def _host(self, service="services"):
        match service:
            case "services":
                match self.environment:
                    case Environment.PRODUCTION:
                        return "https://services.sw.com.mx"
                    case Environment.TEST:
                        return "https://services.test.sw.com.mx"
            case "api":
                match self.environment:
                    case Environment.PRODUCTION:
                        return "https://api.sw.com.mx"
                    case Environment.TEST:
                        return "https://api.test.sw.com.mx"

        raise NotImplementedError("Environment not Supported")

    def _request(self, path, headers=None, method="post", files=None, json=None, needs_token=True, service="services"):
        host = self._host(service)

        r = requests.request(
            method=method,
            url=f"{host}/{path}",
            headers={
                'Cache-Control': "no-cache",
                "Authorization": self.token_fn() if needs_token else "",
                "User-Agent": __version__.__user_agent__,
                **(headers or {})
            },
            json=json,
            files=files
        )

        if r.ok:
            res = r.json()
            if res["status"] != "success":
                raise ResponseError(r)
            return res
        else:
            raise ResponseError(r)

    def _authenticate(self, user, password):
        return self._request(
            path="/security/authenticate",
            headers={'user': user, 'password': password},
            needs_token=False
        )

    def _generate_pdf(self, xml: str):
        return self._request(
            path="pdf/v1/api/GeneratePdf",
            service="api",
            json={
                "xmlContent": xml,
                # "logo": None,
                # "extras": None,
                # "templateId": None
            }
        )

    def _issue_stamp(self, cfdi: CFDI, accept: Accept = Accept.XML, ref_id: str = None, operation="stamp") -> Document:
        headers = {}
        if ref_id:
            headers["customid"] = ref_id

        res = self._request(
            path=f"v4/cfdi33/{operation}/v4",
            files=[
                ('xml', ('xml', cfdi.xml_bytes(), 'text/xml')),
            ],
            headers=headers
        )

        pdf = None
        if accept & Accept.PDF:
            pdf = self._generate_pdf(xml=res["data"]["cfdi"])
            pdf = base64.b64decode(pdf['data']['contentB64'])

        return Document(
            document_id=res["data"]["uuid"],
            xml=res["data"]["cfdi"].encode() if accept & accept.XML else None,
            pdf=pdf
        )

    def validate(self, cfdi: CFDI):
        res = self._request(
            path=f"validate/cfdi",
            files=[
                ('xml', ('xml', cfdi.xml_bytes(), 'text/xml')),
            ],
        )
        return res

    def issue(self, cfdi: CFDI, accept: Accept = Accept.XML, ref_id: str = None) -> Document:
        return self._issue_stamp(cfdi=cfdi, accept=accept, ref_id=ref_id, operation="issue")

    def stamp(self, cfdi: CFDI, accept: Accept = Accept.XML, ref_id: str = None) -> Document:
        return self._issue_stamp(cfdi=cfdi, accept=accept, ref_id=ref_id, operation="stamp")

    def recover(self, document_id: str, accept: Accept = Accept.XML) -> Document:
        return self._request(
            path=f"datawarehouse/v1/live/{document_id}",
            service="api",
            method="get"
        )

    def cancel(self, cfdi: CFDI, reason: CancelReason, substitution_id: str = None, signer: Signer = None) -> CancelationAcknowledgment:
        document_id = cfdi["Complemento"]["TimbreFiscalDigital"]["UUID"]
        rfc = cfdi["Emisor"]["Rfc"]
        path = f"cfdi33/cancel/{rfc}/{document_id}/{reason.value}"
        if substitution_id:
            path += f"/{substitution_id}"

        res = self._request(
            path=path
        )

        return CancelationAcknowledgment(
            code=res["data"]["uuid"][document_id],
            acuse=res["data"]["acuse"]
        )

    def cancel_comprobante(self, cancelation: Cancelacion) -> CancelationAcknowledgment:
        res = self._request(
            path=f"cfdi33/cancel/xml",
            files=[
                ('xml', ('xml', etree.tostring(cancelation.to_xml(), encoding="UTF-8"), 'text/xml')),
            ]
        )

        return CancelationAcknowledgment(
            code=res["data"]["uuid"],
            acuse=res["data"]["acuse"]
        )

    def cancel_retencion(self, cancelation: cancelacionretencion.Cancelacion) -> CancelationAcknowledgment:
        raise NotImplementedError()

    def relations(self, cfdi: CFDI):
        document_id = cfdi["Complemento"]["TimbreFiscalDigital"]["UUID"]
        rfc = cfdi["Emisor"]["Rfc"]
        path = f"relations/{rfc}/{document_id}"

        res = self._request(
            path=path
        )

        return res

    def accept_reject(self, request: SolicitudAceptacionRechazo) -> AcceptRejectAcknowledgment:
        res = self._request(
            path=f"acceptreject/xml",
            files=[
                ('xml', ('xml', etree.tostring(request.to_xml(), encoding="UTF-8"), 'text/xml')),
            ]
        )

        return AcceptRejectAcknowledgment(
            folios={
                k["uuid"]: {
                    'estatusUUID': k['estatusUUID'],
                    'respuesta': k['respuesta']
                }
                for k in res["data"]["folios"]
            },
            acuse=res["data"]["acuse"]
        )

    def pending(self, rfc: str) -> list[str]:
        res = self._request(
            path=f"pendings/{rfc}",
            method="get"
        )
        return res['data']['uuid']

    def rfc_valid(self, rfc: str | list[str]) -> bool | list[bool]:
        raise NotImplementedError()

    def list_69b(self, rfc: str) -> TaxpayerStatus | None:
        res = self._request(
            path=f"taxpayers/{rfc}",
            method="get"
        )
        return res
