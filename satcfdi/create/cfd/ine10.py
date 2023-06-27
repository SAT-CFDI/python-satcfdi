"""ine http://www.sat.gob.mx/ine"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Entidad(ScalarMap):
    """
    Nodo condicional para expresar los datos correspondientes a las entidades federativas en las que se va a aplicar el gasto.
    
    :param clave_entidad: Atributo requerido para registrar la clave de la entidad a la que aplica el gasto.
    :param ambito: Atributo condicional para registrar el tipo de ámbito de un proceso de tipo Campaña o Precampaña. este atributo no se debe registrar para los procesos de tipo Ordinario.
    :param contabilidad: Nodo para expresar la clave de contabilidad de aspirantes precandidatos, candidatos y concentradoras.
    """
    
    def __init__(
            self,
            clave_entidad: str,
            ambito: str = None,
            contabilidad: int | Sequence[int] = None,
    ): 
        super().__init__({
            'ClaveEntidad': clave_entidad,
            'Ambito': ambito,
            'Contabilidad': contabilidad,
        })
        

class INE(CFDI):
    """
    Complemento al Comprobante Fiscal Digital por Internet (CFDI) para incluir los datos que identifiquen el tipo de proceso al que van dirigidos los gastos que realizan los partidos o las Asociaciones Civiles.
    
    :param tipo_proceso: Atributo requerido para expresar el tipo de proceso de que se trate.
    :param tipo_comite: Atributo condicional para expresar el tipo de comité de que se trate.
    :param id_contabilidad: Atributo opcional para registrar la clave de contabilidad de aspirantes precandidatos, candidatos y concentradoras, si se trata de un tipo de proceso ordinario y un comité ejecutivo nacional.Para los otros casos, la clave de contabilidad se registra en el atributo ine:Entidad:Contabilidad:IdContabilidad.
    :param entidad: Nodo condicional para expresar los datos correspondientes a las entidades federativas en las que se va a aplicar el gasto.
    """
    
    tag = '{http://www.sat.gob.mx/ine}INE'
    version = '1.0'
    
    def __init__(
            self,
            tipo_proceso: str,
            tipo_comite: str = None,
            id_contabilidad: int = None,
            entidad: Entidad | dict | Sequence[Entidad | dict] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'TipoProceso': tipo_proceso,
            'TipoComite': tipo_comite,
            'IdContabilidad': id_contabilidad,
            'Entidad': entidad,
        })
        

