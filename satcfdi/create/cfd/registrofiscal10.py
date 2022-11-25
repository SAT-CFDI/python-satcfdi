from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI, XElement


class CFDIRegistroFiscal(CFDI):
    """
    Complemento para incluir los datos de identificación de los CFDIs generados en Registro Fiscal.
    """
    tag = '{http://www.sat.gob.mx/registrofiscal}CFDIRegistroFiscal'
    version = '1.0'
    
    def __init__(
            self,
            folio: str,
    ): 
        """
        Complemento para incluir los datos de identificación de los CFDIs generados en Registro Fiscal.
        
        :param folio: Atributo requerido para expresar la relación del CFDI con el Registro Fiscal.
        """
        
        super().__init__({
            'Version': self.version,
            'Folio': folio,
        })
        

