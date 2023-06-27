"""ecb http://www.sat.gob.mx/ecb"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class MovimientoECBFiscal(ScalarMap):
    """
    Nodo requerido para expresar las operaciones a ser detalladas en el estado de cuenta bancario con RFC con efecto fiscal.
    
    :param fecha: Atributo requerido únicamente para la expresión de la fecha (mes/día) de la operación realizada por el cuentahabiente.
    :param descripcion: Atributo requerido para precisar la descripción del bien o servicio cubierto por el cargo a la cuenta bancaria.
    :param rfc_enajenante: Atributo requerido para indicar el RFC del enajenante, sin el cual no se puede acreditar la compra de bienes o servicios por medio del estado de cuenta bancario.
    :param importe: Atributo requerido para indicar el importe de la operación realizada por el cuentahabiente por medio del instrumento bancario.
    :param referencia: Atributo opcional para indicar el número de referencia o autorización con el que se identifica la operación realizada por el cuentahabiente.
    :param moneda: Atributo opcional para indicar en que moneda se realizó la operación. Si no se especifica dato alguno, se entenderá que el importe está expresado en moneda nacional.
    :param saldo_inicial: Atributo opcional para indicar el saldo inicial del instrumento bancario del cuentahabiente.
    :param saldo_al_corte: Atributo opcional para indicar el saldo al corte del instrumento bancario del cuentahabiente.
    """
    
    def __init__(
            self,
            fecha: datetime,
            descripcion: str,
            rfc_enajenante: str,
            importe: Decimal | int,
            referencia: str = None,
            moneda: str = None,
            saldo_inicial: Decimal | int = None,
            saldo_al_corte: Decimal | int = None,
    ): 
        super().__init__({
            'Fecha': fecha,
            'Descripcion': descripcion,
            'RFCenajenante': rfc_enajenante,
            'Importe': importe,
            'Referencia': referencia,
            'Moneda': moneda,
            'SaldoInicial': saldo_inicial,
            'SaldoAlCorte': saldo_al_corte,
        })
        

class MovimientoECB(ScalarMap):
    """
    Nodo requerido para expresar las operaciones a ser detalladas en el estado de cuenta bancario que no cuentan con un RFC
    
    :param fecha: Atributo requerido únicamente para la expresión de la fecha (mes/día) de la operación realizada por el cuentahabiente.
    :param descripcion: Atributo requerido para precisar la descripción del bien o servicio cubierto por el cargo a la cuenta bancaria.
    :param importe: Atributo requerido para indicar el importe de la operación realizada por el cuentahabiente por medio del instrumento bancario.
    :param referencia: Atributo opcional para indicar el número de referencia o autorización con el que se identifica la operación realizada por el cuentahabiente.
    :param moneda: Atributo opcional para indicar en que moneda se realizó la operación. Si no se especifica dato alguno, se entenderá que el importe está expresado en moneda nacional.
    :param saldo_inicial: Atributo opcional para indicar el saldo inicial del instrumento bancario del cuentahabiente.
    :param saldo_al_corte: Atributo opcional para indicar el saldo al corte del instrumento bancario del cuentahabiente.
    """
    
    def __init__(
            self,
            fecha: datetime,
            descripcion: str,
            importe: Decimal | int,
            referencia: str = None,
            moneda: str = None,
            saldo_inicial: Decimal | int = None,
            saldo_al_corte: Decimal | int = None,
    ): 
        super().__init__({
            'Fecha': fecha,
            'Descripcion': descripcion,
            'Importe': importe,
            'Referencia': referencia,
            'Moneda': moneda,
            'SaldoInicial': saldo_inicial,
            'SaldoAlCorte': saldo_al_corte,
        })
        

class Movimientos(ScalarMap):
    """
    Nodo requerido para enlistar los conceptos cubiertos por Estado de Cuenta Bancario.
    
    :param movimiento_ecb: Nodo requerido para expresar las operaciones a ser detalladas en el estado de cuenta bancario que no cuentan con un RFC
    :param movimiento_ecbfiscal: Nodo requerido para expresar las operaciones a ser detalladas en el estado de cuenta bancario con RFC con efecto fiscal.
    """
    
    def __init__(
            self,
            movimiento_ecb: MovimientoECB | dict = None,
            movimiento_ecbfiscal: MovimientoECBFiscal | dict = None,
    ): 
        super().__init__({
            'MovimientoECB': movimiento_ecb,
            'MovimientoECBFiscal': movimiento_ecbfiscal,
        })
        

class EstadoDeCuentaBancario(CFDI):
    """
    Complemento al Comprobante Fiscal Digital (CFD) y Comprobante Fiscal Digital a través de Internet (CFDI) para integrar información aplicable al estado de cuenta bancario.
    
    :param numero_cuenta: Atributo requerido para indicar el número de cuenta del producto bancario.
    :param nombre_cliente: Atributo requerido para indicar el nombre del cuentahabiente de la institución bancaria.
    :param periodo: Atributo requerido para indicar periodo de los cargos o abonos al instrumento bancario.
    :param movimientos: Nodo requerido para enlistar los conceptos cubiertos por Estado de Cuenta Bancario.
    :param sucursal: Atributo opcional para indicar la sucursal a la cual pertenece el cuentahabiente.
    """
    
    tag = '{http://www.sat.gob.mx/ecb}EstadoDeCuentaBancario'
    version = '1.0'
    
    def __init__(
            self,
            numero_cuenta: int,
            nombre_cliente: str,
            periodo: str,
            movimientos: Movimientos | dict,
            sucursal: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'NumeroCuenta': numero_cuenta,
            'NombreCliente': nombre_cliente,
            'Periodo': periodo,
            'Movimientos': movimientos,
            'Sucursal': sucursal,
        })
        

