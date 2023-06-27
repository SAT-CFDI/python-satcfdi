"""tpe http://www.sat.gob.mx/TuristaPasajeroExtranjero"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class DatosTransito(ScalarMap):
    """
    Elemento requerido para expresar la información de la operación realizada
    
    :param via: Atributo requerido para expresar si es vía “Aérea”, “Marítima” o "Terrestre"
    :param tipo_id: Atributo requerido para la expresión del número de pasaporte.
    :param numero_id: Atributo requerido para expresar el número de identificación (pasaporte, visa, etc.)
    :param nacionalidad: Atributo requerido para expresar la nacionalidad del turista.
    :param empresa_transporte: Atributo requerido para señalar la empresa de transporte que lo ingresa a territorio nacional o lo traslada de salida.
    :param id_transporte: Atributo opcional para expresar el identificador del medio de transporte usado, ejemplo: número de vuelo.
    """
    
    def __init__(
            self,
            via: str,
            tipo_id: str,
            numero_id: str,
            nacionalidad: str,
            empresa_transporte: str,
            id_transporte: str = None,
    ): 
        super().__init__({
            'Via': via,
            'TipoId': tipo_id,
            'NumeroId': numero_id,
            'Nacionalidad': nacionalidad,
            'EmpresaTransporte': empresa_transporte,
            'IdTransporte': id_transporte,
        })
        

class TuristaPasajeroExtranjero(CFDI):
    """
    Complemento opcional al Comprobante Fiscal Digital (CFD) y Comprobante Fiscal Digital a través de Internet (CFDI) para el manejo de datos de TuristaPasajeroExtranjero.
    
    :param fechade_transito: Atributo requerido para expresar la fecha y hora del Arribo o Salida del medio de transporte utilizado. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.
    :param tipo_transito: Atributo requerido para incorporar la operación realizada: Arribo ó Salida.
    :param datos_transito: Elemento requerido para expresar la información de la operación realizada
    """
    
    tag = '{http://www.sat.gob.mx/TuristaPasajeroExtranjero}TuristaPasajeroExtranjero'
    version = '1.0'
    
    def __init__(
            self,
            fechade_transito: datetime,
            tipo_transito: str,
            datos_transito: DatosTransito | dict,
    ): 
        super().__init__({
            'Version': self.version,
            'FechadeTransito': fechade_transito,
            'TipoTransito': tipo_transito,
            'DatosTransito': datos_transito,
        })
        

