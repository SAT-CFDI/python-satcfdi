import xml.etree.ElementTree as ET
from base64 import b64encode
from logging import getLogger
from warnings import warn

import requests

from satcfdi.cfdi import CFDI
from satcfdi.pacs import Accept, Document

from ..exceptions import ResponseError
from . import PAC, Environment


class Finkok(PAC):
    """
    Finkok, S.A.P.I. de C.V.
    Finkok
    """

    RFC = "FIN1203015JA"

    def __init__(
        self, username: str, password: str, environment=Environment.PRODUCTION
    ):
        super().__init__(environment)
        self.username = username
        self.password = password

    def _get_soap_envelope(self, cfdi: CFDI) -> ET.Element:
        ET.register_namespace("stamp", "http://facturacion.finkok.com/stamp")
        ET.register_namespace("SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")
        ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

        envelope = ET.Element("{http://schemas.xmlsoap.org/soap/envelope/}Envelope")
        envelope.append(ET.Element("{http://schemas.xmlsoap.org/soap/envelope/}Header"))
        body = ET.SubElement(
            envelope, "{http://schemas.xmlsoap.org/soap/envelope/}Body"
        )
        stamp = ET.SubElement(body, "{http://facturacion.finkok.com/stamp}quick_stamp")
        xml = ET.SubElement(stamp, "{http://facturacion.finkok.com/stamp}xml")
        xml.text = b64encode(cfdi.xml_bytes()).decode("utf-8")
        username = ET.SubElement(stamp, "{http://facturacion.finkok.com/stamp}username")
        username.text = self.username
        password = ET.SubElement(stamp, "{http://facturacion.finkok.com/stamp}password")
        password.text = self.password

        return envelope

    @property
    def host(self):
        match self.environment:
            case Environment.TEST:
                return "https://demo-facturacion.finkok.com"
            case Environment.PRODUCTION:
                return "https://facturacion.finkok.com"
            case _:
                raise NotImplementedError("Environment not supported")

    def stamp(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:

        if accept & Accept.PDF:
            raise NotImplementedError("accept PDF not supported")

        envelope = self._get_soap_envelope(cfdi)
        url = f"{self.host}/servicios/soap/stamp.wsdl"
        data = ET.tostring(envelope, encoding="utf-8", xml_declaration=True)

        response = requests.post(url, data)
        stamp_response = ET.fromstring(response.text)

        status = stamp_response.find(".//{apps.services.soap.core.views}CodEstatus")
        issues = stamp_response.find(".//{apps.services.soap.core.views}Incidencias")

        for issue in issues:
            code = issue.find("{apps.services.soap.core.views}CodigoError")
            msg = issue.find("{apps.services.soap.core.views}MensajeIncidencia")
            if not status:
                raise ResponseError(f"{code.text} - {msg.text}")
            warn(f"{code.text} - {msg.text}")

        logger = getLogger(f"{self.__module__}.{self.__class__.__name__}")
        logger.debug(status.text)

        xml = stamp_response.find(".//{apps.services.soap.core.views}xml").text
        uuid = stamp_response.find(".//{apps.services.soap.core.views}UUID").text

        return Document(
            document_id=uuid,
            xml=xml.encode(),
            pdf=None,
        )
