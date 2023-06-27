"""iedu http://www.sat.gob.mx/iedu"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class InstEducativas(CFDI):
    """
    Complemento concepto para la expedición de comprobantes fiscales por parte de Instituciones Educativas Privadas, para los efectos del artículo primero y cuarto del decreto por el que se otorga un estímulo fiscal a las personas físicas en relación con los pagos por servicios educativos
    
    :param nombre_alumno: Atributo requerido para indicar el nombre del Alumno
    :param curp: Atributo requerido para indicar la CURP del alumno de la institución educativa
    :param nivel_educativo: Atributo requerido para indicar el nivel educativo que cursa el alumno
    :param aut_rvoe: Atributo requerido para especificar la clave del centro de trabajo o el reconocimiento de validez oficial de estudios en los términos de la Ley General de Educación que tenga la institución educativa privada donde se realiza el pago.
    :param rfc_pago: Atributo opcional para indicar el RFC de quien realiza el pago cuando sea diferente a quien recibe el servicio
    """
    
    tag = '{http://www.sat.gob.mx/iedu}instEducativas'
    version = '1.0'
    
    def __init__(
            self,
            nombre_alumno: str,
            curp: str,
            nivel_educativo: str,
            aut_rvoe: str,
            rfc_pago: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'NombreAlumno': nombre_alumno,
            'CURP': curp,
            'NivelEducativo': nivel_educativo,
            'AutRVOE': aut_rvoe,
            'RfcPago': rfc_pago,
        })
        

