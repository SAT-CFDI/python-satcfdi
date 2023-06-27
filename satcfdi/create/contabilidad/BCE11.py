"""BCE www.sat.gob.mx/esquemas/ContabilidadE/1_1/BalanzaComprobacion"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Ctas(ScalarMap):
    """
    Nodo obligatorio para expresar el detalle de cada cuenta o subcuenta de la balanza de comprobación.
    
    :param num_cta: Atributo requerido para expresar la clave asignada con que se distingue la cuenta o subcuenta en el catálogo de cuentas del contribuyente.
    :param saldo_ini: Atributo requerido para expresar el monto del saldo inicial de la cuenta o subcuenta en el periodo. De acuerdo a la naturaleza de la cuenta o subcuenta, deberá de corresponder el saldo inicial, de lo contrario se entenderá que es un saldo inicial de naturaleza inversa. En caso de no existir dato, colocar cero (0)
    :param debe: Atributo requerido para expresar el monto de los movimientos deudores de la cuenta o subcuenta. En caso de no existir dato, colocar cero (0)
    :param haber: Atributo requerido para expresar el monto de los movimientos acreedores de la cuenta o subcuenta. En caso de no existir dato, colocar cero (0)
    :param saldo_fin: Atributo requerido para expresar el monto del saldo final de la cuenta o subcuenta en el periodo. De acuerdo a la naturaleza de la cuenta o subcuenta, deberá de corresponder el saldo final, de lo contrario se entenderá que es un saldo final de naturaleza inversa. En caso de no existir dato, colocar cero (0)
    """
    
    def __init__(
            self,
            num_cta: str,
            saldo_ini: Decimal | int,
            debe: Decimal | int,
            haber: Decimal | int,
            saldo_fin: Decimal | int,
    ): 
        super().__init__({
            'NumCta': num_cta,
            'SaldoIni': saldo_ini,
            'Debe': debe,
            'Haber': haber,
            'SaldoFin': saldo_fin,
        })
        

class Balanza(CFDI):
    """
    Estándar de balanza de comprobación que se entrega como parte de la contabilidad electrónica.
    
    :param rfc: Atributo requerido para expresar el RFC del contribuyente que envía los datos
    :param mes: Atributo requerido para expresar el mes al que corresponde la balanza de comprobación
    :param anio: Atributo requerido para expresar el año al que corresponde la balanza
    :param tipo_envio: Atributo requerido para expresar el tipo de envío de la balanza (N - Normal; C - Complementaria)
    :param ctas: Nodo obligatorio para expresar el detalle de cada cuenta o subcuenta de la balanza de comprobación.
    :param fecha_mod_bal: Atributo opcional para expresar la fecha de la última modificación contable de la balanza de comprobación. Es requerido cuando el atributo TipoEnvio = C. Se convierte en requerido cuando se cuente con la información.
    :param sello: Atributo opcional para contener el sello digital del archivo de contabilidad electrónica. El sello deberá ser expresado cómo una cadena de texto en formato Base 64
    :param no_certificado: Atributo opcional para expresar el número de serie del certificado de sello digital que ampara el archivo de contabilidad electrónica, de acuerdo al acuse correspondiente a 20 posiciones otorgado por el sistema del SAT.
    :param certificado: Atributo opcional que sirve para expresar el certificado de sello digital que ampara al archivo de contabilidad electrónica como texto, en formato base 64.
    """
    
    tag = '{www.sat.gob.mx/esquemas/ContabilidadE/1_1/BalanzaComprobacion}Balanza'
    version = '1.1'
    
    def __init__(
            self,
            rfc: str,
            mes: str,
            anio: int,
            tipo_envio: str,
            ctas: Ctas | dict | Sequence[Ctas | dict],
            fecha_mod_bal: date = None,
            sello: str = None,
            no_certificado: str = None,
            certificado: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'RFC': rfc,
            'Mes': mes,
            'Anio': anio,
            'TipoEnvio': tipo_envio,
            'Ctas': ctas,
            'FechaModBal': fecha_mod_bal,
            'Sello': sello,
            'NoCertificado': no_certificado,
            'Certificado': certificado,
        })
        

