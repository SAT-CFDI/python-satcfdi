"""registrofiscal http://www.sat.gob.mx/registrofiscal"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class CFDIRegistroFiscal(CFDI):
    """
    Complemento para incluir los datos de identificación de los CFDIs generados en Registro Fiscal.
    
    :param folio: Atributo requerido para expresar la relación del CFDI con el Registro Fiscal.
    """
    
    tag = '{http://www.sat.gob.mx/registrofiscal}CFDIRegistroFiscal'
    version = '1.0'
    
    def __init__(
            self,
            folio: str,
    ): 
        super().__init__({
            'Version': self.version,
            'Folio': folio,
        })
        

