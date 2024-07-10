from dataclasses import dataclass
from enum import Flag, auto, Enum
from ..cfdi import CFDI
from ..models import Signer
from ..create.cancela import cancelacion
from ..create.cancela import cancelacionretencion
from ..create.cancela.aceptacionrechazo import SolicitudAceptacionRechazo

__all__ = [
    'PAC',
    'Accept',
    'Document',
    'CancelationAcknowledgment',
    'AcceptRejectAcknowledgment',
    'CancelReason',
    'TaxpayerStatus',
    'Environment'
]


class Accept(Flag):
    NOTHING = 0
    XML = auto()
    PDF = auto()
    XML_PDF = XML | PDF


@dataclass(init=True)
class Document:
    document_id: str
    xml: bytes = None
    pdf: bytes = None

    @property
    def cfdi(self) -> CFDI:
        return CFDI.from_string(self.xml)


@dataclass(init=True)
class CancelationAcknowledgment:
    code: str | dict
    acuse: bytes = None


@dataclass(init=True)
class AcceptRejectAcknowledgment:
    folios: dict
    acuse: bytes = None


def _enum_value(val):
    if isinstance(val, Enum):
        return val.value
    return val


class CancelReason(Enum):
    COMPROBANTE_EMITIDO_CON_ERRORES_CON_RELACION = "01"
    """
    -- Comprobante emitido con errores con relación --
    
    Este supuesto aplica cuando la factura generada contiene un error en
    la clave del producto, valor unitario, descuento o cualquier otro dato, por lo que se
    debe reexpedir. En este caso, primero se sustituye la factura y cuando se solicita la
    cancelación, se incorpora el folio de la factura que sustituye a la cancelada.

    ¿Qué debo hacer si uso el motivo de cancelación “01” Comprobantes emitidos con
    errores con relación y el comprobante no se cancela o presenta error?

    Se podrá utilizar la clave 02 para realizar la cancelación de los CFDI
    relacionados incluyendo el que sustituye al CFDI a cancelar, esto con la finalidad de
    que no se genere un estatus de “No cancelable”

    En los casos en los que subsista la operación, se deberá emitir un nuevo comprobante
    con la información correcta y la clave de tipo relación 04 sustitución de CFDI previos
    relacionando el folio fiscal del comprobante que se sustituye    
    """

    COMPROBANTE_EMITIDO_CON_ERRORES_SIN_RELACION = "02"
    """
    -- Comprobante emitido con errores sin relación --
    
    Este supuesto aplica cuando la factura generada contiene un error en
    la clave del producto, valor unitario, descuento o cualquier otro dato y no se requiera
    relacionar con otra factura generada.
    """

    NO_SE_LLEVO_A_CABO_LA_OPERACION = "03"
    """
    -- No se llevó a cabo la operación --
    
    Este supuesto aplica cuando se facturó una operación que no se
    concreta.
    """
    OPERACION_NORMATIVA_RELACIONADA_EN_LA_FACTURA_GLOBAL = "04"
    """
    -- Operación nominativa relacionada en la factura global --
    
    Este supuesto aplica cuando se incluye una venta en la factura global
    de operaciones con el público en general y posterior a ello, el cliente solicita su factura
    nominativa, lo que conlleva a cancelar la factura global y reexpedirla, así como
    generar la factura nominativa al cliente.
    """


class TaxpayerStatus(Enum):
    PRESUNTO = 'Presunto'
    """
    PRESUNTO: Cuando la autoridad fiscal detecta que un contribuyente ha estado emitiendo comprobantes de manera irregular,
    se presumirá la inexistencia de las operaciones amparadas en tales comprobantes.

    En este supuesto, procederá a notificar a los contribuyentes que se encuentren en dicha situación a través de su buzón
    tributario, de la página de internet del Servicio de Administración Tributaria, así como mediante una publicación en el
    Diario Oficial de la Federación.
    """

    SENTENCIA_FAVORABLE = 'Sentencia Favorable'
    """
    SENTENCIA FAVORABLE: El contribuyente tiene treinta días para acreditar que efectivamente sus operaciones son reales, si 
    logra corregir su situación se publica este estado.
    """

    DEFINITIVO = 'Definitivo'
    """
    DEFINITIVO: Si el contribuyente no atiende el llamado de la autoridad en quince días a partir de la última de las
    notificaciones o el contribuyente no pueda desvirtuar la existencia de sus operaciones se publica este estado.
    """

    DESVIRTUADO = 'Desvirtuado'
    """
    DESVIRTUADO: Cuando el contribuyente aporte a la autoridad fiscal la documentación e información que consideren 
    pertinentes para desvirtuar los hechos que llevaron a notificarlos con un plazo de quince días contados a partir de la
    última de las notificaciones que se hayan efectuado.
    """


class Environment(Enum):
    PRODUCTION = auto()
    TEST = auto()


class PAC:
    RFC = None

    def __init__(self, environment: Environment):
        self.environment = environment

    def status(self, cfdi: CFDI) -> dict:
        """
        Consulta el estado de un CFDI
        :return: Respuesta de la consulta
        """
        raise NotImplementedError()

    def validate(self, cfdi: CFDI):
        raise NotImplementedError()

    def issue(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        """
        Operation to request CFDI be sealed and stamped by PAC
        :param accept:
        :param cfdi:
        :return:
        """
        raise NotImplementedError()

    def stamp(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        """
        Operation to request sealed CFDI be stamped by PAC
        :param accept:
        :param cfdi:
        :return:
        document_id and bytes of stamped xml
        """
        raise NotImplementedError()

    def recover(self, document_id: str, accept: Accept = Accept.XML) -> Document:
        """

        :param accept:
        :param document_id:
        :return:
        """
        raise NotImplementedError()

    def cancel(self, cfdi: CFDI, reason: CancelReason, substitution_id: str = None, signer: Signer = None) -> CancelationAcknowledgment:
        """
        Operation to request single cfdi to be canceled
        :param signer:
        :param cfdi:
        :param substitution_id:
        :param reason:
        :return:
        """
        raise NotImplementedError()

    def cancel_comprobante(self, cancelation: cancelacion.Cancelacion) -> CancelationAcknowledgment:
        """
        Operation to Cancel a Comprobante
        """
        raise NotImplementedError()

    def cancel_retencion(self, cancelation: cancelacionretencion.Cancelacion) -> CancelationAcknowledgment:
        """
        Operation to Cancel a Retencion
        """
        raise NotImplementedError()

    def accept_reject(self, request: SolicitudAceptacionRechazo) -> AcceptRejectAcknowledgment:
        """
        Operation to Accept Reject a Cancellation Request
        """
        raise NotImplementedError()

    def pending(self, rfc: str) -> list[str]:
        """
        Operation to get pending cancellations
        """
        raise NotImplementedError()

    def list_69b(self, rfc: str) -> TaxpayerStatus | None:
        """
        Operation to get list69b status
        """
        raise NotImplementedError()
