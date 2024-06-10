from base64 import b64encode
from dataclasses import dataclass
from enum import Enum
from html import unescape
from logging import getLogger
from typing import Dict
from warnings import warn

import requests
from lxml import etree

from satcfdi.cfdi import CFDI
from satcfdi.pacs import Accept, Document

from ..exceptions import ResponseError
from . import PAC, CancelationAcknowledgment, CancelReason, Environment


class DocumentStatus(Enum):
    STAMPED = "S"
    FINISHED = "F"


@dataclass(init=True)
class PendingDocument(Document):
    status: DocumentStatus = None


class Finkok(PAC):
    """
    Finkok, S.A.P.I. de C.V.
    Finkok
    """

    RFC = "FIN1203015JA"
    namespaces = {
        "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "apps": "apps.services.soap.core.views",
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
            case "quick_stamp":
                tag = "quick_stamp"
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

    def get_service_url(self, operation: str):
        if operation not in ["stamp", "cancel"]:
            raise NotImplementedError(f"Operation {operation} not supported")
        return f"{self.host}/servicios/soap/{operation}.wsdl"

    @property
    def stamp_url(self):
        return f"{self.host}/servicios/soap/stamp.wsdl"

    def _perform_stamp_operation(self, cfdi: CFDI, accept: Accept, operation: str):
        if accept & Accept.PDF:
            raise NotImplementedError("accept PDF not supported")

        envelope = self._build_sign_stamp_envelope(cfdi, operation)
        data = etree.tostring(envelope)

        url = self.get_service_url("stamp")
        response = requests.post(url, data=data)
        root = etree.fromstring(response.text.encode())

        status = root.find(".//apps:CodEstatus", self.namespaces)
        issues = root.find(".//apps:Incidencias", self.namespaces)

        for issue in issues:
            code = issue.find("apps:CodigoError", self.namespaces)
            msg = issue.find("apps:MensajeIncidencia", self.namespaces)
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
        return self._perform_stamp_operation(
            cfdi=cfdi, accept=accept, operation="stamp"
        )

    def quick_stamp(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        """Operation to request sealed CFDI to be stamped by Finkok using the quick stamp service.

        This operation is recommended for high amount of stamp requests per second.

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
        return self._perform_stamp_operation(
            cfdi=cfdi, accept=accept, operation="quick_stamp"
        )

    def stamped(self, document_id: str) -> Document:
        pass

    def pending_stamp(
        self, document_id: str, accept: Accept = Accept.XML
    ) -> PendingDocument:
        """Check the status of a document that is pending to be sent to the SAT (by failure or quick stamp)

        Args:
            document_id (str): The UUID of the document to recover.
            accept (Accept, optional): The type of response to accept. Defaults to Accept.XML.

        Raises:
            NotImplementedError: If the accept parameter includes Accept.PDF.
            ResponseError: If the response from the Finkok SOAP web service contains an error code.

        Returns:
            PendingDocument: The PendingDocument object with the following attributes:
            - document_id (str): The UUID of the document.
            - xml (bytes): The XML content of the document.
            - status (DocumentStatus): The status of the document.
                - `STAMPED`, the document has been stamped but not sent to the SAT.
                - `FINISHED`, the document has been stamped and sent to the SAT.


        Notes:
            - This function currently only supports accepting XML responses.
            - If the accept parameter includes Accept.PDF, a NotImplementedError is raised.
        """
        if accept & Accept.PDF:
            raise NotImplementedError("accept PDF not supported")

        envelope = self._build_query_envelope(document_id)
        data = etree.tostring(envelope)

        url = self.get_service_url("stamp")
        response = requests.post(url, data)
        root = etree.fromstring(response.text.encode())
        open("test.xml", "wb").write(etree.tostring(root, pretty_print=True))

        error = root.find(".//apps:error", self.namespaces)
        if error is not None and error.text:
            raise ResponseError(error.text)

        status = root.find(".//apps:status", self.namespaces)
        xml = root.find(".//apps:xml", self.namespaces)
        uuid = root.find(".//apps:uuid", self.namespaces)

        return PendingDocument(
            document_id=uuid.text,
            xml=unescape(xml.text).encode() if xml is not None else None,
            status=DocumentStatus(status.text),
        )

        return Document(document_id=uuid, xml=xml.encode())
