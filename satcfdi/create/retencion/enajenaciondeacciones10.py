"""enajenaciondeacciones http://www.sat.gob.mx/esquemas/retencionpago/1/enajenaciondeacciones"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class EnajenaciondeAcciones(CFDI):
    """
    Complemento para expresar la enajenación de acciones u operaciones de valores (incluye ganancia o pérdida).
    
    :param contrato_intermediacion: Atributo requerido para expresar la descripción del contrato de intermediación
    :param ganancia: Atributo requerido para expresar la ganancia obtenida por la enajenación de acciones u operación de valores
    :param perdida: Atributo requerido para expresar la pérdida en el contrato de intermediación
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/enajenaciondeacciones}EnajenaciondeAcciones'
    version = '1.0'
    
    def __init__(
            self,
            contrato_intermediacion: str,
            ganancia: Decimal | int,
            perdida: Decimal | int,
    ): 
        super().__init__({
            'Version': self.version,
            'ContratoIntermediacion': contrato_intermediacion,
            'Ganancia': ganancia,
            'Perdida': perdida,
        })
        

