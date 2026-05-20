"""hidrocarburospetroliferos http://www.sat.gob.mx/hidrocarburospetroliferos"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class HidroYPetro(CFDI):
    """
    Complemento concepto para incorporar al Comprobante Fiscal Digital por Internet (CFDI) la información sobre los permisos otorgados por la autoridad competente referentes a operaciones de hidrocarburos y petrolíferos.
    
    :param tipo_permiso: Atributo requerido para registrar el tipo de permiso cuando éste haya sido otorgado por la autoridad competente.
    :param numero_permiso: Atributo requerido para registrar el número de permiso otorgado por la autoridad competente, de acuerdo con la nomenclatura de la columna “Nomenclatura del número de permiso” del catálogo c_TipoPermiso.
    :param clave_hyp: Atributo requerido para registrar la clave correspondiente a hidrocarburos y petrolíferos.
    :param sub_producto_hyp: Atributo requerido para registrar el subtipo del hidrocarburo y petrolífero.
    """
    
    tag = '{http://www.sat.gob.mx/hidrocarburospetroliferos}HidroYPetro'
    version = '1.0'
    
    def __init__(
            self,
            tipo_permiso: str,
            numero_permiso: str,
            clave_hyp: str,
            sub_producto_hyp: str,
    ): 
        super().__init__({
            'Version': self.version,
            'TipoPermiso': tipo_permiso,
            'NumeroPermiso': numero_permiso,
            'ClaveHYP': clave_hyp,
            'SubProductoHYP': sub_producto_hyp,
        })
        

