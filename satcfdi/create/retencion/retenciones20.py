from collections.abc import *
from datetime import datetime
from decimal import Decimal

from .. import Signer
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap
from ...transform import get_timezone


class CfdiRetenRelacionados(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/2
    Nodo opcional para precisar la información de los comprobantes relacionados.
    """

    def __init__(
            self,
            tipo_relacion: str,
            uuid: str,
    ):
        """
        Nodo opcional para precisar la información de los comprobantes relacionados.
        
        :param tipo_relacion: Atributo requerido para indicar la clave de la relación que existe entre éste que se está generando y el comprobante que ampara retenciones e información de pagos previos.
        :param uuid: Atributo requerido para registrar el folio fiscal (UUID) de un comprobante que ampara retención e información de pagos, relacionado con el presente comprobante, ejemplo: Si éste sustituye a un comprobante cancelado.
        """

        super().__init__({
            'TipoRelacion': tipo_relacion,
            'UUID': uuid,
        })


class ImpRetenidos(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/2
    Nodo opcional para expresar el total de los impuestos retenidos que se desprenden de los conceptos expresados en el comprobante que ampara retenciones e información de pagos.
    """

    def __init__(
            self,
            monto_ret: Decimal | int,
            tipo_pago_ret: str,
            base_ret: Decimal | int = None,
            impuesto_ret: str = None,
    ):
        """
        Nodo opcional para expresar el total de los impuestos retenidos que se desprenden de los conceptos expresados en el comprobante que ampara retenciones e información de pagos.
        
        :param monto_ret: Atributo requerido para expresar el importe del impuesto retenido en el período o ejercicio que se relaciona en el comprobante que ampara retenciones e información de pagos. No se permiten valores negativos.
        :param tipo_pago_ret: Atributo requerido para precisar la clave del tipo del efecto que se le da al monto de la retención.
        :param base_ret: Atributo opcional para expresar la base del impuesto, que puede ser la diferencia entre los ingresos percibidos y las deducciones autorizadas. No se permiten valores negativos.
        :param impuesto_ret: Atributo opcional para señalar el tipo de impuesto retenido del período o ejercicio conforme al catálogo.
        """

        super().__init__({
            'MontoRet': monto_ret,
            'TipoPagoRet': tipo_pago_ret,
            'BaseRet': base_ret,
            'ImpuestoRet': impuesto_ret,
        })


class Totales(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/2
    Nodo requerido para expresar el total de las retenciones e información de los pagos efectuados en el período que ampara el comprobante.
    """

    def __init__(
            self,
            monto_tot_operacion: Decimal | int,
            monto_tot_grav: Decimal | int,
            monto_tot_exent: Decimal | int,
            monto_tot_ret: Decimal | int,
            utilidad_bimestral: Decimal | int = None,
            isr_correspondiente: Decimal | int = None,
            imp_retenidos: Sequence[ImpRetenidos | dict] = None,
    ):
        """
        Nodo requerido para expresar el total de las retenciones e información de los pagos efectuados en el período que ampara el comprobante.
        
        :param monto_tot_operacion: Atributo requerido para expresar el total del monto de la operación que se relaciona en el comprobante que ampara retenciones e información de pagos. No se permiten valores negativos.
        :param monto_tot_grav: Atributo requerido para expresar el total del monto gravado de la operación que se relaciona en el comprobante que ampara retenciones e información de pagos. No se permiten valores negativos.
        :param monto_tot_exent: Atributo requerido para expresar el total del monto exento de la operación que se relaciona en el comprobante que ampara retenciones e información de pagos. No se permiten valores negativos.
        :param monto_tot_ret: Atributo requerido para expresar el monto total de las retenciones. Sumatoria de los montos de retención del nodo ImpRetenidos. No se permiten valores negativos.
        :param utilidad_bimestral: Atributo condicional para expresar el monto de la utilidad bimestral.
        :param isr_correspondiente: Atributo condicional para expresar el monto del ISR correspondiente al bimestre.
        :param imp_retenidos: Nodo opcional para expresar el total de los impuestos retenidos que se desprenden de los conceptos expresados en el comprobante que ampara retenciones e información de pagos.
        """

        super().__init__({
            'MontoTotOperacion': monto_tot_operacion,
            'MontoTotGrav': monto_tot_grav,
            'MontoTotExent': monto_tot_exent,
            'MontoTotRet': monto_tot_ret,
            'UtilidadBimestral': utilidad_bimestral,
            'ISRCorrespondiente': isr_correspondiente,
            'ImpRetenidos': imp_retenidos,
        })


class Periodo(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/2
    Nodo requerido para expresar el período que corresponde al comprobante que ampara retenciones e información de pagos.
    """

    def __init__(
            self,
            mes_ini: str,
            mes_fin: str,
            ejercicio: str,
    ):
        """
        Nodo requerido para expresar el período que corresponde al comprobante que ampara retenciones e información de pagos.
        
        :param mes_ini: Atributo requerido para expresar la clave del mes inicial del período de la retención e información de pagos.
        :param mes_fin: Atributo requerido para expresar la clave del mes final del período de la retención e información de pagos.
        :param ejercicio: Atributo requerido para la expresión del ejercicio fiscal (año) de la retención e información de pagos.
        """

        super().__init__({
            'MesIni': mes_ini,
            'MesFin': mes_fin,
            'Ejercicio': ejercicio,
        })


class Extranjero(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/2
    Nodo requerido para expresar la información del contribuyente receptor del comprobante que ampara retenciones e información de pagos, cuando sea residente en el extranjero.
    """

    def __init__(
            self,
            nom_den_raz_soc_r: str,
            num_reg_id_trib_r: str = None,
    ):
        """
        Nodo requerido para expresar la información del contribuyente receptor del comprobante que ampara retenciones e información de pagos, cuando sea residente en el extranjero.
        
        :param nom_den_raz_soc_r: Atributo requerido para expresar el nombre, denominación o razón social del receptor del comprobante que ampara retenciones e información de pagos, cuando sea residente en el extranjero.
        :param num_reg_id_trib_r: Atributo opcional para expresar el número de registro de identificación fiscal del receptor del comprobante que ampara retenciones e información de pagos, cuando sea residente en el extranjero.
        """

        super().__init__({
            'NomDenRazSocR': nom_den_raz_soc_r,
            'NumRegIdTribR': num_reg_id_trib_r,
        })


class Nacional(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/2
    Nodo requerido para expresar la información del contribuyente receptor en caso de que sea de nacionalidad mexicana.
    """

    def __init__(
            self,
            rfc_r: str,
            nom_den_raz_soc_r: str,
            domicilio_fiscal_r: str,
            curp_r: str = None,
    ):
        """
        Nodo requerido para expresar la información del contribuyente receptor en caso de que sea de nacionalidad mexicana.
        
        :param rfc_r: Atributo requerido para registrar la clave del Registro Federal de Contribuyentes correspondiente al contribuyente receptor del comprobante que ampara retenciones e información de pagos.
        :param nom_den_raz_soc_r: Atributo requerido para registrar el(los) nombre(s), primer apellido, segundo apellido, según corresponda, denominación o razón social del contribuyente, inscrito en el RFC, del receptor del comprobante que ampara retenciones e información de pagos.
        :param domicilio_fiscal_r: Atributo requerido para registrar el código postal del domicilio fiscal del receptor del comprobante que ampara retenciones e información de pagos.
        :param curp_r: Atributo opcional para la Clave Única del Registro Poblacional del contribuyente receptor del comprobante que ampara retenciones e información de pagos.
        """

        super().__init__({
            'RfcR': rfc_r,
            'NomDenRazSocR': nom_den_raz_soc_r,
            'DomicilioFiscalR': domicilio_fiscal_r,
            'CurpR': curp_r,
        })


class Receptor(ScalarMap):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/2
    Nodo requerido para expresar la información del contribuyente receptor del comprobante que ampara retenciones e información de pagos.
    """

    def __init__(
            self,
            nacionalidad_r: str,
            nacional: Nacional | dict = None,
            extranjero: Extranjero | dict = None,
    ):
        """
        Nodo requerido para expresar la información del contribuyente receptor del comprobante que ampara retenciones e información de pagos.
        
        :param nacionalidad_r: Atributo requerido para expresar la nacionalidad del receptor del comprobante que ampara retenciones e información de pagos.
        :param nacional: Nodo requerido para expresar la información del contribuyente receptor en caso de que sea de nacionalidad mexicana.
        :param extranjero: Nodo requerido para expresar la información del contribuyente receptor del comprobante que ampara retenciones e información de pagos, cuando sea residente en el extranjero.
        """

        super().__init__({
            'NacionalidadR': nacionalidad_r,
            'Nacional': nacional,
            'Extranjero': extranjero,
        })


class Emisor(ScalarMap):
    """
    Nodo requerido para expresar la información del contribuyente emisor del comprobante que ampara retenciones e información de pagos.

    :param rfc_e: Atributo requerido para registrar la clave del Registro Federal de Contribuyentes correspondiente al contribuyente emisor del comprobante que ampara retenciones e información de pagos, sin guiones o espacios.
    :param nom_den_raz_soc_e: Atributo requerido para registrar el nombre, denominación o razón social del contribuyente inscrito en el RFC, emisor del comprobante que ampara retenciones e información de pagos.
    :param regimen_fiscal_e: Atributo requerido para incorporar la clave del régimen del contribuyente emisor del comprobante que ampara retenciones e información de pagos.
    """

    def __init__(
            self,
            rfc_e: str,
            nom_den_raz_soc_e: str,
            regimen_fiscal_e: str,
    ):
        super().__init__({
            'RfcE': rfc_e,
            'NomDenRazSocE': nom_den_raz_soc_e,
            'RegimenFiscalE': regimen_fiscal_e,
        })


class Retenciones(CFDI):
    """
    Estándar del Comprobante Fiscal Digital por Internet que ampara retenciones e información de pagos. Los importes se expresan en la moneda de pesos mexicanos (MXN).
    """
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/2}Retenciones'
    version = '2.0'

    def __init__(
            self,
            lugar_exp_retenc: str,
            cve_retenc: str,
            emisor: Emisor | dict,
            receptor: Receptor | dict,
            periodo: Periodo | dict,
            totales: Totales | dict,
            folio_int: str = None,
            desc_retenc: str = None,
            cfdi_reten_relacionados: CfdiRetenRelacionados | dict = None,
            complemento: XElement | Sequence[XElement] = None,
            addenda: XElement | Sequence[XElement] = None,
            fecha_exp: datetime = None,
    ):
        """
        Estándar del Comprobante Fiscal Digital por Internet que ampara retenciones e información de pagos. Los importes se expresan en la moneda de pesos mexicanos (MXN).

        :param sello: Atributo requerido para contener el sello digital del comprobante que ampara retenciones e información de pagos, al que hacen referencia las reglas de resolución miscelánea vigente. El sello debe ser expresado como una cadena de texto en formato Base 64.
        :param no_certificado: Atributo requerido para expresar el número de serie del certificado de sello digital que ampara al comprobante de retención e información de pagos, de acuerdo con el acuse correspondiente a 20 posiciones otorgado por el sistema del SAT.
        :param certificado: Atributo requerido que sirve para incorporar el certificado de sello digital que ampara el comprobante de retención e información de pagos. El certificado debe ser expresado como una cadena de texto en formato Base 64.
        :param fecha_exp: Atributo requerido para la expresión de la fecha y hora de expedición del comprobante que ampara retenciones e información de pagos. Se expresa en la forma AAAA-MM-DDThh:mm:ss y debe corresponder con la hora local donde se expide el comprobante.
        :param lugar_exp_retenc: Atributo requerido para incorporar el código postal del lugar de expedición del comprobante que ampara retenciones e información de pagos.
        :param cve_retenc: Atributo requerido para expresar la clave de la retención e información de pagos de acuerdo al catálogo publicado en internet por el SAT.
        :param emisor: Nodo requerido para expresar la información del contribuyente emisor del comprobante que ampara retenciones e información de pagos.
        :param receptor: Nodo requerido para expresar la información del contribuyente receptor del comprobante que ampara retenciones e información de pagos.
        :param periodo: Nodo requerido para expresar el período que corresponde al comprobante que ampara retenciones e información de pagos.
        :param totales: Nodo requerido para expresar el total de las retenciones e información de los pagos efectuados en el período que ampara el comprobante.
        :param folio_int: Atributo opcional para control interno del contribuyente que expresa el folio del comprobante que ampara retenciones e información de pagos. Permite números y/o letras.
        :param desc_retenc: Atributo condicional que expresa la descripción de la retención e información de pagos.
        :param cfdi_reten_relacionados: Nodo opcional para precisar la información de los comprobantes relacionados.
        :param complemento: Nodo opcional donde se incluirá el complemento Timbre Fiscal Digital de manera obligatoria y los nodos complementarios determinados por el SAT, de acuerdo a las disposiciones particulares a un sector o actividad específica.
        :param addenda: Nodo opcional para recibir las extensiones al formato que sean de utilidad al contribuyente. Para las reglas de uso del mismo, referirse al formato de origen.
        """

        fecha_exp = fecha_exp or datetime.now(tz=get_timezone(lugar_exp_retenc)).replace(tzinfo=None)
        super().__init__({
            'Version': self.version,
            'Sello': '',
            'FechaExp': fecha_exp,
            'LugarExpRetenc': lugar_exp_retenc,
            'CveRetenc': cve_retenc,
            'FolioInt': folio_int,
            'DescRetenc': desc_retenc,
            'CfdiRetenRelacionados': cfdi_reten_relacionados,
            'Emisor': emisor,
            'Receptor': receptor,
            'Periodo': periodo,
            'Totales': totales,
            'Complemento': complemento,
            'Addenda': addenda,
        })

    def sign(self, signer: Signer):
        self['NoCertificado'] = signer.certificate_number,
        self['Certificado'] = signer.certificate_base64(),
        self['Sello'] = signer.sign_sha256(
            self.cadena_original().encode()
        )
