from base64 import b64encode
from html import unescape
from logging import getLogger
from typing import Dict
from warnings import warn

import requests
from lxml import etree

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
    namespaces = {
        "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "stamp": "http://facturacion.finkok.com/stamp",
    }

    def __init__(
        self, username: str, password: str, environment=Environment.PRODUCTION
    ):
        super().__init__(environment)
        self.username = username
        self.password = password

    def _build_envelope(
        self, param_element: etree.Element, nsmap: Dict[str, str] = {}
    ) -> etree.Element:
        namespaces = {**self.namespaces, **nsmap}

        envelope = etree.Element(
            etree.QName(namespaces["soapenv"], "Envelope"), nsmap=namespaces
        )
        envelope.append(etree.Element(etree.QName(namespaces["soapenv"], "Header")))
        body = etree.SubElement(envelope, etree.QName(namespaces["soapenv"], "Body"))
        body.append(param_element)
        return envelope

    def _add_auth(self, element: etree.Element, namespace: str) -> etree.Element:
        username = etree.SubElement(element, etree.QName(namespace, "username"))
        username.text = self.username
        password = etree.SubElement(element, etree.QName(namespace, "password"))
        password.text = self.password
        return element

    def _build_sign_stamp_envelope(self, cfdi: CFDI, operation: str) -> etree.Element:
        stamp_ns = self.namespaces["stamp"]
        match operation:
            case "issue":
                tag = "sign_stamp"
            case "stamp":
                tag = "stamp"
            case _:
                raise NotImplementedError("Operation not supported")

        stamp = etree.Element(etree.QName(stamp_ns, tag))
        xml = etree.SubElement(stamp, etree.QName(stamp_ns, "xml"))
        xml.text = b64encode(cfdi.xml_bytes()).decode("utf-8")
        stamp = self._add_auth(stamp, stamp_ns)

        return self._build_envelope(
            stamp, {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}
        )

    def _build_query_envelope(self, document_id: str) -> etree.Element:
        query_element = etree.Element(
            etree.QName(self.namespaces["stamp"], "query_pending")
        )
        query_element = self._add_auth(query_element, self.namespaces["stamp"])
        etree.SubElement(
            query_element, etree.QName(self.namespaces["stamp"], "uuid")
        ).text = document_id

        return self._build_envelope(query_element)

    @property
    def host(self):
        match self.environment:
            case Environment.TEST:
                return "https://demo-facturacion.finkok.com"
            case Environment.PRODUCTION:
                return "https://facturacion.finkok.com"
            case _:
                raise NotImplementedError("Environment not supported")

    @property
    def stamp_url(self):
        return f"{self.host}/servicios/soap/stamp.wsdl"

    def _perform_operation(self, cfdi: CFDI, accept: Accept, operation: str):
        if accept & Accept.PDF:
            raise NotImplementedError("accept PDF not supported")

        envelope = self._build_sign_stamp_envelope(cfdi, operation)
        data = etree.tostring(envelope)

        response = requests.post(self.stamp_url, data=data)
        root = etree.fromstring(response.text.encode())

        status = root.find(".//{apps.services.soap.core.views}CodEstatus")
        issues = root.find(".//{apps.services.soap.core.views}Incidencias")

        for issue in issues:
            code = issue.find("{apps.services.soap.core.views}CodigoError")
            msg = issue.find("{apps.services.soap.core.views}MensajeIncidencia")
            if not status:
                raise ResponseError(f"{code.text} - {msg.text}")
            warn(f"{code.text} - {msg.text}")

        logger = getLogger(f"{self.__module__}.{self.__class__.__name__}")
        logger.debug(status.text)

        xml = root.find(".//{apps.services.soap.core.views}xml").text
        uuid = root.find(".//{apps.services.soap.core.views}UUID").text

        return Document(document_id=uuid, xml=xml.encode())

    def issue(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        """Operation to request CFDI to be sealed and stamped by Finkok.

        Args:
            cfdi (CFDI): The CFDI object to be sealed and stamped
            accept (Accept, optional): The type of response to accept. Defaults to Accept.XML.

        Raises:
            NotImplementedError: If the accept parameter includes Accept.PDF
            ResponseError: If the response from the Finkok SOAP web service contains an error code

        Returns:
            Document: The stamped CFDI as a Document object with the following fields:
                - document_id (str): The UUID of the stamped CFDI.
                - xml (bytes): The XML content of the stamped CFDI.

        Notes:
            - This function currently only supports accepting XML responses.
            - If the accept parameter includes Accept.PDF, a NotImplementedError is raised.
        """
        return self._perform_operation(cfdi=cfdi, accept=accept, operation="issue")

    def stamp(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        """Operation to request sealed CFDI to be stamped by Finkok

        Args:
            cfdi (CFDI): The CFDI object to be stamped
            accept (Accept, optional): The type of response to accept. Defaults to Accept.XML.

        Raises:
            NotImplementedError: If the accept parameter includes Accept.PDF
            ResponseError: If the response from the Finkok SOAP web service contains an error code

        Returns:
            Document: The stamped CFDI as a Document object with the following fields:
                - document_id (str): The UUID of the stamped CFDI.
                - xml (bytes): The XML content of the stamped CFDI.

        Notes:
            - This function currently only supports accepting XML responses.
            - If the accept parameter includes Accept.PDF, a NotImplementedError is raised.
        """
        return self._perform_operation(cfdi=cfdi, accept=accept, operation="stamp")

    def recover(self, document_id: str, accept: Accept = Accept.XML) -> Document:
        """Recover a document from Finkok SOAP web service by its document ID (UUID).

        Args:
            document_id (str): The UUID of the document to recover.
            accept (Accept, optional): The type of response to accept. Defaults to Accept.XML.

        Raises:
            NotImplementedError: If the accept parameter includes Accept.PDF.
            ResponseError: If the response from the Finkok SOAP web service contains an error code.

        Returns:
            Document: The recovered document as a Document object with the following fields:
                - document_id (str): The UUID of the recovered document.
                - xml (bytes): The XML content of the recovered document.

        Notes:
            - This function currently only supports accepting XML responses.
            - If the accept parameter includes Accept.PDF, a NotImplementedError is raised.
        """
        if accept & Accept.PDF:
            raise NotImplementedError("accept PDF not supported")

        envelope = self._build_query_envelope(document_id)
        data = etree.tostring(envelope)

        response = requests.post(self.stamp_url, data)
        root = etree.fromstring(response.text.encode())

        error = root.find(".//{apps.services.soap.core.views}error")
        if error is not None:
            raise ResponseError(error.text)

        xml = unescape(root.find(".//{apps.services.soap.core.views}xml").text)
        uuid = root.find(".//{apps.services.soap.core.views}uuid").text

        return Document(document_id=uuid, xml=xml.encode())
