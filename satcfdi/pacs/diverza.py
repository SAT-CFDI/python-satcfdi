import base64
import io
from zipfile import ZipFile

from lxml.etree import QName
from packaging import version
import requests

from . import PAC, Environment, Accept, Document, CancelReason, CancelationAcknowledgment
from .. import __version__
from ..exceptions import ResponseError, DocumentNotFoundError
from ..cfdi import CFDI
from ..utils import iterate
from ..models import Signer


def _process_content(response, fmt):
    if content := response.get("content"):
        match fmt:
            case "xml":
                response["xml"] = base64.b64decode(content)
            case "pdf":
                response["pdf"] = base64.b64decode(content)
            case "zip":
                zip_data = base64.b64decode(content)
                with io.BytesIO(zip_data) as b:
                    with ZipFile(b, "r") as zf:
                        response["xml"] = zf.read('invoice.xml')
                        response["pdf"] = zf.read('invoice.pdf')


def _process_format(accept: Accept):
    match accept:
        case Accept.XML_PDF:
            return "zip"
        case Accept.PDF:
            return "pdf"
        case Accept.XML:
            return "xml"
        case _:
            raise NotImplementedError()


class Diverza(PAC):
    """
    Class to call Diverza API's
    see https://diverza.docs.apiary.io/ for more information
    """
    RFC = "SNF171020F3A"

    def __init__(self, rfc: str, id: str, token: str, environment=Environment.PRODUCTION):
        """
        :param rfc: Document emitter's RFC Info
        :param id: ID assigned by Diverza when the client is registered
        :param token: Security token assigned by Diverza. It must match with the Client & Tax ID (RFC)
        """
        super().__init__(environment)
        self.payload_append = {
            "credentials": {
                "id": id,
                "token": token
            },
            "issuer": {
                "rfc": rfc
            }
        }

    def _request(self, path, json, method="post"):
        json = self.payload_append | json
        match self.environment:
            case Environment.PRODUCTION:
                host = "https://servicios.diverza.com"
            case Environment.TEST:
                host = "https://serviciosdemo.diverza.com"
            case _:
                raise NotImplementedError("Environment not Supported")

        r = requests.request(
            method=method,
            url=f"{host}/{path}",
            headers={
                "User-Agent": __version__.__user_agent__
                # Nota: Header de Accept genera errores
            },
            json=json
        )

        if r.ok:
            return r
        else:
            raise ResponseError(r)

    def _issue_stamp(self, cfdi: CFDI, accept: Accept = Accept.XML, ref_id: str = None, operation: str = "stamp") -> Document:
        raw_cfdi = base64.b64encode(cfdi.xml_bytes()).decode()
        fmt = _process_format(accept)

        def _process_vnd():
            if comp := [QName(x.tag).localname for x in iterate(cfdi.get("Complemento"))]:
                if "Nomina" in comp:
                    return f"application/vnd.diverza.cfdi_{cfdi['Version']}_complemento_nomina+xml"
                else:
                    return f"application/vnd.diverza.cfdi_{cfdi['Version']}_complemento+xml"
            else:
                return f"application/vnd.diverza.cfdi_{cfdi['Version']}+xml"

        def _process_path():
            if version.parse(cfdi['Version']) >= version.parse("4.0"):
                return f'api/v2/documents/{operation}'
            return f"api/v1/documents/{operation}"

        json = {
            "issuer": {
                "rfc": cfdi["Emisor"]["Rfc"]
            },
            "receiver": {
                "emails": []
            },
            "document": {
                "certificate-number": cfdi["NoCertificado"],
                "section": "all",
                "format": fmt,
                "type": _process_vnd(),
                "content": raw_cfdi,
                "template": "letter"
            }
        }
        if ref_id:
            json["document"]["ref-id"] = ref_id

        res = self._request(
            path=_process_path(),
            json=json
        ).json()

        _process_content(res, fmt)
        return Document(
            document_id=res['uuid'],
            xml=res.get('xml'),
            pdf=res.get('pdf'),
        )

    def issue(self, cfdi: CFDI, accept: Accept = Accept.XML, ref_id: str = None) -> Document:
        return self._issue_stamp(cfdi=cfdi, accept=accept, ref_id=ref_id, operation="issue")

    def stamp(self, cfdi: CFDI, accept: Accept = Accept.XML, ref_id: str = None) -> Document:
        return self._issue_stamp(cfdi=cfdi, accept=accept, ref_id=ref_id, operation="stamp")

    def cancel(self, cfdi: CFDI, reason: CancelReason, substitution_id: str = None, signer: Signer = None) -> CancelationAcknowledgment:
        def _process_path():
            if version.parse(cfdi['Version']) >= version.parse("4.0"):
                return f"api/v2/documents/{document_id}/cancel"
            return f"api/v1/documents/{document_id}/cancel"

        document_id = cfdi["Complemento"]["TimbreFiscalDigital"]["UUID"]
        res = self._request(
            path=_process_path(),
            json={
                "issuer": {
                    "rfc": cfdi["Emisor"]["Rfc"]
                }
            },
            method="put"
        ).json()

        if res["status"] == "canceled":
            return CancelationAcknowledgment(
                code="202"
            )

        raise Exception("Unknow Response: " + res.text)

    def recover(self, document_id: str, accept: Accept = Accept.XML) -> Document:
        fmt = _process_format(accept)

        def doc_recover(version):
            return self._request(
                path=f"api/{version}/documents/{document_id}/reprint",
                json={
                    "receiver": {
                        "emails": []
                    },
                    "document": {
                        "section": "all",
                        "format": fmt,
                        "template": "letter"
                    }
                }
            ).json()

        try:
            res = doc_recover("v2")
        except ResponseError as ex_v2:
            if ex_v2.response.status_code != 404:
                raise

            try:
                res = doc_recover("v1")
            except ResponseError:
                raise DocumentNotFoundError(ex_v2.response)

        _process_content(res, fmt)
        return Document(
            document_id=res['uuid'],
            xml=res.get('xml'),
            pdf=res.get('pdf'),
        )

    def rfc_valid(self, rfc: str | list[str]) -> bool | list[bool]:
        r = self._request(
            path="api/v1/rfc/status",
            json={
                "identifiers": [
                    {
                        "rfc": r
                    }
                    for r in iterate(rfc)
                ]
            }
        )

        res = r.json()
        if isinstance(rfc, str):
            return res['identifiers'][0]['active'] == "Y"

        return [
            i["active"] == "Y" for i in res['identifiers']
        ]
