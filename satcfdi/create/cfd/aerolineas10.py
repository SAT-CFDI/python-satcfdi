"""aerolineas http://www.sat.gob.mx/aerolineas"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Cargo(ScalarMap):
    """
    Nodo para expresar la información detallada de un cargo.
    
    :param codigo_cargo: Atributo requerido para indicar el código del cargo según el catálogo de la IATA.
    :param importe: Atributo requerido para representar el importe del cargo.
    """
    
    def __init__(
            self,
            codigo_cargo: str,
            importe: Decimal | int,
    ): 
        super().__init__({
            'CodigoCargo': codigo_cargo,
            'Importe': importe,
        })
        

class OtrosCargos(ScalarMap):
    """
    Nodo opcional para expresar otros cargos aplicables
    
    :param total_cargos: Atributo requerido para expresar el total de los cargos adicionales que se están aplicando.
    :param cargo: Nodo para expresar la información detallada de un cargo.
    """
    
    def __init__(
            self,
            total_cargos: Decimal | int,
            cargo: Cargo | dict | Sequence[Cargo | dict],
    ): 
        super().__init__({
            'TotalCargos': total_cargos,
            'Cargo': cargo,
        })
        

class Aerolineas(CFDI):
    """
    Complemento al Comprobante Fiscal Digital a través de Internet (CFDI) para el manejo de datos de Aerolíneas para pasajeros.
    
    :param tua: Atributo requerido para indicar el importe del TUA aplicable al boleto.
    :param otros_cargos: Nodo opcional para expresar otros cargos aplicables
    """
    
    tag = '{http://www.sat.gob.mx/aerolineas}Aerolineas'
    version = '1.0'
    
    def __init__(
            self,
            tua: Decimal | int,
            otros_cargos: OtrosCargos | dict = None,
    ): 
        super().__init__({
            'Version': self.version,
            'TUA': tua,
            'OtrosCargos': otros_cargos,
        })
        

