"""AuxiliarCtas http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarCtas"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class DetalleAux(ScalarMap):
    """
    Nodo obligatorio para expresar el detalle de los movimientos del periodo de cada uno de los auxiliares
    
    :param fecha: Atributo requerido para expresar la fecha de registro de la transacción que afecta la cuenta o subcuenta que integra el auxiliar.
    :param num_un_iden_pol: Atributo requerido para expresar el número único de identificación de la póliza. El campo deberá contener la clave o nombre utilizado por el contribuyente para diferenciar, el tipo de póliza y el número correspondiente. En un mes ordinario no debe repetirse un mismo número de póliza con la clave o nombre asignado por el contribuyente.
    :param concepto: Atributo requerido para expresar el concepto de la transacción que integra el auxiliar.
    :param debe: Atributo requerido para expresar el monto del cargo de la cuenta o subcuenta de la transacción que integra el auxiliar. En caso de no existir dato, colocar cero (0)
    :param haber: Atributo requerido para expresar el monto del abono de la cuenta o subcuenta de la transacción que integra el auxiliar. En caso de no existir dato, colocar cero (0)
    """
    
    def __init__(
            self,
            fecha: date,
            num_un_iden_pol: str,
            concepto: str,
            debe: Decimal | int,
            haber: Decimal | int,
    ): 
        super().__init__({
            'Fecha': fecha,
            'NumUnIdenPol': num_un_iden_pol,
            'Concepto': concepto,
            'Debe': debe,
            'Haber': haber,
        })
        

class Cuenta(ScalarMap):
    """
    Nodo obligatorio para expresar los movimientos del periodo de cada uno de los auxiliares de la cuenta y/o subcuenta.
    
    :param num_cta: Atributo requerido para expresar la clave con que se distingue la cuenta o subcuenta que se afecta por la transacción que integra el auxiliar.
    :param des_cta: Atributo requerido para expresar el concepto de la cuenta o subcuenta que se afecta por la transacción que integra el auxiliar.
    :param saldo_ini: Atributo requerido para expresar el monto del saldo inicial de la cuenta o subcuenta del periodo del auxiliar. En caso de no existir dato, colocar cero (0)
    :param saldo_fin: Atributo requerido para expresar el monto del saldo final de la cuenta o subcuenta del periodo del auxiliar. En caso de no existir dato, colocar cero (0)
    :param detalle_aux: Nodo obligatorio para expresar el detalle de los movimientos del periodo de cada uno de los auxiliares
    """
    
    def __init__(
            self,
            num_cta: str,
            des_cta: str,
            saldo_ini: Decimal | int,
            saldo_fin: Decimal | int,
            detalle_aux: DetalleAux | dict | Sequence[DetalleAux | dict],
    ): 
        super().__init__({
            'NumCta': num_cta,
            'DesCta': des_cta,
            'SaldoIni': saldo_ini,
            'SaldoFin': saldo_fin,
            'DetalleAux': detalle_aux,
        })
        

class AuxiliarCtas(CFDI):
    """
    Estándar de auxiliar de la cuenta o subcuenta del periodo que se entrega como parte de la contabilidad electrónica
    
    :param rfc: Atributo requerido para expresar el RFC del contribuyente que envía los datos.
    :param mes: Atributo requerido para expresar el mes en que inicia la vigencia del auxiliar de la cuenta o subcuenta.
    :param anio: Atributo requerido para expresar el año al que inicia la vigencia del auxiliar de la cuenta o subcuenta.
    :param tipo_solicitud: Atributo requerido para expresar el tipo de envío del auxiliar de la cuenta o subcuenta ( AF - Acto de Fiscalización; FC - Fiscalización Compulsa; DE - Devolución; CO - Compensación )
    :param cuenta: Nodo obligatorio para expresar los movimientos del periodo de cada uno de los auxiliares de la cuenta y/o subcuenta.
    :param num_orden: Atributo opcional para expresar el número de orden asignado al acto de fiscalización al que hace referencia la solicitud del auxiliar de la cuenta o subcuenta. Requerido para tipo de solicitud = AF y FC. Se convierte en requerido cuando se cuente con la información.
    :param num_tramite: Atributo opcional para expresar el número de trámite asignado a la solicitud de devolución o compensación al que hace referencia el auxiliar de la cuenta o subcuenta. Requerido para tipo de solicitud = DE o CO. Se convierte en requerido cuando se cuente con la información.
    :param sello: Atributo opcional para contener el sello digital del archivo de contabilidad electrónica. El sello deberá ser expresado cómo una cadena de texto en formato Base 64
    :param no_certificado: Atributo opcional para expresar el número de serie del certificado de sello digital que ampara el archivo de contabilidad electrónica, de acuerdo al acuse correspondiente a 20 posiciones otorgado por el sistema del SAT.
    :param certificado: Atributo opcional que sirve para expresar el certificado de sello digital que ampara al archivo de contabilidad electrónica como texto, en formato base 64.
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarCtas}AuxiliarCtas'
    version = '1.3'
    
    def __init__(
            self,
            rfc: str,
            mes: str,
            anio: int,
            tipo_solicitud: str,
            cuenta: Cuenta | dict | Sequence[Cuenta | dict],
            num_orden: str = None,
            num_tramite: str = None,
            sello: str = None,
            no_certificado: str = None,
            certificado: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'RFC': rfc,
            'Mes': mes,
            'Anio': anio,
            'TipoSolicitud': tipo_solicitud,
            'Cuenta': cuenta,
            'NumOrden': num_orden,
            'NumTramite': num_tramite,
            'Sello': sello,
            'NoCertificado': no_certificado,
            'Certificado': certificado,
        })
        

