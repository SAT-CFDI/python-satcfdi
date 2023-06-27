"""intereses http://www.sat.gob.mx/esquemas/retencionpago/1/intereses"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Intereses(CFDI):
    """
    Complemento para expresar los intereses obtenidos por rendimiento en inversiones
    
    :param sist_financiero: Atributo requerido para expresar si los interés obtenidos en el periodo o ejercicio provienen del sistema financiero
    :param retiro_aoresret_int: Atributo requerido para expresar si los intereses obtenidos fueron retirados en el periodo o ejercicio
    :param oper_financ_derivad: Atributo requerido para expresar si los intereses obtenidos corresponden a operaciones financieras derivadas.
    :param mont_int_nominal: Atributo requerido para expresar el importe del interés Nóminal obtenido en un periodo o ejercicio
    :param mont_int_real: Atributo requerido para expresar el monto de los intereses reales (diferencia que se obtiene restando al tipo de interés nominal y la tasa de inflación del periodo o ejercicio )
    :param perdida: Atributo requerido para expresar la pérdida por los intereses obtenidos en el periodo o ejercicio
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/intereses}Intereses'
    version = '1.0'
    
    def __init__(
            self,
            sist_financiero: str,
            retiro_aoresret_int: str,
            oper_financ_derivad: str,
            mont_int_nominal: Decimal | int,
            mont_int_real: Decimal | int,
            perdida: Decimal | int,
    ): 
        super().__init__({
            'Version': self.version,
            'SistFinanciero': sist_financiero,
            'RetiroAORESRetInt': retiro_aoresret_int,
            'OperFinancDerivad': oper_financ_derivad,
            'MontIntNominal': mont_int_nominal,
            'MontIntReal': mont_int_real,
            'Perdida': perdida,
        })
        

