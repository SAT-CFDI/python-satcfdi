"""cfdi http://www.sat.gob.mx/cfd/3"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class TInformacionAduanera(ScalarMap):
    """
    Tipo definido para expresar información aduanera
    
    :param numero: Atributo requerido para expresar el número del documento aduanero que ampara la importación del bien.
    :param fecha: Atributo requerido para expresar la fecha de expedición del documento aduanero que ampara la importación del bien. Se expresa en el formato aaaa-mm-dd
    :param aduana: Atributo opcional para precisar el nombre de la aduana por la que se efectuó la importación del bien.
    """
    
    def __init__(
            self,
            numero: str,
            fecha: date,
            aduana: str = None,
    ): 
        super().__init__({
            'Numero': numero,
            'Fecha': fecha,
            'Aduana': aduana,
        })
        

class TUbicacionFiscal(ScalarMap):
    """
    Tipo definido para expresar domicilios o direcciones
    
    :param calle: Este atributo requerido sirve para precisar la avenida, calle, camino o carretera donde se da la ubicación.
    :param municipio: Atributo requerido que sirve para precisar el municipio o delegación (en el caso del Distrito Federal) en donde se da la ubicación.
    :param estado: Atributo requerido que sirve para precisar el estado o entidad federativa donde se da la ubicación.
    :param pais: Atributo requerido que sirve para precisar el país donde se da la ubicación.
    :param codigo_postal: Atributo requerido que sirve para asentar el código postal en donde se da la ubicación.
    :param no_exterior: Este atributo opcional sirve para expresar el número particular en donde se da la ubicación sobre una calle dada.
    :param no_interior: Este atributo opcional sirve para expresar información adicional para especificar la ubicación cuando calle y número exterior (noExterior) no resulten suficientes para determinar la ubicación de forma precisa.
    :param colonia: Este atributo opcional sirve para precisar la colonia en donde se da la ubicación cuando se desea ser más específico en casos de ubicaciones urbanas.
    :param localidad: Atributo opcional que sirve para precisar la ciudad o población donde se da la ubicación.
    :param referencia: Atributo opcional para expresar una referencia de ubicación adicional.
    """
    
    def __init__(
            self,
            calle: str,
            municipio: str,
            estado: str,
            pais: str,
            codigo_postal: str,
            no_exterior: str = None,
            no_interior: str = None,
            colonia: str = None,
            localidad: str = None,
            referencia: str = None,
    ): 
        super().__init__({
            'Calle': calle,
            'Municipio': municipio,
            'Estado': estado,
            'Pais': pais,
            'CodigoPostal': codigo_postal,
            'NoExterior': no_exterior,
            'NoInterior': no_interior,
            'Colonia': colonia,
            'Localidad': localidad,
            'Referencia': referencia,
        })
        

class TUbicacion(ScalarMap):
    """
    Tipo definido para expresar domicilios o direcciones
    
    :param pais: Atributo requerido que sirve para precisar el país donde se da la ubicación.
    :param calle: Este atributo opcional sirve para precisar la avenida, calle, camino o carretera donde se da la ubicación.
    :param no_exterior: Este atributo opcional sirve para expresar el número particular en donde se da la ubicación sobre una calle dada.
    :param no_interior: Este atributo opcional sirve para expresar información adicional para especificar la ubicación cuando calle y número exterior (noExterior) no resulten suficientes para determinar la ubicación de forma precisa.
    :param colonia: Este atributo opcional sirve para precisar la colonia en donde se da la ubicación cuando se desea ser más específico en casos de ubicaciones urbanas.
    :param localidad: Atributo opcional que sirve para precisar la ciudad o población donde se da la ubicación.
    :param referencia: Atributo opcional para expresar una referencia de ubicación adicional.
    :param municipio: Atributo opcional que sirve para precisar el municipio o delegación (en el caso del Distrito Federal) en donde se da la ubicación.
    :param estado: Atributo opcional que sirve para precisar el estado o entidad federativa donde se da la ubicación.
    :param codigo_postal: Atributo opcional que sirve para asentar el código postal en donde se da la ubicación.
    """
    
    def __init__(
            self,
            pais: str,
            calle: str = None,
            no_exterior: str = None,
            no_interior: str = None,
            colonia: str = None,
            localidad: str = None,
            referencia: str = None,
            municipio: str = None,
            estado: str = None,
            codigo_postal: str = None,
    ): 
        super().__init__({
            'Pais': pais,
            'Calle': calle,
            'NoExterior': no_exterior,
            'NoInterior': no_interior,
            'Colonia': colonia,
            'Localidad': localidad,
            'Referencia': referencia,
            'Municipio': municipio,
            'Estado': estado,
            'CodigoPostal': codigo_postal,
        })
        

class Traslado(ScalarMap):
    """
    Nodo para la información detallada de un traslado de impuesto específico
    
    :param impuesto: Atributo requerido para señalar el tipo de impuesto trasladado
    :param tasa: Atributo requerido para señalar la tasa del impuesto que se traslada por cada concepto amparado en el comprobante
    :param importe: Atributo requerido para señalar el importe del impuesto trasladado
    """
    
    def __init__(
            self,
            impuesto: str,
            tasa: Decimal | int,
            importe: Decimal | int,
    ): 
        super().__init__({
            'Impuesto': impuesto,
            'Tasa': tasa,
            'Importe': importe,
        })
        

class Retencion(ScalarMap):
    """
    Nodo para la información detallada de una retención de impuesto específico
    
    :param impuesto: Atributo requerido para señalar el tipo de impuesto retenido
    :param importe: Atributo requerido para señalar el importe o monto del impuesto retenido
    """
    
    def __init__(
            self,
            impuesto: str,
            importe: Decimal | int,
    ): 
        super().__init__({
            'Impuesto': impuesto,
            'Importe': importe,
        })
        

class Impuestos(ScalarMap):
    """
    Nodo requerido para capturar los impuestos aplicables.
    
    :param total_impuestos_retenidos: Atributo opcional para expresar el total de los impuestos retenidos que se desprenden de los conceptos expresados en el comprobante fiscal digital a través de Internet.
    :param total_impuestos_trasladados: Atributo opcional para expresar el total de los impuestos trasladados que se desprenden de los conceptos expresados en el comprobante fiscal digital a través de Internet.
    :param retenciones: Nodo opcional para capturar los impuestos retenidos aplicables
    :param traslados: Nodo opcional para asentar o referir los impuestos trasladados aplicables
    """
    
    def __init__(
            self,
            total_impuestos_retenidos: Decimal | int = None,
            total_impuestos_trasladados: Decimal | int = None,
            retenciones: Retencion | dict | Sequence[Retencion | dict] = None,
            traslados: Traslado | dict | Sequence[Traslado | dict] = None,
    ): 
        super().__init__({
            'TotalImpuestosRetenidos': total_impuestos_retenidos,
            'TotalImpuestosTrasladados': total_impuestos_trasladados,
            'Retenciones': retenciones,
            'Traslados': traslados,
        })
        

class Parte(ScalarMap):
    """
    Nodo opcional para expresar las partes o componentes que integran la totalidad del concepto expresado en el comprobante fiscal digital a través de Internet
    
    :param cantidad: Atributo requerido para precisar la cantidad de bienes o servicios del tipo particular definido por la presente parte.
    :param descripcion: Atributo requerido para precisar la descripción del bien o servicio cubierto por la presente parte.
    :param unidad: Atributo opcional para precisar la unidad de medida aplicable para la cantidad expresada en la parte.
    :param no_identificacion: Atributo opcional para expresar el número de serie del bien o identificador del servicio amparado por la presente parte.
    :param valor_unitario: Atributo opcional para precisar el valor o precio unitario del bien o servicio cubierto por la presente parte.
    :param importe: Atributo opcional para precisar el importe total de los bienes o servicios de la presente parte. Debe ser equivalente al resultado de multiplicar la cantidad por el valor unitario expresado en la parte.
    :param informacion_aduanera: Nodo opcional para introducir la información aduanera aplicable cuando se trate de partes o componentes importados vendidos de primera mano.
    """
    
    def __init__(
            self,
            cantidad: Decimal | int,
            descripcion: str,
            unidad: str = None,
            no_identificacion: str = None,
            valor_unitario: Decimal | int = None,
            importe: Decimal | int = None,
            informacion_aduanera: TInformacionAduanera | dict | Sequence[TInformacionAduanera | dict] = None,
    ): 
        super().__init__({
            'Cantidad': cantidad,
            'Descripcion': descripcion,
            'Unidad': unidad,
            'NoIdentificacion': no_identificacion,
            'ValorUnitario': valor_unitario,
            'Importe': importe,
            'InformacionAduanera': informacion_aduanera,
        })
        

class Concepto(ScalarMap):
    """
    Nodo para introducir la información detallada de un bien o servicio amparado en el comprobante.
    
    :param cantidad: Atributo requerido para precisar la cantidad de bienes o servicios del tipo particular definido por el presente concepto.
    :param unidad: Atributo requerido para precisar la unidad de medida aplicable para la cantidad expresada en el concepto.
    :param descripcion: Atributo requerido para precisar la descripción del bien o servicio cubierto por el presente concepto.
    :param valor_unitario: Atributo requerido para precisar el valor o precio unitario del bien o servicio cubierto por el presente concepto.
    :param importe: Atributo requerido para precisar el importe total de los bienes o servicios del presente concepto. Debe ser equivalente al resultado de multiplicar la cantidad por el valor unitario expresado en el concepto.
    :param no_identificacion: Atributo opcional para expresar el número de serie del bien o identificador del servicio amparado por el presente concepto.
    :param informacion_aduanera: Nodo opcional para introducir la información aduanera aplicable cuando se trate de ventas de primera mano de mercancías importadas.
    :param cuenta_predial: Nodo opcional para asentar el número de cuenta predial con el que fue registrado el inmueble, en el sistema catastral de la entidad federativa de que trate, o bien para incorporar los datos de identificación del certificado de participación inmobiliaria no amortizable.
    :param complemento_concepto: Nodo opcional donde se incluirán los nodos complementarios de extensión al concepto, definidos por el SAT, de acuerdo a disposiciones particulares a un sector o actividad especifica.
    :param parte: Nodo opcional para expresar las partes o componentes que integran la totalidad del concepto expresado en el comprobante fiscal digital a través de Internet
    """
    
    def __init__(
            self,
            cantidad: Decimal | int,
            unidad: str,
            descripcion: str,
            valor_unitario: Decimal | int,
            importe: Decimal | int,
            no_identificacion: str = None,
            informacion_aduanera: TInformacionAduanera | dict | Sequence[TInformacionAduanera | dict] = None,
            cuenta_predial: str = None,
            complemento_concepto: XElement | Sequence[XElement] = None,
            parte: Parte | dict | Sequence[Parte | dict] = None,
    ): 
        super().__init__({
            'Cantidad': cantidad,
            'Unidad': unidad,
            'Descripcion': descripcion,
            'ValorUnitario': valor_unitario,
            'Importe': importe,
            'NoIdentificacion': no_identificacion,
            'InformacionAduanera': informacion_aduanera,
            'CuentaPredial': cuenta_predial,
            'ComplementoConcepto': complemento_concepto,
            'Parte': parte,
        })
        

class Receptor(ScalarMap):
    """
    Nodo requerido para precisar la información del contribuyente receptor del comprobante.
    
    :param rfc: Atributo requerido para precisar la Clave del Registro Federal de Contribuyentes correspondiente al contribuyente receptor del comprobante.
    :param nombre: Atributo opcional para el nombre, denominación o razón social del contribuyente receptor del comprobante.
    :param domicilio: Nodo opcional para la definición de la ubicación donde se da el domicilio del receptor del comprobante fiscal.
    """
    
    def __init__(
            self,
            rfc: str,
            nombre: str = None,
            domicilio: TUbicacion | dict = None,
    ): 
        super().__init__({
            'Rfc': rfc,
            'Nombre': nombre,
            'Domicilio': domicilio,
        })
        

class Emisor(ScalarMap):
    """
    Nodo requerido para expresar la información del contribuyente emisor del comprobante.
    
    :param rfc: Atributo requerido para la Clave del Registro Federal de Contribuyentes correspondiente al contribuyente emisor del comprobante sin guiones o espacios.
    :param regimen_fiscal: Nodo requerido para incorporar los regímenes en los que tributa el contribuyente emisor. Puede contener más de un régimen.
    :param nombre: Atributo opcional para el nombre, denominación o razón social del contribuyente emisor del comprobante.
    :param domicilio_fiscal: Nodo opcional para precisar la información de ubicación del domicilio fiscal del contribuyente emisor
    :param expedido_en: Nodo opcional para precisar la información de ubicación del domicilio en donde es emitido el comprobante fiscal en caso de que sea distinto del domicilio fiscal del contribuyente emisor.
    """
    
    def __init__(
            self,
            rfc: str,
            regimen_fiscal: str | Sequence[str],
            nombre: str = None,
            domicilio_fiscal: TUbicacionFiscal | dict = None,
            expedido_en: TUbicacion | dict = None,
    ): 
        super().__init__({
            'Rfc': rfc,
            'RegimenFiscal': regimen_fiscal,
            'Nombre': nombre,
            'DomicilioFiscal': domicilio_fiscal,
            'ExpedidoEn': expedido_en,
        })
        

class Comprobante(CFDI):
    """
    Estándar de Comprobante fiscal digital a través de Internet.
    
    :param fecha: Atributo requerido para la expresión de la fecha y hora de expedición del comprobante fiscal. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.
    :param sello: Atributo requerido para contener el sello digital del comprobante fiscal, al que hacen referencia las reglas de resolución miscelánea aplicable. El sello deberá ser expresado cómo una cadena de texto en formato Base 64.
    :param forma_de_pago: Atributo requerido para precisar la forma de pago que aplica para este comprobnante fiscal digital a través de Internet. Se utiliza para expresar Pago en una sola exhibición o número de parcialidad pagada contra el total de parcialidades, Parcialidad 1 de X.
    :param no_certificado: Atributo requerido para expresar el número de serie del certificado de sello digital que ampara al comprobante, de acuerdo al acuse correspondiente a 20 posiciones otorgado por el sistema del SAT.
    :param certificado: Atributo requerido que sirve para expresar el certificado de sello digital que ampara al comprobante como texto, en formato base 64.
    :param sub_total: Atributo requerido para representar la suma de los importes antes de descuentos e impuestos.
    :param total: Atributo requerido para representar la suma del subtotal, menos los descuentos aplicables, más los impuestos trasladados, menos los impuestos retenidos.
    :param tipo_de_comprobante: Atributo requerido para expresar el efecto del comprobante fiscal para el contribuyente emisor.
    :param metodo_de_pago: Atributo requerido de texto libre para expresar el método de pago de los bienes o servicios amparados por el comprobante. Se entiende como método de pago leyendas tales como: cheque, tarjeta de crédito o debito, depósito en cuenta, etc.
    :param lugar_expedicion: Atributo requerido para incorporar el lugar de expedición del comprobante.
    :param emisor: Nodo requerido para expresar la información del contribuyente emisor del comprobante.
    :param receptor: Nodo requerido para precisar la información del contribuyente receptor del comprobante.
    :param conceptos: Nodo requerido para enlistar los conceptos cubiertos por el comprobante.
    :param impuestos: Nodo requerido para capturar los impuestos aplicables.
    :param serie: Atributo opcional para precisar la serie para control interno del contribuyente. Este atributo acepta una cadena de caracteres alfabéticos de 1 a 25 caracteres sin incluir caracteres acentuados.
    :param folio: Atributo opcional para control interno del contribuyente que acepta un valor numérico entero superior a 0 que expresa el folio del comprobante.
    :param condiciones_de_pago: Atributo opcional para expresar las condiciones comerciales aplicables para el pago del comprobante fiscal digital a través de Internet.
    :param descuento: Atributo opcional para representar el importe total de los descuentos aplicables antes de impuestos.
    :param motivo_descuento: Atributo opcional para expresar el motivo del descuento aplicable.
    :param tipo_cambio: Atributo opcional para representar el tipo de cambio conforme a la moneda usada
    :param moneda: Atributo opcional para expresar la moneda utilizada para expresar los montos
    :param num_cta_pago: Atributo Opcional para incorporar al menos los cuatro últimos digitos del número de cuenta con la que se realizó el pago.
    :param folio_fiscal_orig: Atributo opcional para señalar el número de folio fiscal del comprobante que se hubiese expedido por el valor total del comprobante, tratándose del pago en parcialidades.
    :param serie_folio_fiscal_orig: Atributo opcional para señalar la serie del folio del comprobante que se hubiese expedido por el valor total del comprobante, tratándose del pago en parcialidades.
    :param fecha_folio_fiscal_orig: Atributo opcional para señalar la fecha de expedición del comprobante que se hubiese emitido por el valor total del comprobante, tratándose del pago en parcialidades. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.
    :param monto_folio_fiscal_orig: Atributo opcional para señalar el total del comprobante que se hubiese expedido por el valor total de la operación, tratándose del pago en parcialidades
    :param complemento: Nodo opcional donde se incluirá el complemento Timbre Fiscal Digital de manera obligatoria y los nodos complementarios determinados por el SAT, de acuerdo a las disposiciones particulares a un sector o actividad específica.
    :param addenda: Nodo opcional para recibir las extensiones al presente formato que sean de utilidad al contribuyente. Para las reglas de uso del mismo, referirse al formato de origen.
    """
    
    tag = '{http://www.sat.gob.mx/cfd/3}Comprobante'
    version = '3.2'
    
    def __init__(
            self,
            fecha: datetime,
            sello: str,
            forma_de_pago: str,
            no_certificado: str,
            certificado: str,
            sub_total: Decimal | int,
            total: Decimal | int,
            tipo_de_comprobante: str,
            metodo_de_pago: str,
            lugar_expedicion: str,
            emisor: Emisor | dict,
            receptor: Receptor | dict,
            conceptos: Concepto | dict | Sequence[Concepto | dict],
            impuestos: Impuestos | dict,
            serie: str = None,
            folio: str = None,
            condiciones_de_pago: str = None,
            descuento: Decimal | int = None,
            motivo_descuento: str = None,
            tipo_cambio: str = None,
            moneda: str = None,
            num_cta_pago: str = None,
            folio_fiscal_orig: str = None,
            serie_folio_fiscal_orig: str = None,
            fecha_folio_fiscal_orig: datetime = None,
            monto_folio_fiscal_orig: Decimal | int = None,
            complemento: XElement | Sequence[XElement] = None,
            addenda: XElement | Sequence[XElement] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'Fecha': fecha,
            'Sello': sello,
            'FormaDePago': forma_de_pago,
            'NoCertificado': no_certificado,
            'Certificado': certificado,
            'SubTotal': sub_total,
            'Total': total,
            'TipoDeComprobante': tipo_de_comprobante,
            'MetodoDePago': metodo_de_pago,
            'LugarExpedicion': lugar_expedicion,
            'Emisor': emisor,
            'Receptor': receptor,
            'Conceptos': conceptos,
            'Impuestos': impuestos,
            'Serie': serie,
            'Folio': folio,
            'CondicionesDePago': condiciones_de_pago,
            'Descuento': descuento,
            'MotivoDescuento': motivo_descuento,
            'TipoCambio': tipo_cambio,
            'Moneda': moneda,
            'NumCtaPago': num_cta_pago,
            'FolioFiscalOrig': folio_fiscal_orig,
            'SerieFolioFiscalOrig': serie_folio_fiscal_orig,
            'FechaFolioFiscalOrig': fecha_folio_fiscal_orig,
            'MontoFolioFiscalOrig': monto_folio_fiscal_orig,
            'Complemento': complemento,
            'Addenda': addenda,
        })
        

