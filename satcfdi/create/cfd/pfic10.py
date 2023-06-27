"""pfic http://www.sat.gob.mx/pfic"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class PFintegranteCoordinado(CFDI):
    """
    Este complemento permite incorporar a un Comprobante Fiscal Digital (CFD) o a un Comprobante Fiscal Digital a través de Internet (CFDI) los datos de identificación del vehículo que corresponda a personas físicas integrantes de coordinados, que opten por pagar el impuesto individualmente de conformidad con lo establecido por el artículo 83, séptimo párrafo de la Ley del Impuesto sobre la Renta.
    
    :param clave_vehicular: Atributo requerido para precisar Clave vehicular que corresponda a la versión del vehículo enajenado.
    :param placa: Atributo requerido para señalar la placa o número de folio del permiso del vehículo que corresponda.
    :param rfc_pf: Atributo opcional para precisar el RFC de la persona física integrante de coordinados, que opte por pagar el impuesto individualmente.
    """
    
    tag = '{http://www.sat.gob.mx/pfic}PFintegranteCoordinado'
    version = '1.0'
    
    def __init__(
            self,
            clave_vehicular: str,
            placa: str,
            rfc_pf: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'ClaveVehicular': clave_vehicular,
            'Placa': placa,
            'RFCPF': rfc_pf,
        })
        

