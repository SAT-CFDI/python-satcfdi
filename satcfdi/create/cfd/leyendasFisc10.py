"""leyendasFisc http://www.sat.gob.mx/leyendasFiscales"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Leyenda(ScalarMap):
    """
    Nodo para expresar la(s) leyenda(s) fiscal(es) que apliquen al comprobante
    
    :param texto_leyenda: Atributo requerido para especificar la leyenda fiscal
    :param disposicion_fiscal: Atributo opcional para especificar la Ley, Resolución o Disposición fiscal que regula la leyenda, deberá expresarse en siglas de mayúsculas y sin puntuación (p. ej: ISR)
    :param norma: Atributo opcional para especificar el número de Artículo o en su caso Regla que regula la obligación de la leyenda
    """
    
    def __init__(
            self,
            texto_leyenda: str,
            disposicion_fiscal: str = None,
            norma: str = None,
    ): 
        super().__init__({
            'TextoLeyenda': texto_leyenda,
            'DisposicionFiscal': disposicion_fiscal,
            'Norma': norma,
        })
        

class LeyendasFiscales(CFDI):
    """
    Nodo opcional para incluir leyendas previstas en disposiciones fiscales, distintas a las contenidas en el estándar de Comprobante Fiscal Digital (CFD) o Comprobante Fiscal Digital a través de Internet (CFDI).
    
    :param leyenda: Nodo para expresar la(s) leyenda(s) fiscal(es) que apliquen al comprobante
    """
    
    tag = '{http://www.sat.gob.mx/leyendasFiscales}LeyendasFiscales'
    version = '1.0'
    
    def __init__(
            self,
            leyenda: Leyenda | dict | Sequence[Leyenda | dict],
    ): 
        super().__init__({
            'Version': self.version,
            'Leyenda': leyenda,
        })
        

