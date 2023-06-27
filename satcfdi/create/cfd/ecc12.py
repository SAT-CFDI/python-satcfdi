"""ecc12 http://www.sat.gob.mx/EstadoDeCuentaCombustible12"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Traslado(ScalarMap):
    """
    Nodo para la definición de información detallada de un traslado de impuesto específico.
    
    :param impuesto: Atributo requerido para definir el tipo de impuesto trasladado.
    :param tasa_o_cuota: Atributo requerido para señalar la tasa o la cuota del impuesto que se traslada por cada concepto amparado en el comprobante. Cuando se registre un porcentaje, por ejemplo 16%, debe expresarse como 0.16 y no como 16.00
    :param importe: Atributo requerido para definir el importe o monto del impuesto trasladado.
    """
    
    def __init__(
            self,
            impuesto: str,
            tasa_o_cuota: Decimal | int,
            importe: Decimal | int,
    ): 
        super().__init__({
            'Impuesto': impuesto,
            'TasaOCuota': tasa_o_cuota,
            'Importe': importe,
        })
        

class ConceptoEstadoDeCuentaCombustible(ScalarMap):
    """
    Nodo requerido para la expresión de una transacción a ser reportada en el estado de cuenta del proveedor de monedero electrónico para operaciones de compra de combustibles.
    
    :param identificador: Atributo requerido para la expresión del identificador o número del monedero electrónico.
    :param fecha: Atributo requerido para la expresión de la Fecha y hora de expedición de la operación reportada. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.
    :param rfc: Atributo requerido del RFC del enajenante del combustible.
    :param clave_estacion: Atributo requerido para expresar la clave de cliente de la estación de servicio, a 10 caracteres.
    :param cantidad: Atributo requerido para definir el volumen de combustible adquirido.
    :param tipo_combustible: Atributo requerido para indicar la clave del tipo de combustible.
    :param nombre_combustible: Atributo requerido para expresar el nombre del combustible adquirido.
    :param folio_operacion: Atributo requerido para referir el número de folio de cada operación realizada por cada monedero electrónico.
    :param valor_unitario: Atributo requerido para definir el precio unitario del combustible adquirido.
    :param importe: Atributo requerido para definir el monto total de consumo de combustible. Debe ser equivalente al resultado de multiplicar la cantidad por el valor unitario, redondeado a centésimas.
    :param traslados: Nodo requerido para enlistar los impuestos trasladados aplicables de combustibles.
    :param unidad: Atributo condicional para precisar la unidad de medida.
    """
    
    def __init__(
            self,
            identificador: str,
            fecha: datetime,
            rfc: str,
            clave_estacion: str,
            cantidad: Decimal | int,
            tipo_combustible: str,
            nombre_combustible: str,
            folio_operacion: str,
            valor_unitario: Decimal | int,
            importe: Decimal | int,
            traslados: Traslado | dict | Sequence[Traslado | dict],
            unidad: str = None,
    ): 
        super().__init__({
            'Identificador': identificador,
            'Fecha': fecha,
            'Rfc': rfc,
            'ClaveEstacion': clave_estacion,
            'Cantidad': cantidad,
            'TipoCombustible': tipo_combustible,
            'NombreCombustible': nombre_combustible,
            'FolioOperacion': folio_operacion,
            'ValorUnitario': valor_unitario,
            'Importe': importe,
            'Traslados': traslados,
            'Unidad': unidad,
        })
        

class EstadoDeCuentaCombustible(CFDI):
    """
    Complemento para el Comprobante Fiscal Digital por Internet (CFDI) para integrar la información aplicable al estado de cuenta emitido por un prestador de servicios de monedero electrónico
    
    :param numero_de_cuenta: Atributo requerido para expresar el número de cuenta del adquirente del monedero electrónico
    :param sub_total: Atributo requerido para representar la suma de todos los importes tipo ConceptoEstadoDeCuentaCombustible.
    :param total: Atributo requerido para expresar el monto total de consumo de combustible.
    :param conceptos: Nodo requerido para enlistar los conceptos cubiertos por Estado de Cuenta de Combustible.
    """
    
    tag = '{http://www.sat.gob.mx/EstadoDeCuentaCombustible12}EstadoDeCuentaCombustible'
    version = '1.2'
    tipo_operacion = 'Tarjeta'
    
    def __init__(
            self,
            numero_de_cuenta: str,
            sub_total: Decimal | int,
            total: Decimal | int,
            conceptos: ConceptoEstadoDeCuentaCombustible | dict | Sequence[ConceptoEstadoDeCuentaCombustible | dict],
    ): 
        super().__init__({
            'Version': self.version,
            'TipoOperacion': self.tipo_operacion,
            'NumeroDeCuenta': numero_de_cuenta,
            'SubTotal': sub_total,
            'Total': total,
            'Conceptos': conceptos,
        })
        

