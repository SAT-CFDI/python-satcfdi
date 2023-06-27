from collections.abc import *
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from ...cfdi import CFDI
from ...models import Signer
from ...xelement import XElement
from ...utils import ScalarMap


class ImpRetenidos(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/1
    Nodo opcional para expresar el total de los impuestos retenidos que se desprenden de los conceptos expresados en el documento de retenciones e información de pagos.
    """
    def __init__(
            self,
            monto_ret: Decimal | int,
            tipo_pago_ret: str,
            base_ret: Decimal | int = None,
            impuesto: str = None,
    ): 
        """
        Nodo opcional para expresar el total de los impuestos retenidos que se desprenden de los conceptos expresados en el documento de retenciones e información de pagos.
        
        :param monto_ret: Atributo requerido para expresar el importe del impuesto retenido en el periodo o ejercicio
        :param tipo_pago_ret: Atributo requerido para precisar si el monto de la retención es considerado pago definitivo o pago provisional
        :param base_ret: Atributo opcional para expresar la  base del impuesto, que puede ser la diferencia entre los ingresos percibidos y las deducciones autorizadas
        :param impuesto: Atributo opcional para señalar el tipo de impuesto retenido del periodo o ejercicio conforme al catálogo.
        """
        
        super().__init__({
            'MontoRet': monto_ret,
            'TipoPagoRet': tipo_pago_ret,
            'BaseRet': base_ret,
            'Impuesto': impuesto,
        })
        

class Totales(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/1
    Nodo requerido para expresar el total de las retenciones e información de pagos efectuados en el período que ampara el documento.
    """
    def __init__(
            self,
            monto_tot_operacion: Decimal | int,
            monto_tot_grav: Decimal | int,
            monto_tot_exent: Decimal | int,
            monto_tot_ret: Decimal | int,
            imp_retenidos: Sequence[ImpRetenidos | dict] = None,
    ): 
        """
        Nodo requerido para expresar el total de las retenciones e información de pagos efectuados en el período que ampara el documento.
        
        :param monto_tot_operacion: Atributo requerido para expresar  el total del monto de la operación  que se relaciona en el comprobante 
        :param monto_tot_grav: Atributo requerido para expresar el total del monto gravado de la operación  que se relaciona en el comprobante.
        :param monto_tot_exent: Atributo requerido para expresar el total del monto exento de la operación  que se relaciona en el comprobante.
        :param monto_tot_ret: Atributo requerido para expresar el monto total de las retenciones. Sumatoria de los montos de retención del nodo ImpRetenidos.
        :param imp_retenidos: Nodo opcional para expresar el total de los impuestos retenidos que se desprenden de los conceptos expresados en el documento de retenciones e información de pagos.
        """
        
        super().__init__({
            'MontoTotOperacion': monto_tot_operacion,
            'MontoTotGrav': monto_tot_grav,
            'MontoTotExent': monto_tot_exent,
            'MontoTotRet': monto_tot_ret,
            'ImpRetenidos': imp_retenidos,
        })
        

class Periodo(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/1
    Nodo requerido para expresar el periodo que ampara el documento de retenciones e información de pagos
    """
    def __init__(
            self,
            mes_ini: int,
            mes_fin: int,
            ejerc: int,
    ): 
        """
        Nodo requerido para expresar el periodo que ampara el documento de retenciones e información de pagos
        
        :param mes_ini: Atributo requerido para la expresión del mes inicial del periodo de la retención e información de pagos
        :param mes_fin: Atributo requerido para la expresión del mes final del periodo de la retención e información de pagos
        :param ejerc: Atributo requerido para la expresión del ejercicio fiscal (año) 
        """
        
        super().__init__({
            'MesIni': mes_ini,
            'MesFin': mes_fin,
            'Ejerc': ejerc,
        })
        

class Extranjero(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/1
    Nodo requerido para expresar la información del contribuyente receptor del documento cuando sea residente en el extranjero
    """
    def __init__(
            self,
            nom_den_raz_soc_r: str,
            num_reg_id_trib: str = None,
    ): 
        """
        Nodo requerido para expresar la información del contribuyente receptor del documento cuando sea residente en el extranjero
        
        :param nom_den_raz_soc_r: Atributo requerido para expresar el nombre, denominación o razón social del receptor del documento cuando sea residente en el extranjero
        :param num_reg_id_trib: Atributo opcional para expresar el número de registro de identificación fiscal del receptor del documento cuando sea residente en el extranjero
        """
        
        super().__init__({
            'NomDenRazSocR': nom_den_raz_soc_r,
            'NumRegIdTrib': num_reg_id_trib,
        })
        

class Nacional(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/1
    Nodo requerido para expresar la información del contribuyente receptor en caso de que sea de nacionalidad mexicana
    """
    def __init__(
            self,
            rfcrecep: str,
            nom_den_raz_soc_r: str = None,
            curpr: str = None,
    ): 
        """
        Nodo requerido para expresar la información del contribuyente receptor en caso de que sea de nacionalidad mexicana
        
        :param rfcrecep: Atributo requerido para la clave del Registro Federal de Contribuyentes correspondiente al contribuyente receptor del documento.
        :param nom_den_raz_soc_r: Atributo opcional para el nombre, denominación o razón social del contribuyente receptor del documento.
        :param curpr: Atributo opcional para la Clave Única del Registro Poblacional del contribuyente receptor del documento.
        """
        
        super().__init__({
            'RFCRecep': rfcrecep,
            'NomDenRazSocR': nom_den_raz_soc_r,
            'CURPR': curpr,
        })
        

class Receptor(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/1
    Nodo requerido para expresar la información del contribuyente receptor del documento electrónico de retenciones e información de pagos.
    """
    def __init__(
            self,
            nacionalidad: str,
            nacional: Nacional | dict = None,
            extranjero: Extranjero | dict = None,
    ): 
        """
        Nodo requerido para expresar la información del contribuyente receptor del documento electrónico de retenciones e información de pagos.
        
        :param nacionalidad: Atributo requerido para expresar la nacionalidad del receptor del documento.
        :param nacional: Nodo requerido para expresar la información del contribuyente receptor en caso de que sea de nacionalidad mexicana
        :param extranjero: Nodo requerido para expresar la información del contribuyente receptor del documento cuando sea residente en el extranjero
        """
        
        super().__init__({
            'Nacionalidad': nacionalidad,
            'Nacional': nacional,
            'Extranjero': extranjero,
        })


class Emisor(ScalarMap):
    """
    Nodo requerido para expresar la información del contribuyente emisor del documento electrónico de retenciones e información de pagos.

    :param rfc_emisor: Atributo requerido para incorporar la clave en el Registro Federal de Contribuyentes correspondiente al contribuyente emisor del documento de retención e información de pagos, sin guiones o espacios.
    :param nom_den_raz_soc_e: Atributo opcional para el nombre, denominación o razón social del contribuyente emisor del documento de retención e información de pagos.
    :param curpe: Atributo opcional para la Clave Única del Registro Poblacional del contribuyente emisor del documento de retención e información de pagos.
    """

    def __init__(
            self,
            rfc_emisor: str,
            nom_den_raz_soc_e: str = None,
            curpe: str = None,
    ):
        super().__init__({
            'RFCEmisor': rfc_emisor,
            'NomDenRazSocE': nom_den_raz_soc_e,
            'CURPE': curpe,
        })


class Retenciones(CFDI):
    """
    Estándar de Documento Electrónico Retenciones e Información de Pagos.
    """
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1}Retenciones'
    version = '1.0'

    def __init__(
            self,
            cve_retenc: str,
            emisor: Emisor | dict,
            receptor: Receptor | dict,
            periodo: Periodo | dict,
            totales: Totales | dict,
            folio_int: str = None,
            desc_retenc: str = None,
            complemento: XElement | Sequence[XElement] = None,
            addenda: XElement | Sequence[XElement] = None,
            fecha_exp: datetime = None,
    ):
        """
        Estándar de Documento Electrónico Retenciones e Información de Pagos.

        :param sello: Atributo requerido para contener el sello digital del documento de retención e información de pagos. El sello deberá ser expresado como una cadena de texto en formato base 64.
        :param num_cert: Atributo requerido para expresar el número de serie del certificado de sello digital con el que se selló digitalmente el documento de la retención e información de pagos.
        :param cert: Atributo requerido que sirve para incorporar el certificado de sello digital que ampara el documento de retención e información de pagos como texto, en formato base 64.
        :param fecha_exp: Atributo requerido para la expresión de la fecha y hora de expedición del documento de retención e información de pagos. Se expresa en la forma yyyy-mm-ddThh:mm:ssTZD-6, de acuerdo con la especificación ISO 8601.
        :param cve_retenc: Atributo requerido para expresar la clave de la retención e información de pagos de acuerdo al catálogo publicado en internet por el SAT.
        :param emisor: Nodo requerido para expresar la información del contribuyente emisor del documento electrónico de retenciones e información de pagos.
        :param receptor: Nodo requerido para expresar la información del contribuyente receptor del documento electrónico de retenciones e información de pagos.
        :param periodo: Nodo requerido para expresar el periodo que ampara el documento de retenciones e información de pagos
        :param totales: Nodo requerido para expresar el total de las retenciones e información de pagos efectuados en el período que ampara el documento.
        :param folio_int: Atributo opcional para control interno del contribuyente que expresa el folio del documento que ampara la retención e información de pagos. Permite números y/o letras.
        :param desc_retenc: Atributo opcional que expresa la descripción de la retención e información de pagos en caso de que en el atributo CveRetenc se haya elegido el valor para 'otro tipo de retenciones'
        :param complemento: Nodo opcional donde se incluirá el complemento Timbre Fiscal Digital de manera obligatoria y los nodos complementarios determinados por el SAT, de acuerdo a las disposiciones particulares a un sector o actividad específica.
        :param addenda: Nodo opcional para recibir las extensiones al formato que sean de utilidad al contribuyente. Para las reglas de uso del mismo, referirse al formato de origen.
        """

        fecha_exp = fecha_exp or datetime.now(tz=timezone(timedelta(hours=-6)))
        super().__init__({
            'Version': self.version,
            'Sello': '',
            'NumCert': '',
            'Cert':  '',
            'FechaExp': fecha_exp,
            'CveRetenc': cve_retenc,
            'FolioInt': folio_int,
            'DescRetenc': desc_retenc,
            'Emisor': emisor,
            'Receptor': receptor,
            'Periodo': periodo,
            'Totales': totales,
            'Complemento': complemento,
            'Addenda': addenda,
        })

    def sign(self, signer: Signer):
        self['NumCert'] = signer.certificate_number
        self['Cert'] = signer.certificate_base64()
        self['Sello'] = signer.sign_sha1(
            self.cadena_original().encode()
        )
