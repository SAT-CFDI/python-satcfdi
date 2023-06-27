"""RepAux www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class ComprExt(ScalarMap):
    """
    Nodo opcional para relacionar el detalle de los comprobantes de origen extranjero relacionados con la transacción. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    
    :param num_fact_ext: Atributo requerido para expresar la clave numérico o alfanumérico del comprobante de origen extranjero que soporte la operación
    :param monto_total: Atributo requerido para expresar el monto total del comprobante de origen extranjero que soporte la operación.
    :param tax_id: Atributo opcional que sirve para expresar el Identificador del contribuyente extranjero. Se convierte en requerido cuando se cuente con la información
    :param met_pago_aux: Atributo opcional para expresar el método de pago de la operación, de acuerdo al catálogo publicado en la página de internet del SAT. Se convierte en requerido cuando se cuente con la información.
    :param moneda: Atributo opcional para expresar el tipo de moneda utilizado en la transacción, de acuerdo al catálogo publicado en la página de internet del SAT. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    :param tip_camb: Atributo opcional para expresar el tipo de cambio utilizado de acuerdo al tipo de moneda. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            num_fact_ext: str,
            monto_total: Decimal | int,
            tax_id: str = None,
            met_pago_aux: str = None,
            moneda: str = None,
            tip_camb: Decimal | int = None,
    ): 
        super().__init__({
            'NumFactExt': num_fact_ext,
            'MontoTotal': monto_total,
            'TaxID': tax_id,
            'MetPagoAux': met_pago_aux,
            'Moneda': moneda,
            'TipCamb': tip_camb,
        })
        

class ComprNalOtr(ScalarMap):
    """
    Nodo opcional para relacionar el detalle de los comprobantes de origen nacional relacionados con la transacción, diferente a CFDI, es decir, CFD y/o CBB. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    
    :param cfd_cbb_num_fol: Atributo requerido para expresar el número de folio del comprobante CFD_CBB que soporte la operación.
    :param monto_total: Atributo requerido para expresar el monto total del CFD y/o CBB que soporte la operación. (Incluye IVA en su caso)
    :param rfc: Atributo requerido para expresar el RFC relacionado con la operación. El RFC al que se hace referencia, es el distinto del contribuyente que envía los datos, es decir, el RFC del tercero vinculado.
    :param cfd_cbb_serie: Atributo opcional para expresar la serie del comprobante CFD_CBB que soporte la operación.
    :param met_pago_aux: Atributo opcional para expresar el método de pago de la operación, de acuerdo al catálogo publicado en la página de internet del SAT. Se convierte en requerido cuando se cuente con la información.
    :param moneda: Atributo opcional para expresar el tipo de moneda utilizado en la transacción, de acuerdo al catálogo publicado en la página de internet del SAT. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    :param tip_camb: Atributo opcional para expresar el tipo de cambio utilizado de acuerdo al tipo de moneda. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            cfd_cbb_num_fol: int,
            monto_total: Decimal | int,
            rfc: str,
            cfd_cbb_serie: str = None,
            met_pago_aux: str = None,
            moneda: str = None,
            tip_camb: Decimal | int = None,
    ): 
        super().__init__({
            'CFD_CBB_NumFol': cfd_cbb_num_fol,
            'MontoTotal': monto_total,
            'RFC': rfc,
            'CFD_CBB_Serie': cfd_cbb_serie,
            'MetPagoAux': met_pago_aux,
            'Moneda': moneda,
            'TipCamb': tip_camb,
        })
        

class ComprNal(ScalarMap):
    """
    Nodo opcional para relacionar el detalle de los comprobantes de origen nacional relacionados con la transacción. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    
    :param uuid_cfdi: Atributo requerido para expresar la clave UUID del CFDI soporte de la operación. (36 caracteres)
    :param monto_total: Atributo requerido para expresar el monto total del CFDI que soporte la operación (Incluye IVA en su caso)
    :param rfc: Atributo requerido para expresar el RFC relacionado con la operación. El RFC al que se hace referencia, es el distinto del contribuyente que envía los datos, es decir, el RFC del tercero vinculado.
    :param met_pago_aux: Atributo opcional para expresar el método de pago de la operación, de acuerdo al catálogo publicado en la página de internet del SAT. Se convierte en requerido cuando se cuente con la información.
    :param moneda: Atributo opcional para expresar el tipo de moneda utilizado en la transacción, de acuerdo al catálogo publicado en la página de internet del SAT. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    :param tip_camb: Atributo opcional para expresar el tipo de cambio utilizado de acuerdo al tipo de moneda. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            uuid_cfdi: str,
            monto_total: Decimal | int,
            rfc: str,
            met_pago_aux: str = None,
            moneda: str = None,
            tip_camb: Decimal | int = None,
    ): 
        super().__init__({
            'UUID_CFDI': uuid_cfdi,
            'MontoTotal': monto_total,
            'RFC': rfc,
            'MetPagoAux': met_pago_aux,
            'Moneda': moneda,
            'TipCamb': tip_camb,
        })
        

