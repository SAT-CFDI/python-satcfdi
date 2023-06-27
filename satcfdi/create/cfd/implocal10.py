"""implocal http://www.sat.gob.mx/implocal"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class TrasladosLocales(ScalarMap):
    """
    Nodo opcional para la expresión de los impuestos locales trasladados
    
    :param imp_loc_trasladado: Nombre del impuesto local trasladado
    :param tasa_de_traslado: Porcentaje de traslado del impuesto local
    :param importe: Monto del impuesto local trasladado
    """
    
    def __init__(
            self,
            imp_loc_trasladado: str,
            tasa_de_traslado: Decimal | int,
            importe: Decimal | int,
    ): 
        super().__init__({
            'ImpLocTrasladado': imp_loc_trasladado,
            'TasadeTraslado': tasa_de_traslado,
            'Importe': importe,
        })
        

class RetencionesLocales(ScalarMap):
    """
    Nodo opcional para la expresión de los impuestos locales retenidos
    
    :param imp_loc_retenido: Nombre del impuesto local retenido
    :param tasa_de_retencion: Porcentaje de retención del impuesto local
    :param importe: Monto del impuesto local retenido
    """
    
    def __init__(
            self,
            imp_loc_retenido: str,
            tasa_de_retencion: Decimal | int,
            importe: Decimal | int,
    ): 
        super().__init__({
            'ImpLocRetenido': imp_loc_retenido,
            'TasadeRetencion': tasa_de_retencion,
            'Importe': importe,
        })
        

class ImpuestosLocales(CFDI):
    """
    Complemento al Comprobante Fiscal Digital para Impuestos Locales
    
    :param total_de_retenciones: Atributo requerido para expresar la suma total de Retenciones aplicables
    :param total_de_traslados: Atributo requerido para expresar la suma total de traslados aplicables
    :param retenciones_locales: Nodo opcional para la expresión de los impuestos locales retenidos
    :param traslados_locales: Nodo opcional para la expresión de los impuestos locales trasladados
    """
    
    tag = '{http://www.sat.gob.mx/implocal}ImpuestosLocales'
    version = '1.0'
    
    def __init__(
            self,
            total_de_retenciones: Decimal | int,
            total_de_traslados: Decimal | int,
            retenciones_locales: RetencionesLocales | dict = None,
            traslados_locales: TrasladosLocales | dict = None,
    ): 
        super().__init__({
            'Version': self.version,
            'TotaldeRetenciones': total_de_retenciones,
            'TotaldeTraslados': total_de_traslados,
            'RetencionesLocales': retenciones_locales,
            'TrasladosLocales': traslados_locales,
        })
        

