"""valesdedespensa http://www.sat.gob.mx/valesdedespensa"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Concepto(ScalarMap):
    """
    Nodo requerido para la expresión de una transacción a ser reportada por el proveedor del monedero electrónico de vales de despensa.
    
    :param identificador: Atributo requerido para expresar el identificador o numero del monedero electrónico.
    :param fecha: Atributo requerido para la expresión de la Fecha y hora de expedición de la operación reportada. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.
    :param rfc: Atributo requerido para la expresión del Registro Federal de Contribuyentes del trabajador al que se le otorgó el monedero electrónico sin guiones o espacios
    :param curp: Atributo requerido para la expresión de la CURP del trabajador al que se le otorgó el monedero electrónico.
    :param nombre: Atributo requerido para la expresión del Nombre del trabajador al que se le otorgó el monedero electrónico sin guiones o espacios
    :param importe: Atributo requerido para expresar el importe del depósito efectuado al trabajador en el monedero electrónico.
    :param num_seguridad_social: Atributo opcional para la expresión del numero de seguridad social aplicable al trabajador.
    """
    
    def __init__(
            self,
            identificador: str,
            fecha: datetime,
            rfc: str,
            curp: str,
            nombre: str,
            importe: Decimal | int,
            num_seguridad_social: str = None,
    ): 
        super().__init__({
            'Identificador': identificador,
            'Fecha': fecha,
            'Rfc': rfc,
            'Curp': curp,
            'Nombre': nombre,
            'Importe': importe,
            'NumSeguridadSocial': num_seguridad_social,
        })
        

class ValesDeDespensa(CFDI):
    """
    Complemento al Comprobante Fiscal Digital por Internet (CFDI) para integrar la información emitida por un prestador de servicios de monedero electrónico de vales de despensa.
    
    :param numero_de_cuenta: Atributo requerido para expresar el numero de cuenta del adquiriente del monedero electrónico.
    :param total: Atributo requerido para expresar el monto total de vales de despensa otorgados.
    :param conceptos: Nodo requerido para enlistar los conceptos cubiertos por los monederos electrónicos de vales de despensa.
    :param registro_patronal: Atributo opcional para expresar el registro patronal del adquirente del monedero electrónico.
    """
    
    tag = '{http://www.sat.gob.mx/valesdedespensa}ValesDeDespensa'
    version = '1.0'
    tipo_operacion = 'monedero electrónico'
    
    def __init__(
            self,
            numero_de_cuenta: str,
            total: Decimal | int,
            conceptos: Concepto | dict | Sequence[Concepto | dict],
            registro_patronal: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'TipoOperacion': self.tipo_operacion,
            'NumeroDeCuenta': numero_de_cuenta,
            'Total': total,
            'Conceptos': conceptos,
            'RegistroPatronal': registro_patronal,
        })
        

