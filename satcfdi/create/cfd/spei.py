"""spei http://www.sat.gob.mx/spei"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Beneficiario(ScalarMap):
    """
    Elemento para describir los datos del beneficiario del SPEI
    
    :param banco_receptor: Atributo requerido para expresar el nombre del Banco o Institución Financiera Receptora del SPEI
    :param nombre: Nombre de la persona física o moral receptora del pago.
    :param tipo_cuenta: Categoría de la cuenta a la que se efectuará el abono por la transferencia electrónica de fondos. Consultar Catálogo de Tipos de Cuenta.
    :param cuenta: Esta cuenta deberá estar ligada al campo Tipo de Cuenta del Beneficiario, donde son abonados los fondos.
    :param rfc: Atributo requerido para la expresión del registro federal de contribuyentes del beneficiario. Se pondrá ND en caso de no estar disponible
    :param concepto: Descripción del motivo por el que el ordenante hace el pago al beneficiario.
    :param monto_pago: Atributo obligatorio para la expresión del monto de la operación. Se trata de un entero positivo
    :param iva: Importes de IVA correspondientes al pago. El monto debe ser mayor a cero y menor o igual a 9,999,999,999,999,999.99
    """
    
    def __init__(
            self,
            banco_receptor: str,
            nombre: str,
            tipo_cuenta: Decimal | int,
            cuenta: Decimal | int,
            rfc: str,
            concepto: str,
            monto_pago: Decimal | int,
            iva: Decimal | int = None,
    ): 
        super().__init__({
            'BancoReceptor': banco_receptor,
            'Nombre': nombre,
            'TipoCuenta': tipo_cuenta,
            'Cuenta': cuenta,
            'RFC': rfc,
            'Concepto': concepto,
            'MontoPago': monto_pago,
            'IVA': iva,
        })
        

class Ordenante(ScalarMap):
    """
    Elemento para describir los datos del ordenante del SPEI
    
    :param banco_emisor: Atributo requerido para expresar el nombre del Banco o Institución Financiera emisora del SPEI
    :param nombre: Nombre de la persona física o moral que ordena el envío del pago.
    :param tipo_cuenta: Categoría de la Cuenta a la que se efectuará el cargo por la transferencia electrónica de fondos.
    :param cuenta: Cuenta que deberá estar ligada al Tipo de Cuenta del Ordenante, donde serán cargados los fondos.
    :param rfc: Corresponde al registro federal de contribuyentes o clave única de registro de población del ordenante. Se pondrá ND en caso de no tenerlo disponible
    """
    
    def __init__(
            self,
            banco_emisor: str,
            nombre: str,
            tipo_cuenta: Decimal | int,
            cuenta: Decimal | int,
            rfc: str,
    ): 
        super().__init__({
            'BancoEmisor': banco_emisor,
            'Nombre': nombre,
            'TipoCuenta': tipo_cuenta,
            'Cuenta': cuenta,
            'RFC': rfc,
        })
        

class SPEI_Tercero(ScalarMap):
    """
    Estándar aplicable a operaciones de SPEI a terceros
    
    :param fecha_operacion: Fecha de operación con formato. Debe ser la misma que la fecha de operación del sistema.
    :param hora: hora del acreditamiento
    :param clave_spei: Clave SPEI del Participante Emisor.
    :param sello: Atributo requerido para contener el sello digital del comprobante de pago. El sello deberá ser expresado cómo una cadena de texto en formato Base 64.
    :param numero_certificado: Atributo requerido para la identificación del certificado de seguridad utilizado para el sello digital.
    :param cadena_cda: Atributo que contiene la información del CDA fidedigna que la institución ha enviado a Banco de México.
    :param ordenante: Elemento para describir los datos del ordenante del SPEI
    :param beneficiario: Elemento para describir los datos del beneficiario del SPEI
    """
    
    def __init__(
            self,
            fecha_operacion: date,
            hora: time,
            clave_spei: int,
            sello: str,
            numero_certificado: str,
            cadena_cda: str,
            ordenante: Ordenante | dict,
            beneficiario: Beneficiario | dict,
    ): 
        super().__init__({
            'FechaOperacion': fecha_operacion,
            'Hora': hora,
            'ClaveSPEI': clave_spei,
            'Sello': sello,
            'NumeroCertificado': numero_certificado,
            'CadenaCDA': cadena_cda,
            'Ordenante': ordenante,
            'Beneficiario': beneficiario,
        })
        

class ComplementoSPEI(CFDI):
    """
    Complemento para el uso de SPEI Tercero a Tercero
    
    :param spei_tercero: Estándar aplicable a operaciones de SPEI a terceros
    """
    
    tag = '{http://www.sat.gob.mx/spei}Complemento_SPEI'
    
    def __init__(
            self,
            spei_tercero: SPEI_Tercero | dict | Sequence[SPEI_Tercero | dict],
    ): 
        super().__init__({
            'SPEI_Tercero': spei_tercero,
        })
        

