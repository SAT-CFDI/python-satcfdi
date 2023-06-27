"""donat http://www.sat.gob.mx/donat"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Donatarias(CFDI):
    """
    Nodo opcional para incluir la información requerida por el Servicio de Administración Tributaria a las organizaciones civiles o fideicomisos autorizados para recibir donativos, que permite hacer deducibles los Comprobantes Fiscales Digitales (CFD) y Comprobantes Fiscales Digitales a través de Internet (CFDI) a los donantes.
    
    :param no_autorizacion: Atributo requerido para expresar el número del oficio en que se haya informado a la organización civil o fideicomiso, la procedencia de la autorización para recibir donativos deducibles, o su renovación correspondiente otorgada por el Servicio de Administración Tributaria.
    :param fecha_autorizacion: Atributo requerido para expresar la fecha del oficio en que se haya informado a la organización civil o fideicomiso, la procedencia de la autorización para recibir donativos deducibles, o su renovación correspondiente otorgada por el Servicio de Administración Tributaria.
    :param leyenda: Atributo requerido para señalar de manera expresa que el comprobante que se expide se deriva de un donativo.
    """
    
    tag = '{http://www.sat.gob.mx/donat}Donatarias'
    version = '1.1'
    
    def __init__(
            self,
            no_autorizacion: str,
            fecha_autorizacion: date,
            leyenda: str,
    ): 
        super().__init__({
            'Version': self.version,
            'NoAutorizacion': no_autorizacion,
            'FechaAutorizacion': fecha_autorizacion,
            'Leyenda': leyenda,
        })
        

