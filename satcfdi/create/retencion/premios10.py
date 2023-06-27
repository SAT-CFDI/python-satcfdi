"""premios http://www.sat.gob.mx/esquemas/retencionpago/1/premios"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Premios(CFDI):
    """
    Complemento para expresar los premios obtenidos en un periodo o ejercicio
    
    :param entidad_federativa: Atributo requerido para expresar la entidad federativa en la que se paga el premio obtenido, conforme al catálogo.
    :param mont_tot_pago: Atributo requerido para expresar el importe del pago realizado por la obtención de un premio
    :param mont_tot_pago_grav: Atributo requerido para expresar el importe gravado en la obtención de un premio
    :param mont_tot_pago_exent: Atributo requerido para expresar el monto total exento en la obtención de un premio
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/premios}Premios'
    version = '1.0'
    
    def __init__(
            self,
            entidad_federativa: str,
            mont_tot_pago: Decimal | int,
            mont_tot_pago_grav: Decimal | int,
            mont_tot_pago_exent: Decimal | int,
    ): 
        super().__init__({
            'Version': self.version,
            'EntidadFederativa': entidad_federativa,
            'MontTotPago': mont_tot_pago,
            'MontTotPagoGrav': mont_tot_pago_grav,
            'MontTotPagoExent': mont_tot_pago_exent,
        })
        

