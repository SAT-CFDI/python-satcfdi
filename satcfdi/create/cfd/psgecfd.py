"""psgecfd http://www.sat.gob.mx/psgecfd"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class PrestadoresDeServiciosDeCFD(CFDI):
    """
    Complemento requerido para los Proveedores de Servicio de generación y envío de Comprobantes Fiscales Digitales.
    
    :param nombre: Atributo requerido para el nombre o razón social del proveedor de servicios autorizado que generó y envió el comprobante fiscal digital.
    :param rfc: Atributo requerido para el Registro Federal de Contribuyentes del proveedor de servicios de generación y envío de comprobantes fiscales digitales.
    :param no_certificado: Atributo requerido para expresar el número de serie del certificado de sello digital del proveedor del servicio autorizado que generó y envió el comprobante fiscal digital.
    :param fecha_autorizacion: Atributo requerido para la expresión de la fecha y hora de autorización del proveedor del servicio que generó y envió el comprobante fiscal digital. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.
    :param no_autorizacion: Atributo requerido para precisar el número de autorización del proveedor del servicio de generación y envío comprobantes autorizado por el SAT.
    :param sello_del_psgecfd: Atributo requerido para contener el sello digital del proveedor del servicio de generación y envío de comprobantes fiscales digitales que generó y emitió el comprobante fiscal digital. El sello deberá ser expresado cómo una cadena de texto en formato Base 64.
    """
    
    tag = '{http://www.sat.gob.mx/psgecfd}PrestadoresDeServiciosDeCFD'
    
    def __init__(
            self,
            nombre: str,
            rfc: str,
            no_certificado: str,
            fecha_autorizacion: datetime,
            no_autorizacion: int,
            sello_del_psgecfd: str,
    ): 
        super().__init__({
            'Nombre': nombre,
            'Rfc': rfc,
            'NoCertificado': no_certificado,
            'FechaAutorizacion': fecha_autorizacion,
            'NoAutorizacion': no_autorizacion,
            'SelloDelPSGECFD': sello_del_psgecfd,
        })
        

