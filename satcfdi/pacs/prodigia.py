import base64
from typing import Sequence

import requests
from requests.auth import HTTPBasicAuth

from . import PAC, Accept, Document, CancelReason, CancelationAcknowledgment, Environment
from .. import __version__
from ..exceptions import ResponseError
from ..models import Signer
from ..cfdi import CFDI


class Prodigia(PAC):
    """
    PAC de facturacion Prodigia

    Documentacion: https://www.prodigia.com.mx/api-de-integracion-para-timbrado-de-cfdi
    """
    RFC = "PPD101129EA3"

    def __init__(self, user: str, password: str, contrato: str, environment=Environment.PRODUCTION):
        super().__init__(environment=environment)
        self.auth = HTTPBasicAuth(user, password)
        self.contrato = contrato

    def _request(self, path, data, method="post", opciones: Sequence[str] = None):
        host = "https://timbrado.pade.mx/servicio/rest"
        params = [
            ("contrato", self.contrato),
            ("opciones", 'RESPUESTA_JSON'),
            ("opciones", 'REGRESAR_CON_ERROR_307_XML'),
        ]

        if opciones:
            for o in opciones:
                params.append(
                    ('opciones', o)
                )

        r = requests.request(
            method=method,
            url=f"{host}/{path}",
            headers={
                "User-Agent": __version__.__user_agent__,
                "Content-Type": "application/xml",
                # Nota: Header de Accept genera errores
            },
            data=data,
            auth=self.auth,
            params=params
        )

        if r.ok:
            return r
        else:
            raise ResponseError(r)

    def issue(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        pass

    def stamp(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        match (self.environment, cfdi.tag):
            case Environment.PRODUCTION, '{http://www.sat.gob.mx/cfd/4}Comprobante':
                path = "timbrado40"
            case Environment.TEST, '{http://www.sat.gob.mx/cfd/4}Comprobante':
                path = "timbrado40Prueba"
            case _:
                raise NotImplementedError("Not Supported CFDI")

        opciones = []
        if accept & Accept.PDF:
            opciones.append("GENERAR_PDF")

        res = self._request(
            path=path,
            data=cfdi.xml_bytes(),
            opciones=opciones
        ).json()

        servicio_timbrado = res['servicioTimbrado']

        if not servicio_timbrado['timbradoOk']:
            raise ResponseError(res)

        return Document(
            document_id=servicio_timbrado['UUID'],
            xml=base64.b64decode(servicio_timbrado['xmlBase64']) if accept & Accept.XML else None,
            pdf=base64.b64decode(servicio_timbrado['pdfBase64']) if accept & Accept.PDF else None
        )

    def cancel(self, cfdi: CFDI, reason: CancelReason, substitution_id: str = None, signer: Signer = None) -> CancelationAcknowledgment:
        raise NotImplementedError()

    def recover(self, document_id: str, accept: Accept = Accept.XML) -> Document:
        raise NotImplementedError()

    def rfc_valid(self, rfc: str | list[str]) -> bool | list[bool]:
        raise NotImplementedError()
