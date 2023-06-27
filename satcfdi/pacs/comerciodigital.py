import requests

from . import PAC, Accept, Document, CancelationAcknowledgment, CancelReason, Environment
from .. import __version__
from ..cfdi import CFDI
from ..exceptions import ResponseError
from ..models import Signer


class ComercioDigital(PAC):
    RFC = "SCD110105654"

    def __init__(self, user: str, password: str, environment=Environment.PRODUCTION):
        super().__init__(environment=environment)
        self.user = user.replace('Ñ', '@')
        self.password = password

    def _request(self, path, data, method="post", headers=None):
        match self.environment:
            case Environment.PRODUCTION:
                host = "https://ws.comercio-digital.mx"
            case Environment.TEST:
                host = "https://pruebas.comercio-digital.mx"
            case _:
                raise NotImplementedError("Not Implemented Environment")

        h = {
            "User-Agent": __version__.__user_agent__,
            "Content-Type": "text/plain",
            "usrws": self.user,
            "pwdws": self.password,
            "tipo": "XML"
        }
        if headers:
            h = h | headers

        r = requests.request(
            method=method,
            url=f"{host}/{path}",
            headers=h,
            data=data,
        )

        if r.ok and 'errmsg' not in r.headers and r.headers['codigo'] == '000':
            return r
        else:
            raise ResponseError(r)

    def issue(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        raise NotImplementedError()

    def stamp(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        match cfdi.tag:
            case '{http://www.sat.gob.mx/cfd/3}Comprobante':
                path = "timbre/timbrarV5"
            case '{http://www.sat.gob.mx/cfd/4}Comprobante':
                path = "timbre4/timbrarV5"
            case _:
                raise NotImplementedError("cfdi type not supported")

        if accept & Accept.PDF:
            raise NotImplementedError("accept PDF not supported")

        res = self._request(
            path=path,
            data=iter((
                b'<?xml version="1.0" encoding="utf-8"?>',
                cfdi.xml_bytes(xml_declaration=False)
            ))
        )

        return Document(
            document_id=res.headers['uuid'],
            xml=res.content if accept & Accept.XML else None
        )

    def cancel(self, cfdi: CFDI, reason: CancelReason, substitution_id: str = None, signer: Signer = None) -> CancelationAcknowledgment:
        raise NotImplementedError()

    def recover(self, document_id: str, accept: Accept = Accept.XML) -> Document:
        raise NotImplementedError()

    def rfc_valid(self, rfc: str | list[str]) -> bool | list[bool]:
        raise NotImplementedError()
