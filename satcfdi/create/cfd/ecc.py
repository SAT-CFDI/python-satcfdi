"""ecc http://www.sat.gob.mx/ecc"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Traslado(ScalarMap):
    """
    Nodo para la definición de información detallada de un traslado de impuesto específico
    
    :param impuesto: Atributo requerido para definir el tipo de impuesto trasladado
    :param tasa: Atributo requerido para señalar la tasa del impuesto que se traslada por cada concepto amparado en el comprobante
    :param importe: Atributo requerido para definir el importe o monto del impuesto trasladado
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
        

class ConceptoEstadoDeCuentaCombustible(ScalarMap):
    """
    Nodo requerido para la expresión de una transacción a ser reportada en el estado de cuenta del proveedor de monedero electrónico para operaciones de compra de combustibles.
    
    :param identificador: Atributo requerido para la expresión del identificador o número del monedero electrónico
    :param fecha: Atributo requerido para la expresión de la Fecha y hora de expedición de la operación reportada. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.
    :param rfc: Atributo requerido del RFC del enajenante del combustible
    :param clave_estacion: Atributo requerido para expresar la clave de cliente de la estación de servicio, a 10 caracteres, cuando sea requerido.
    :param cantidad: Atributo requerido para definir el volumen de combustible adquirido.
    :param nombre_combustible: Atributo requerido para expresar el nombre del combustible adquirido.
    :param folio_operacion: Atributo requerido para referir el número de folio de cada operación realizada por cada monedero electrónico.
    :param valor_unitario: Atributo requerido para definir el precio unitario del combustible adquirido.
    :param importe: Atributo requerido para definir el monto total de consumo de combustible. Debe ser equivalente al resultado de multiplicar la cantidad por el valor unitario.
    :param traslados: Nodo requerido para enlistar los impuestos trasladados aplicables de combustibles.
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
            traslados: Traslado | dict | Sequence[Traslado | dict],
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
            'Traslados': traslados,
        })
        

class EstadoDeCuentaCombustible(CFDI):
    """
    Complemento al Comprobante Fiscal Digital (CFD) y Comprobante Fiscal Digital por Internet (CFDI) para integrar la información aplicable al estado de cuenta emitido por un prestador de servicios de monedero electrónico.
    
    :param numero_de_cuenta: Nodo requerido para expresar el número de cuenta del adquirente del monedero electrónico
    :param total: Atributo requerido para expresar el monto total de consumo de combustible.
    :param conceptos: Nodo requerido para enlistar los conceptos cubiertos por Estado de Cuenta de Combustible.
    :param sub_total: Atributo opcional para representar la suma de todos los importes tipo ConceptoEstadoDeCuentaCombustible.
    """
    
    tag = '{http://www.sat.gob.mx/ecc}EstadoDeCuentaCombustible'
    tipo_operacion = 'Tarjeta'
    
    def __init__(
            self,
            numero_de_cuenta: str,
            total: Decimal | int,
            conceptos: ConceptoEstadoDeCuentaCombustible | dict | Sequence[ConceptoEstadoDeCuentaCombustible | dict],
            sub_total: Decimal | int = None,
    ): 
        super().__init__({
            'TipoOperacion': self.tipo_operacion,
            'NumeroDeCuenta': numero_de_cuenta,
            'Total': total,
            'Conceptos': conceptos,
            'SubTotal': sub_total,
        })
        

