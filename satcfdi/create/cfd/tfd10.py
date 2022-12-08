from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import *

from ... import Signer
from ... import CFDI, XElement, ScalarMap
from ...transform import MEXICO_TZ


class TimbreFiscalDigital(CFDI):
    """
    Complemento requerido para el Timbrado Fiscal Digital que da valides a un Comprobante Fiscal Digital.
    """
    tag = '{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital'
    version = '1.0'
    
    def __init__(
            self,
            proveedor: Signer,
            uuid: str,
            fecha_timbrado: datetime,
            sello_cfd: str
    ):
        """
        Complemento requerido para el Timbrado Fiscal Digital que da valides a un Comprobante Fiscal Digital.
        
        :param uuid: Atributo requerido para expresar los 36 caracteres del UUID de la transacción de timbrado
        :param fecha_timbrado: Atributo requerido para expresar la fecha y hora de la generación del timbre
        :param sello_cfd: Atributo requerido para contener el sello digital del comprobante fiscal, que será timbrado. El sello deberá ser expresado cómo una cadena de texto en formato Base 64.
        :param no_certificado_sat: Atributo requerido para expresar el número de serie del certificado del SAT usado para el Timbre
        :param sello_sat: Atributo requerido para contener el sello digital del Timbre Fiscal Digital, al que hacen referencia las reglas de resolución miscelánea aplicable. El sello deberá ser expresado cómo una cadena de texto en formato Base 64.
        :return: objeto CFDI
        """

        super().__init__({
            'Version': self.version,
            'UUID': uuid,
            'FechaTimbrado': fecha_timbrado or datetime.now(tz=MEXICO_TZ).replace(tzinfo=None),
            'RfcProvCertif': proveedor.rfc_pac,
            'SelloCFD': sello_cfd,
            'NoCertificadoSAT': proveedor.certificate_number,
            'SelloSAT': '',
        })

        self['SelloSAT'] = proveedor.sign_sha1(
            self.cadena_original().encode()
        )
