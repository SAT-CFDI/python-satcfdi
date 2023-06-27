"""PLZ www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class OtrMetodoPago(ScalarMap):
    """
    Nodo opcional para relacionar otros métodos de pago de la transacción. Se convierte en requerido cuando la transacción involucra un método de pago diverso a cheque y/o transferencia.
    
    :param met_pago_pol: Atributo requerido para expresar el método de pago de la operación, de acuerdo al catálogo publicado en la página de internet del SAT.
    :param fecha: Atributo requerido, es la fecha de la transacción de otros métodos de pago.
    :param benef: Atributo requerido, nombre de la persona o contribuyente a la cual se realiza éstos métodos de pago.
    :param rfc: Atributo requerido para expresar el RFC relacionado con la transacción. El RFC al que se hace referencia, es el distinto del contribuyente que envía los datos, es decir, el RFC del tercero vinculado.
    :param monto: Atributo requerido para expresar el monto del método de pago soporte de la transacción.
    :param moneda: Atributo opcional para expresar el tipo de moneda utilizado en la transacción, de acuerdo al catálogo publicado en la página de internet del SAT. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    :param tip_camb: Atributo opcional para expresar el tipo de cambio utilizado de acuerdo al tipo de moneda. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            met_pago_pol: str,
            fecha: date,
            benef: str,
            rfc: str,
            monto: Decimal | int,
            moneda: str = None,
            tip_camb: Decimal | int = None,
    ): 
        super().__init__({
            'MetPagoPol': met_pago_pol,
            'Fecha': fecha,
            'Benef': benef,
            'RFC': rfc,
            'Monto': monto,
            'Moneda': moneda,
            'TipCamb': tip_camb,
        })
        

class Transferencia(ScalarMap):
    """
    Nodo opcional para relacionar el detalle de las transferencias bancarias que integran la póliza. Se convierte en requerido cuando exista una salida de recursos que involucre este método de pago por parte del contribuyente que envía los datos. Además se convierte en requerido cuando se realicen transacciones, entre las cuentas propias del contribuyente.
    
    :param banco_ori_nal: Atributo requerido, para expresar el Banco de la cuenta origen de la transferencia, de acuerdo al catálogo publicado en la página de internet del SAT. Se considera banco nacional aquellos bancos de residencia nacional, indistintamente, si el tipo de moneda es nacional o extranjero.
    :param cta_dest: Atributo requerido para expresar el número de cuenta destino, la cual se transfieren los recursos.
    :param banco_dest_nal: Atributo requerido, para expresar el Banco de la cuenta destino de la transferencia, de acuerdo al catálogo publicado en la página de internet del SAT. Se considera banco nacional aquellos bancos de residencia nacional, indistintamente, si el tipo de moneda es nacional o extranjero.
    :param fecha: Atributo requerido, es la fecha de la transferencia
    :param benef: Atributo requerido, nombre del beneficiario de la transferencia.
    :param rfc: Atributo requerido para expresar el RFC relacionado con el movimiento. El RFC al que se hace referencia, es el distinto del contribuyente que envía los datos, es decir, el RFC del tercero vinculado.
    :param monto: Atributo requerido, es el monto transferido
    :param cta_ori: Atributo opcional para expresar el número de cuenta de origen desde la cual se transfieren los recursos. Se convierte en requerido cuando se cuente con la información.
    :param banco_ori_ext: Atributo opcional para expresar el nombre completo del banco origen extranjero. Se convierte en requerido cuando se cuente con la información.
    :param banco_dest_ext: Atributo opcional para expresar el nombre completo del banco destino extranjero. Se convierte en requerido cuando se cuente con la información.
    :param moneda: Atributo opcional para expresar el tipo de moneda utilizado en la transacción, de acuerdo al catálogo publicado en la página de internet del SAT. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    :param tip_camb: Atributo opcional para expresar el tipo de cambio utilizado de acuerdo al tipo de moneda. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            banco_ori_nal: str,
            cta_dest: str,
            banco_dest_nal: str,
            fecha: date,
            benef: str,
            rfc: str,
            monto: Decimal | int,
            cta_ori: str = None,
            banco_ori_ext: str = None,
            banco_dest_ext: str = None,
            moneda: str = None,
            tip_camb: Decimal | int = None,
    ): 
        super().__init__({
            'BancoOriNal': banco_ori_nal,
            'CtaDest': cta_dest,
            'BancoDestNal': banco_dest_nal,
            'Fecha': fecha,
            'Benef': benef,
            'RFC': rfc,
            'Monto': monto,
            'CtaOri': cta_ori,
            'BancoOriExt': banco_ori_ext,
            'BancoDestExt': banco_dest_ext,
            'Moneda': moneda,
            'TipCamb': tip_camb,
        })
        

class Cheque(ScalarMap):
    """
    Nodo opcional para relacionar el detalle de los cheques que integran la póliza. Se convierte en requerido cuando exista una salida de recursos, que involucre este método de pago de la obligación contraída por parte del contribuyente que envía los datos
    
    :param num: Atributo requerido para expresar el número del cheque emitido
    :param ban_emis_nal: Atributo requerido, para expresar el Banco nacional emisor del cheque, de acuerdo al catálogo publicado en la página de internet del SAT. Se consideran banco nacional aquellos bancos de residencia nacional, indistintamente, si el tipo de moneda es nacional o extranjero.
    :param cta_ori: Atributo requerido para expresar el número de cuenta bancaria del origen de los recursos.
    :param fecha: Atributo requerido, es la fecha del cheque
    :param benef: Atributo requerido, nombre del beneficiario del cheque
    :param rfc: Atributo requerido para expresar el RFC relacionado con el movimiento. El RFC al que se hace referencia, es el distinto del contribuyente que envía los datos, es decir, el RFC del tercero vinculado.
    :param monto: Atributo requerido, es el monto del cheque emitido
    :param ban_emis_ext: Atributo opcional para expresar el nombre completo del Banco extranjero emisor del cheque. Se convierte en requerido cuando se cuente con la información.
    :param moneda: Atributo opcional para expresar el tipo de moneda utilizado en la transacción, de acuerdo al catálogo publicado en la página de internet del SAT. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    :param tip_camb: Atributo opcional para expresar el tipo de cambio utilizado de acuerdo al tipo de moneda. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            num: str,
            ban_emis_nal: str,
            cta_ori: str,
            fecha: date,
            benef: str,
            rfc: str,
            monto: Decimal | int,
            ban_emis_ext: str = None,
            moneda: str = None,
            tip_camb: Decimal | int = None,
    ): 
        super().__init__({
            'Num': num,
            'BanEmisNal': ban_emis_nal,
            'CtaOri': cta_ori,
            'Fecha': fecha,
            'Benef': benef,
            'RFC': rfc,
            'Monto': monto,
            'BanEmisExt': ban_emis_ext,
            'Moneda': moneda,
            'TipCamb': tip_camb,
        })
        

