from base64 import b64encode
from dataclasses import dataclass
from enum import Enum
from html import unescape
from logging import getLogger
from typing import Literal, Sequence
from warnings import warn

import requests
from lxml import etree

from satcfdi.cfdi import CFDI
from satcfdi.create.cancela import cancelacion
from satcfdi.create.cancela.aceptacionrechazo import SolicitudAceptacionRechazo
from satcfdi.models.signer import Signer
from satcfdi.pacs import Accept, Document
from satcfdi.xelement import XElement

from ..exceptions import DocumentNotFoundError, ResponseError
from . import (
    PAC,
    AcceptRejectAcknowledgment,
    CancelationAcknowledgment,
    CancelReason,
    Environment,
)


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
        "apps": "apps.services.soap.core.views",
        "cancel": "http://facturacion.finkok.com/cancel",
        "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "stamp": "http://facturacion.finkok.com/stamp",
    }

    def __init__(
        self, username: str, password: str, environment=Environment.PRODUCTION
    ):
        super().__init__(environment)
        self.username = username
        self.password = password

    @property
    def _logger(self):
        return getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def _build_envelope(self, body_child: etree.Element) -> etree.Element:
        envelope_qname = etree.QName(self.namespaces["soapenv"], "Envelope")
        envelope = etree.Element(envelope_qname, nsmap=self.namespaces)

        header_qname = etree.QName(self.namespaces["soapenv"], "Header")
        envelope.append(etree.Element(header_qname))

        body_qname = etree.QName(self.namespaces["soapenv"], "Body")
        body = etree.SubElement(envelope, body_qname)
        body.append(body_child)
        return envelope

    def _add_auth(self, element: etree.Element, namespace: str) -> etree.Element:
        username = etree.SubElement(element, etree.QName(namespace, "username"))
        username.text = self.username
        password = etree.SubElement(element, etree.QName(namespace, "password"))
        password.text = self.password
        return element

    def _build_xml_envelope(self, xelement: XElement, operation: str) -> etree.Element:
        match operation:
            case "issue":
                namespace = self.namespaces["stamp"]
                tag = "sign_stamp"
            case "stamp":
                namespace = self.namespaces["stamp"]
                tag = "stamp"
            case "quick_stamp":
                namespace = self.namespaces["stamp"]
                tag = "quick_stamp"
            case "stamped":
                namespace = self.namespaces["stamp"]
                tag = "stamped"
            case "cancel":
                namespace = self.namespaces["cancel"]
                tag = "cancel_signature"
            case "accept_reject":
                namespace = self.namespaces["cancel"]
                tag = "accept_reject_signature"
            case _:
                raise NotImplementedError("Operation not supported")

        operation_element = etree.Element(etree.QName(namespace, tag))
        xml = etree.SubElement(operation_element, etree.QName(namespace, "xml"))
        xml.text = b64encode(xelement.xml_bytes(xml_declaration=True))
        operation_element = self._add_auth(operation_element, namespace)

        return self._build_envelope(operation_element)

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

    def get_service_url(self, operation: Literal["stamp", "cancel"]):
        if operation not in ["stamp", "cancel"]:
            raise NotImplementedError(f"Operation {operation} not supported")
        return f"{self.host}/servicios/soap/{operation}.wsdl"

    @property
    def stamp_url(self):
        return f"{self.host}/servicios/soap/stamp.wsdl"

    def _perform_request(self, url: str, envelope: etree.Element) -> etree.Element:
        """Sends a POST request to the specified URL with the provided XML envelope and returns the parsed XML response.

        Args:
            url (str): The URL to send the request to.
            envelope (etree.Element): The XML envelope to send in the request.

        Returns:
            etree.Element: The parsed XML response from the request.
        """
        data = etree.tostring(envelope)
        response = requests.post(url=url, data=data)
        return etree.fromstring(response.content)

    def _validate_stamp_response(self, root: etree.Element):
        status = root.find(".//apps:CodEstatus", self.namespaces)
        issues = root.find(".//apps:Incidencias", self.namespaces)

        for issue in issues:
            code = issue.find("apps:CodigoError", self.namespaces)
            msg = issue.find("apps:MensajeIncidencia", self.namespaces)
            full_msg = f"{code.text} - {msg.text}" if code is not None else msg.text
            if (
                status is None
                or status.text != "Comprobante timbrado satisfactoriamente"
            ):
                raise ResponseError(full_msg)
            warn(full_msg)

        if status is not None and status.text:
            self._logger.info(status.text)

    def _validate_cancel_response(self, root: etree.Element):
        cancel_status = root.find(".//apps:EstatusCancelacion", self.namespaces)
        if cancel_status is not None and cancel_status.text:
            self._logger.info(cancel_status.text)

        ws_status = root.find(".//apps:CodEstatus", self.namespaces)
        if ws_status is not None and ws_status.text:
            if ws_status.text.endswith("No Encontrado"):
                raise DocumentNotFoundError(ws_status.text)
            raise ResponseError(ws_status.text)

        error = root.find(".//apps:error", self.namespaces)
        if error is not None and error.text:
            raise ResponseError(error.text)

    def _perform_stamp_operation(self, cfdi: CFDI, accept: Accept, operation: str):
        if not isinstance(cfdi, CFDI):
            raise TypeError("cfdi must be a CFDI object")

        if accept & Accept.PDF:
            raise NotImplementedError("accept PDF not supported")

        envelope = self._build_xml_envelope(cfdi, operation)
        url = self.get_service_url("stamp")
        root = self._perform_request(url, envelope)

        self._validate_stamp_response(root)

        xml = root.find(".//apps:xml", self.namespaces).text
        uuid = root.find(".//apps:UUID", self.namespaces).text
        return Document(document_id=uuid, xml=xml.encode())

    def _perform_cancel_operation(self, cancellation: XElement, operation: str):
        envelope = self._build_xml_envelope(cancellation, operation)
        url = self.get_service_url("cancel")
        root = self._perform_request(url, envelope)

        self._validate_cancel_response(root)

        ack = root.find(".//apps:Acuse", self.namespaces)

        if operation == "accept_reject":
            acceptances = root.find(".//apps:aceptacion", self.namespaces)
            rejections = root.find(".//apps:rechazo", self.namespaces)
            folios = {}
            for a in acceptances:
                uuid = a.find(".//apps:uuid", self.namespaces).text
                status = a.find(".//apps:status", self.namespaces).text
                folios.update({uuid: {"status": status, "response": "Aceptacion"}})

            for r in rejections:
                uuid = r.find(".//apps:uuid", self.namespaces).text
                status = r.find(".//apps:status", self.namespaces).text
                folios.update({uuid: {"status": status, "response": "Rechazo"}})

            return AcceptRejectAcknowledgment(
                folios=folios,
                acuse=unescape(ack.text).encode() if ack is not None else None,
            )

        return CancelationAcknowledgment(
            code=root.find(".//apps:EstatusUUID", self.namespaces).text,
            acuse=unescape(ack.text).encode(),
        )

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
        return self._perform_stamp_operation(
            cfdi=cfdi, accept=accept, operation="issue"
        )

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

    def stamped(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        """Retrieves a previously stamped XML that failed to be retrieved in the first request.

        Args:
            cfdi (CFDI): The CFDI object to be checked.
            accept (Accept, optional): The type of response to accept. Defaults to Accept.XML.

        Raises:
            NotImplementedError: If the accept parameter includes Accept.PDF
            ResponseError: If the response from the Finkok SOAP web service contains an error code

        Returns:
            Document: The document with the following fields:
                - document_id (str): The UUID of the document.
                - xml (bytes): The XML content of the document.

        Notes:
            - This function currently only supports accepting XML responses.
            - If the accept parameter includes Accept.PDF, a NotImplementedError is raised.
        """
        return self._perform_stamp_operation(
            cfdi=cfdi, accept=accept, operation="stamped"
        )

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
        url = self.get_service_url("stamp")
        root = self._perform_request(url, envelope)

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

    def cancel(
        self,
        cfdi: CFDI,
        reason: CancelReason,
        substitution_id: str = None,
        signer: Signer = None,
    ) -> CancelationAcknowledgment:
        """Cancels a CFDI document using the Finkok API.

        Args:
            cfdi (CFDI): The CFDI document to be canceled.
            reason (CancelReason): The reason for canceling the CFDI document.
            substitution_id (str, optional): The ID of the substitution document. Defaults to None.
            signer (Signer): The signer of the CFDI document.

        Returns:
            CancelationAcknowledgment: The acknowledgment of the cancellation.

        Raises:
            ValueError: If the signer is not provided.
            DocumentNotFoundError: If the CFDI document to cancel is not found.
            ResponseError: If there is an error in the response from the API.
        """
        if signer is None:
            raise ValueError("signer is required")

        uuid = cfdi["Complemento"]["TimbreFiscalDigital"]["UUID"]
        folio = cancelacion.Folio(uuid, reason.value, substitution_id)
        return self.cancel_comprobante(cancelacion.Cancelacion(signer, folio))

    def cancel_comprobante(
        self, cancelation: cancelacion.Cancelacion
    ) -> CancelationAcknowledgment:
        """Operation to request the cancellation of a CFDI document using a Cancelacion object.

        Args:
            cancelation (cancelacion.Cancelacion): The cancelation object.

        Returns:
            CancelationAcknowledgment: The acknowledgment of the cancellation.

        Raises:
            DocumentNotFoundError: If the document is not found.
            ResponseError: If there is an error in the response.
        """
        return self._perform_cancel_operation(cancelation, "cancel")

    def accept_reject(
        self, request: SolicitudAceptacionRechazo
    ) -> AcceptRejectAcknowledgment:
        """Operation to Accept Reject a Cancellation Request

        Args:
            request (SolicitudAceptacionRechazo): The cancellation request.

        Returns:
            AcceptRejectAcknowledgment: The acknowledgment of the cancellation.

        Raises:
            ResponseError: If there is an error in the response.
        """
        return self._perform_cancel_operation(request, "accept_reject")

    def pending(self, rfc: str) -> list[str]:
        namespace = self.namespaces["cancel"]
        operation_element = etree.Element(etree.QName(namespace, "get_pending"))

        rtaxpayer_id = etree.SubElement(
            operation_element, etree.QName(namespace, "rtaxpayer_id")
        )
        rtaxpayer_id.text = rfc

        operation_element = self._add_auth(operation_element, namespace)
        envelope = self._build_envelope(operation_element)

        url = self.get_service_url("cancel")
        root = self._perform_request(url, envelope)

        return [uuid.text for uuid in root.find(".//apps:uuids", self.namespaces)]
