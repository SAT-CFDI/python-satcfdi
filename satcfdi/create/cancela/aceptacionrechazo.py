from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence

from ..w3.signature import signature_c14n_sha1
from ... import Signer
from ...cfdi import CFDI, XElement


class Folios(XElement):
    def __init__(
            self,
            respuesta: str,
            uuid: str = None,
    ): 
        """
        
        :param respuesta: 
        :param uuid: 
        """
        
        super().__init__({
            'Respuesta': respuesta,
            'UUID': uuid,
        })
        

class SolicitudAceptacionRechazo(XElement):
    """
    Elemento raíz para realizar la aceptacion o rechazo de una solicitud de cancelacion.
    """
    tag = '{http://cancelacfd.sat.gob.mx}SolicitudAceptacionRechazo'
    
    def __init__(
            self,
            rfc_receptor: Signer = None,
            rfc_pac_envia_solicitud: str = None,
            folios: Folios | Sequence[Folios | dict] = None,
            fecha: datetime = None,
    ):
        """
        Elemento raíz para realizar la aceptacion o rechazo de una solicitud de cancelacion.
        
        :param fecha:
        :param rfc_receptor: 
        :param rfc_pac_envia_solicitud: 
        :param folios: 
        :return: objeto CFDI
        """

        super().__init__({
            'Fecha': fecha or datetime.now(),
            'RfcReceptor': rfc_receptor.rfc,
            'RfcPacEnviaSolicitud': rfc_pac_envia_solicitud,
            'Folios': folios,
        })
        self["_nsmap"] = {
            None: "http://cancelacfd.sat.gob.mx",
            "xsd": "http://www.w3.org/2001/XMLSchema",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }

        sig = signature_c14n_sha1(
            signer=rfc_receptor,
            element=self.to_xml(),
            nsmap={
                None: 'http://www.w3.org/2000/09/xmldsig#',
                "xsd": "http://www.w3.org/2001/XMLSchema",
                "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            }
        )
        self['Signature'] = sig