class CompExt(ScalarMap):
    """
    Nodo opcional para relacionar el detalle de los comprobantes de origen extranjero relacionados con la transacción. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    
    :param num_fact_ext: Atributo requerido para expresar la clave numérico o alfanumérico del comprobante de origen extranjero que soporte la operación
    :param monto_total: Atributo requerido para expresar el monto total del comprobante de origen extranjero que soporte la operación.
    :param tax_id: Atributo opcional que sirve para expresar el Identificador del contribuyente extranjero. Se convierte en requerido cuando se cuente con la información
    :param moneda: Atributo opcional para expresar el tipo de moneda utilizado en la transacción, de acuerdo al catálogo publicado en la página de internet del SAT. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    :param tip_camb: Atributo opcional para expresar el tipo de cambio utilizado de acuerdo al tipo de moneda. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            num_fact_ext: str,
            monto_total: Decimal | int,
            tax_id: str = None,
            moneda: str = None,
            tip_camb: Decimal | int = None,
    ): 
        super().__init__({
            'NumFactExt': num_fact_ext,
            'MontoTotal': monto_total,
            'TaxID': tax_id,
            'Moneda': moneda,
            'TipCamb': tip_camb,
        })
        

class CompNalOtr(ScalarMap):
    """
    Nodo opcional para relacionar el detalle de los comprobantes de origen nacional relacionados con la transacción, diferente a CFDI, es decir, CFD y/o CBB. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    
    :param cfd_cbb_num_fol: Atributo requerido para expresar el número de folio del comprobante CFD_CBB que soporte la transacción.
    :param rfc: Atributo requerido para expresar el RFC relacionado con el movimiento o transacción. El RFC al que se hace referencia, es el distinto del contribuyente que envía los datos, es decir, el RFC del tercero vinculado.
    :param monto_total: Atributo requerido para expresar el monto total del CFD y/o CBB que soporte la transacción. (Incluye IVA en su caso)
    :param cfd_cbb_serie: Atributo opcional para expresar la serie del comprobante CFD_CBB que soporte la transacción.
    :param moneda: Atributo opcional para expresar el tipo de moneda utilizado en la transacción, de acuerdo al catálogo publicado en la página de internet del SAT. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    :param tip_camb: Atributo opcional para expresar el tipo de cambio utilizado de acuerdo al tipo de moneda. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            cfd_cbb_num_fol: int,
            rfc: str,
            monto_total: Decimal | int,
            cfd_cbb_serie: str = None,
            moneda: str = None,
            tip_camb: Decimal | int = None,
    ): 
        super().__init__({
            'CFD_CBB_NumFol': cfd_cbb_num_fol,
            'RFC': rfc,
            'MontoTotal': monto_total,
            'CFD_CBB_Serie': cfd_cbb_serie,
            'Moneda': moneda,
            'TipCamb': tip_camb,
        })
        

