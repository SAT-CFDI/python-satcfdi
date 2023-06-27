"""consumodecombustibles http://www.sat.gob.mx/consumodecombustibles"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Determinado(ScalarMap):
    """
    Nodo para la definición de información detallada de un impuesto específico
    
    :param impuesto: Atributo requerido para definir el tipo de impuesto
    :param tasa: Atributo requerido para señalar la tasa del impuesto por cada concepto amparado en el comprobante
    :param importe: Atributo requerido para definir el importe o monto del impuesto
    """
    
    def __init__(
            self,
            impuesto: str,
            tasa: Decimal | int,
            importe: Decimal | int,
    ): 
        super().__init__({
            'Impuesto': impuesto,
            'Tasa': tasa,
            'Importe': importe,
        })
        

class ConceptoConsumoDeCombustibles(ScalarMap):
    """
    Nodo requerido para la expresión de una transacción para operaciones de compra de combustibles.
    
    :param identificador: Atributo requerido para la expresión del identificador o número del monedero electrónico
    :param fecha: Atributo requerido para la expresión de la Fecha y hora de expedición de la operación reportada. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.
    :param rfc: Atributo requerido del RFC del enajenante del combustible
    :param clave_estacion: Atributo requerido para expresar la clave de cliente de la estación de servicio, a 10 caracteres, cuando sea requerido.
    :param cantidad: Atributo requerido para definir el volumen de combustible adquirido.
    :param nombre_combustible: Atributo requerido para expresar el nombre del combustible adquirido.
    :param folio_operacion: Atributo requerido para referir el número de folio de cada operación realizada por cada monedero electrónico.
    :param valor_unitario: Atributo requerido para definir el precio unitario del combustible adquirido.
    :param importe: Atributo requerido para definir el monto total de consumo de combustible. Debe ser equivalente al resultado de multiplicar la cantidad por el valor unitario.
    :param determinados: Nodo requerido para enlistar los impuestos determinados aplicables de combustibles.
    """
    
    def __init__(
            self,
            identificador: str,
            fecha: datetime,
            rfc: str,
            clave_estacion: str,
            cantidad: Decimal | int,
            nombre_combustible: str,
            folio_operacion: str,
            valor_unitario: Decimal | int,
            importe: Decimal | int,
            determinados: Determinado | dict | Sequence[Determinado | dict],
    ): 
        super().__init__({
            'Identificador': identificador,
            'Fecha': fecha,
            'Rfc': rfc,
            'ClaveEstacion': clave_estacion,
            'Cantidad': cantidad,
            'NombreCombustible': nombre_combustible,
            'FolioOperacion': folio_operacion,
            'ValorUnitario': valor_unitario,
            'Importe': importe,
            'Determinados': determinados,
        })
        

class ConsumoDeCombustibles(CFDI):
    """
    Complemento al Comprobante Fiscal Digital por Internet (CFDI) para integrar la información de consumo de combustibles por monedero electrónico.
    
    :param numero_de_cuenta: Nodo requerido para expresar el número de cuenta del adquirente del monedero electrónico
    :param total: Atributo requerido para expresar el monto total de consumo de combustibles.
    :param conceptos: Nodo requerido para enlistar los conceptos cubiertos por Consumo de Combustibles.
    :param sub_total: Atributo opcional para representar la suma de todos los importes tipo ConceptoConsumoDeCombustibles.
    """
    
    tag = '{http://www.sat.gob.mx/consumodecombustibles}ConsumoDeCombustibles'
    version = '1.0'
    tipo_operacion = 'monedero electrónico'
    
    def __init__(
            self,
            numero_de_cuenta: str,
            total: Decimal | int,
            conceptos: ConceptoConsumoDeCombustibles | dict | Sequence[ConceptoConsumoDeCombustibles | dict],
            sub_total: Decimal | int = None,
    ): 
        super().__init__({
            'Version': self.version,
            'TipoOperacion': self.tipo_operacion,
            'NumeroDeCuenta': numero_de_cuenta,
            'Total': total,
            'Conceptos': conceptos,
            'SubTotal': sub_total,
        })
        

