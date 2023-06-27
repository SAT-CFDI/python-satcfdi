from datetime import datetime

from ...cfdi import CFDI


class SelloDigitalContElec:
    """
    Documento requerido para el Sello Digital del SAT que da constancia de recibo del archivo de la contabilidad electrónica.
    """
    tag = '{www.sat.gob.mx/esquemas/ContabilidadE/1_3/SelloDigitalContElec}SelloDigitalContElec'
    version = '1.3'
    
    def __new__(
            cls,
            folio: str,
            rfc: str,
            fechade_sello: datetime,
            no_certificado_sat: str,
            sello_sat: str,
            sello: str = None,
    ) -> CFDI: 
        """
        Documento requerido para el Sello Digital del SAT que da constancia de recibo del archivo de la contabilidad electrónica.
        
        :param folio: Atributo requerido para expresar los 22 caracteres del folio asignado por el SAT en la recepción de los archivos.
        :param rfc: Atributo requerido para expresar el RFC del contribuyente que envía los datos
        :param fechade_sello: Atributo requerido para expresar la fecha y hora de la generación del Sello digital del SAT. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601
        :param no_certificado_sat: Atributo requerido para expresar el número de serie del certificado del SAT usado para generar el sello digital.
        :param sello_sat: Atributo requerido para contener el sello digital del SAT. El sello deberá ser expresado cómo una cadena de texto en formato Base 64.
        :param sello: Atributo opcional para contener el sello digital del archivo de contabilidad electrónica, que corresponda. El sello deberá ser expresado cómo una cadena de texto en formato Base 64.
        :return: objeto CFDI
        """
        
        cfdi = CFDI({
            'Version': cls.version,
            'Folio': folio,
            'RFC': rfc,
            'FechadeSello': fechade_sello,
            'NoCertificadoSAT': no_certificado_sat,
            'SelloSAT': sello_sat,
            'Sello': sello,
        })
        cfdi.tag = cls.tag
        return cfdi

        