class DetAuxFol(ScalarMap):
    """
    Nodo opcional para expresar el detalle de los folios de los comprobantes fiscales que integran la póliza.
    
    :param num_un_iden_pol: Atributo requerido para expresar el número único de identificación de la póliza. El campo deberá contener la clave o nombre utilizado por el contribuyente para diferenciar, el tipo de póliza y el número correspondiente. En un mes ordinario no debe repetirse un mismo número de póliza con la clave o nombre asignado por el contribuyente.
    :param fecha: Atributo requerido para expresar la fecha de registro de la póliza.
    :param compr_nal: Nodo opcional para relacionar el detalle de los comprobantes de origen nacional relacionados con la transacción. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    :param compr_nal_otr: Nodo opcional para relacionar el detalle de los comprobantes de origen nacional relacionados con la transacción, diferente a CFDI, es decir, CFD y/o CBB. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    :param compr_ext: Nodo opcional para relacionar el detalle de los comprobantes de origen extranjero relacionados con la transacción. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            num_un_iden_pol: str,
            fecha: date,
            compr_nal: ComprNal | dict | Sequence[ComprNal | dict] = None,
            compr_nal_otr: ComprNalOtr | dict | Sequence[ComprNalOtr | dict] = None,
            compr_ext: ComprExt | dict | Sequence[ComprExt | dict] = None,
    ): 
        super().__init__({
            'NumUnIdenPol': num_un_iden_pol,
            'Fecha': fecha,
            'ComprNal': compr_nal,
            'ComprNalOtr': compr_nal_otr,
            'ComprExt': compr_ext,
        })
        

class RepAuxFol(CFDI):
    """
    Estándar de reporte auxiliar de folios de los comprobantes fiscales de las pólizas que se entrega como parte de las pólizas de la contabilidad electrónica.
    
    :param rfc: Atributo requerido para expresar el RFC del contribuyente que envía los datos
    :param mes: Atributo requerido para expresar el mes en que inicia la vigencia del reporte auxiliar de los folios de los comprobantes fiscales de las pólizas.
    :param anio: Atributo requerido para expresar el año al que inicia la vigencia del reporte auxiliar de los folios de los comprobantes fiscales de las pólizas.
    :param tipo_solicitud: Atributo requerido para expresar el tipo de solicitud del reporte auxiliar de los folios de los comprobantes fiscales de las pólizas. ( AF - Acto de Fiscalización; FC - Fiscalización Compulsa; DE - Devolución; CO - Compensación )
    :param num_orden: Atributo opcional para expresar el número de orden asignado al acto de fiscalización al que hace referencia el reporte auxiliar de los folios de los comprobantes fiscales de las pólizas. Requerido para tipo de solicitud = AF y FC. Se convierte en requerido cuando se cuente con la información.
    :param num_tramite: Atributo opcional para expresar el número de trámite asignado a la solicitud de devolución o compensación al que hace referencia el reporte auxiliar de los folios de los comprobantes fiscales de las pólizas. Requerido para tipo de solicitud = DE o CO. Se convierte en requerido cuando se cuente con la información.
    :param sello: Atributo opcional para contener el sello digital del archivo de contabilidad electrónica. El sello deberá ser expresado cómo una cadena de texto en formato Base 64
    :param no_certificado: Atributo opcional para expresar el número de serie del certificado de sello digital que ampara el archivo de contabilidad electrónica, de acuerdo al acuse correspondiente a 20 posiciones otorgado por el sistema del SAT.
    :param certificado: Atributo opcional que sirve para expresar el certificado de sello digital que ampara al archivo de contabilidad electrónica como texto, en formato base 64.
    :param det_aux_fol: Nodo opcional para expresar el detalle de los folios de los comprobantes fiscales que integran la póliza.
    """
    
    tag = '{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios}RepAuxFol'
    version = '1.2'
    
    def __init__(
            self,
            rfc: str,
            mes: str,
            anio: int,
            tipo_solicitud: str,
            num_orden: str = None,
            num_tramite: str = None,
            sello: str = None,
            no_certificado: str = None,
            certificado: str = None,
            det_aux_fol: DetAuxFol | dict | Sequence[DetAuxFol | dict] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'RFC': rfc,
            'Mes': mes,
            'Anio': anio,
            'TipoSolicitud': tipo_solicitud,
            'NumOrden': num_orden,
            'NumTramite': num_tramite,
            'Sello': sello,
            'NoCertificado': no_certificado,
            'Certificado': certificado,
            'DetAuxFol': det_aux_fol,
        })
        

