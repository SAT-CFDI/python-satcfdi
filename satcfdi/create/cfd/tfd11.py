"""tfd http://www.sat.gob.mx/TimbreFiscalDigital"""
from datetime import datetime
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap
from ...models.signer import Signer
from ...transform import MEXICO_TZ


class TimbreFiscalDigital(CFDI):
    """
    Complemento requerido para el Timbrado Fiscal Digital que da valides a un Comprobante Fiscal Digital.

    :param uuid: Atributo requerido para expresar los 36 caracteres del UUID de la transacción de timbrado
    :param fecha_timbrado: Atributo requerido para expresar la fecha y hora de la generación del timbre
    :param sello_cfd: Atributo requerido para contener el sello digital del comprobante fiscal, que será timbrado. El sello deberá ser expresado cómo una cadena de texto en formato Base 64.
    """

    tag = '{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital'
    version = '1.1'

    def __init__(
            self,
            proveedor: Signer,
            uuid: str,
            fecha_timbrado: datetime,
            sello_cfd: str,
            leyenda: str = None,
    ):
        super().__init__({
            'Version': self.version,
            'UUID': uuid,
            'FechaTimbrado': fecha_timbrado or datetime.now(tz=MEXICO_TZ).replace(tzinfo=None),
            'RfcProvCertif': proveedor.rfc_pac,
            'SelloCFD': sello_cfd,
            'NoCertificadoSAT': proveedor.certificate_number,
            'SelloSAT': '',
            'Leyenda': leyenda,
        })

        self['SelloSAT'] = proveedor.sign_sha256(
            self.cadena_original().encode()
        )