class CompNal(ScalarMap):
    """
    Nodo opcional para relacionar el detalle de los comprobantes de origen nacional relacionados con la transacción. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    
    :param uuid_cfdi: Atributo requerido para expresar la clave UUID del CFDI soporte de la operación. (36 caracteres)
    :param rfc: Atributo requerido para expresar el RFC relacionado con el movimiento o transacción. El RFC al que se hace referencia, es el distinto del contribuyente que envía los datos, es decir, el RFC del tercero vinculado.
    :param monto_total: Atributo requerido para expresar el monto total del CFDI que soporte la transacción. (Incluye IVA en su caso)
    :param moneda: Atributo opcional para expresar el tipo de moneda utilizado en la transacción, de acuerdo al catálogo publicado en la página de internet del SAT. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    :param tip_camb: Atributo opcional para expresar el tipo de cambio utilizado de acuerdo al tipo de moneda. Este dato sólo se utiliza en el caso de que el tipo de moneda, sea diferente a la moneda nacional (peso). Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            uuid_cfdi: str,
            rfc: str,
            monto_total: Decimal | int,
            moneda: str = None,
            tip_camb: Decimal | int = None,
    ): 
        super().__init__({
            'UUID_CFDI': uuid_cfdi,
            'RFC': rfc,
            'MontoTotal': monto_total,
            'Moneda': moneda,
            'TipCamb': tip_camb,
        })
        

class Transaccion(ScalarMap):
    """
    Nodo obligatorio para relacionar el detalle de cada transacción dentro de la póliza
    
    :param num_cta: Atributo requerido para expresar la clave con que se distingue la cuenta o subcuenta que se afecta por la transacción.
    :param des_cta: Atributo requerido para expresar el nombre de la cuenta o subcuenta que se afecta por la transacción.
    :param concepto: Atributo requerido para expresar el concepto de la transacción
    :param debe: Atributo requerido para expresar el monto del cargo a la cuenta o subcuenta que se afecta en la transacción. En caso de no existir dato, colocar cero (0)
    :param haber: Atributo requerido para expresar el monto del abono a la cuenta o subcuenta que se afecta en la transacción. En caso de no existir dato, colocar cero (0)
    :param comp_nal: Nodo opcional para relacionar el detalle de los comprobantes de origen nacional relacionados con la transacción. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    :param comp_nal_otr: Nodo opcional para relacionar el detalle de los comprobantes de origen nacional relacionados con la transacción, diferente a CFDI, es decir, CFD y/o CBB. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    :param comp_ext: Nodo opcional para relacionar el detalle de los comprobantes de origen extranjero relacionados con la transacción. Se considera que se debe identificar, el soporte documental, tanto en la provisión, como en el pago y/o cobro de cada una de las cuentas y subcuentas que se vean afectadas. Se convierte en requerido cuando se cuente con la información.
    :param cheque: Nodo opcional para relacionar el detalle de los cheques que integran la póliza. Se convierte en requerido cuando exista una salida de recursos, que involucre este método de pago de la obligación contraída por parte del contribuyente que envía los datos
    :param transferencia: Nodo opcional para relacionar el detalle de las transferencias bancarias que integran la póliza. Se convierte en requerido cuando exista una salida de recursos que involucre este método de pago por parte del contribuyente que envía los datos. Además se convierte en requerido cuando se realicen transacciones, entre las cuentas propias del contribuyente.
    :param otr_metodo_pago: Nodo opcional para relacionar otros métodos de pago de la transacción. Se convierte en requerido cuando la transacción involucra un método de pago diverso a cheque y/o transferencia.
    """
    
    def __init__(
            self,
            num_cta: str,
            des_cta: str,
            concepto: str,
            debe: Decimal | int,
            haber: Decimal | int,
            comp_nal: CompNal | dict | Sequence[CompNal | dict] = None,
            comp_nal_otr: CompNalOtr | dict | Sequence[CompNalOtr | dict] = None,
            comp_ext: CompExt | dict | Sequence[CompExt | dict] = None,
            cheque: Cheque | dict | Sequence[Cheque | dict] = None,
            transferencia: Transferencia | dict | Sequence[Transferencia | dict] = None,
            otr_metodo_pago: OtrMetodoPago | dict | Sequence[OtrMetodoPago | dict] = None,
    ): 
        super().__init__({
            'NumCta': num_cta,
            'DesCta': des_cta,
            'Concepto': concepto,
            'Debe': debe,
            'Haber': haber,
            'CompNal': comp_nal,
            'CompNalOtr': comp_nal_otr,
            'CompExt': comp_ext,
            'Cheque': cheque,
            'Transferencia': transferencia,
            'OtrMetodoPago': otr_metodo_pago,
        })
        

class Poliza(ScalarMap):
    """
    Nodo obligatorio para relacionar el detalle de cada transacción dentro de la póliza.
    
    :param num_un_iden_pol: Atributo requerido para expresar el número único de identificación de la póliza. El campo deberá contener la clave o nombre utilizado por el contribuyente para diferenciar, el tipo de póliza y el número correspondiente. En un mes ordinario no debe repetirse un mismo número de póliza con la clave o nombre asignado por el contribuyente.
    :param fecha: Atributo requerido para expresar la fecha de registro de la póliza
    :param concepto: Atributo requerido para expresar el concepto de la operación
    :param transaccion: Nodo obligatorio para relacionar el detalle de cada transacción dentro de la póliza
    """
    
    def __init__(
            self,
            num_un_iden_pol: str,
            fecha: date,
            concepto: str,
            transaccion: Transaccion | dict | Sequence[Transaccion | dict],
    ): 
        super().__init__({
            'NumUnIdenPol': num_un_iden_pol,
            'Fecha': fecha,
            'Concepto': concepto,
            'Transaccion': transaccion,
        })
        

class Polizas(CFDI):
    """
    Estándar de pólizas del periodo que se entrega como parte de la contabilidad electrónica.
    
    :param rfc: Atributo requerido para expresar el RFC del contribuyente que envía los datos
    :param mes: Atributo requerido para expresar el mes al que corresponde la póliza
    :param anio: Atributo requerido para expresar el año al que corresponde la póliza
    :param tipo_solicitud: Atributo requerido para expresar el tipo de solicitud de la póliza ( AF - Acto de Fiscalización; FC - Fiscalización Compulsa; DE - Devolución; CO - Compensación )
    :param poliza: Nodo obligatorio para relacionar el detalle de cada transacción dentro de la póliza.
    :param num_orden: Atributo opcional para expresar el número de orden asignado al acto de fiscalización al que hace referencia la solicitud de la póliza. Requerido para tipo de solicitud = AF y FC. Se convierte en requerido cuando se cuente con la información.
    :param num_tramite: Atributo opcional para expresar el número de trámite asignado a la solicitud de devolución o compensación al que hace referencia la solicitud de la póliza. Requerido para tipo de solicitud = DE o CO. Se convierte en requerido cuando se cuente con la información.
    :param sello: Atributo opcional para contener el sello digital del archivo de contabilidad electrónica. El sello deberá ser expresado cómo una cadena de texto en formato Base 64
    :param no_certificado: Atributo opcional para expresar el número de serie del certificado de sello digital que ampara el archivo de contabilidad electrónica, de acuerdo al acuse correspondiente a 20 posiciones otorgado por el sistema del SAT.
    :param certificado: Atributo opcional que sirve para expresar el certificado de sello digital que ampara al archivo de contabilidad electrónica como texto, en formato base 64.
    """
    
    tag = '{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}Polizas'
    version = '1.1'
    
    def __init__(
            self,
            rfc: str,
            mes: str,
            anio: int,
            tipo_solicitud: str,
            poliza: Poliza | dict | Sequence[Poliza | dict],
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
            'Poliza': poliza,
            'NumOrden': num_orden,
            'NumTramite': num_tramite,
            'Sello': sello,
            'NoCertificado': no_certificado,
            'Certificado': certificado,
        })
        

