"""servicioparcial http://www.sat.gob.mx/servicioparcialconstruccion"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Inmueble(ScalarMap):
    """
    Nodo requerido para expresar la información del inmueble en el que se proporcionan los servicios parciales de construcción.
    
    :param calle: Este atributo requerido sirve para precisar la avenida, calle, camino o carretera del inmueble
    :param municipio: Atributo requerido que sirve para precisar el municipio o delegación (en el caso del Distrito Federal) en donde se da la ubicación del inmueble.
    :param estado: Entidad Federativa donde se ubica el inmueble conforme al catálogo publicado en el portal del SAT en Internet.
    :param codigo_postal: Atributo requerido que sirve para asentar el código postal en donde se da la ubicación del inmueble.
    :param no_exterior: Este atributo opcional sirve para expresar el número particular en donde se da la ubicación del inmueble en una calle dada.
    :param no_interior: Este atributo opcional sirve para expresar información adicional para especificar la ubicación cuando calle y número exterior (noExterior) no resulten suficientes para determinar la ubicación precisa del inmueble.
    :param colonia: Este atributo opcional sirve para precisar la colonia en donde se da la ubicación del inmueble cuando se desea ser más específico en casos de ubicaciones urbanas.
    :param localidad: Atributo opcional que sirve para precisar la ciudad o población donde se da la ubicación del inmueble.
    :param referencia: Atributo opcional para expresar una referencia adicional de ubicación del inmueble.
    """
    
    def __init__(
            self,
            calle: str,
            municipio: str,
            estado: str,
            codigo_postal: str,
            no_exterior: str = None,
            no_interior: str = None,
            colonia: str = None,
            localidad: str = None,
            referencia: str = None,
    ): 
        super().__init__({
            'Calle': calle,
            'Municipio': municipio,
            'Estado': estado,
            'CodigoPostal': codigo_postal,
            'NoExterior': no_exterior,
            'NoInterior': no_interior,
            'Colonia': colonia,
            'Localidad': localidad,
            'Referencia': referencia,
        })
        

class Parcialesconstruccion(CFDI):
    """
    Complemento para incorporar información de servicios parciales de construcción de inmuebles destinados a casa habitación.
    
    :param num_per_lico_aut: Atributo requerido para expresar el número de permiso, licencia o autorización de construcción proporcionado por el prestatario de los servicios parciales de construcción.
    :param inmueble: Nodo requerido para expresar la información del inmueble en el que se proporcionan los servicios parciales de construcción.
    """
    
    tag = '{http://www.sat.gob.mx/servicioparcialconstruccion}parcialesconstruccion'
    version = '1.0'
    
    def __init__(
            self,
            num_per_lico_aut: str,
            inmueble: Inmueble | dict,
    ): 
        super().__init__({
            'Version': self.version,
            'NumPerLicoAut': num_per_lico_aut,
            'Inmueble': inmueble,
        })
        

