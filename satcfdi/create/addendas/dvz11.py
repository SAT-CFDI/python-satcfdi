"""dvz http://www.diverza.com/ns/addenda/diverza/1"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Extra(ScalarMap):
    """
    Tipo definido para determinar cualquier información útil que se requiera expresar en la versión impresa del Comprobante.
    
    :param indicador: Atributo opcional para señalar un valor que sea útil para identificar el atributo extra
    :param atributo: Atributo opcional para especificar el nombre de un atributo adicional que se desee incluir en la Addenda
    :param valor: Dato opcional que especifica el valor del atributo determinado en el elemento extra
    :param prefijo: Valor opcional que puede incorporarse como prefijo para una mejor identificación del elemento extra
    :param sufijo: Valor opcional que puede incorporarse como sufijo para una mejor identificación del elemento extra
    """
    
    def __init__(
            self,
            indicador: str = None,
            atributo: str = None,
            valor: str = None,
            prefijo: str = None,
            sufijo: str = None,
    ): 
        super().__init__({
            'Indicador': indicador,
            'Atributo': atributo,
            'Valor': valor,
            'Prefijo': prefijo,
            'Sufijo': sufijo,
        })
        

class DatosContacto(ScalarMap):
    """
    Tipo de dato para determinar información de datos de contacto como teléfono, email y otros.
    
    :param telefono: Atributo opcional para especificar el teléfono de contacto.
    :param email_comercial: Atributo opcional para especificar el email comerical que se quiera publicar a los clientes.
    :param email_contacto: Atributo opcional para especificar el email de contacto para notificaciones privadas.
    :param web: Atributo opcional para especificar la URL del sitio Web.
    """
    
    def __init__(
            self,
            telefono: str = None,
            email_comercial: str = None,
            email_contacto: str = None,
            web: str = None,
    ): 
        super().__init__({
            'Telefono': telefono,
            'EmailComercial': email_comercial,
            'EmailContacto': email_contacto,
            'Web': web,
        })
        

class Ubicacion(ScalarMap):
    """
    Tipo definido para expresar domicilios o direcciones
    
    :param tax_id: Atributo opcional para colocar la clave de identificación fiscal del receptor.
    :param codigo_sitio: Elemento opcional para especificar el código de sitio del domicilio.
    :param calle: Este atributo opcional sirve para precisar la avenida, calle, camino o carretera donde se da la ubicación.
    :param numero: Este atributo opcional sirve para expresar el número particular en donde se da la ubicación sobre una calle dada.
    :param colonia: Este atributo opcional sirve para precisar la colonia en donde se da la ubicación cuando se desea ser más específico en casos de ubicaciones urbanas.
    :param ciudad: Atributo opcional que sirve para precisar la ciudad o población donde se da la ubicación.
    :param municipio: Atributo opcional que sirve para precisar el municipio o delegación (en el caso del Distrito Federal) en donde se da la ubicación.
    :param estado: Atributo opcional que sirve para precisar el estado o entidad federativa donde se da la ubicación.
    :param pais: Atributo opcional que sirve para precisar el país donde se da la ubicación.
    :param codigo_postal: Atributo opcional que sirve para asentar el código postal en donde se da la ubicación.
    """
    
    def __init__(
            self,
            tax_id: str = None,
            codigo_sitio: str = None,
            calle: str = None,
            numero: str = None,
            colonia: str = None,
            ciudad: str = None,
            municipio: str = None,
            estado: str = None,
            pais: str = None,
            codigo_postal: str = None,
    ): 
        super().__init__({
            'TaxID': tax_id,
            'CodigoSitio': codigo_sitio,
            'Calle': calle,
            'Numero': numero,
            'Colonia': colonia,
            'Ciudad': ciudad,
            'Municipio': municipio,
            'Estado': estado,
            'Pais': pais,
            'CodigoPostal': codigo_postal,
        })
        

class Concepto(ScalarMap):
    """
    Nodo de información para especificar información adicional a un concepto del Comprobante
    
    :param indicador: Atributo opcional para definir un identificador básico que relacione la información de la Addenda con los nodos Concepto del Comprobante
    :param identificador1: Atributo opcional para especificar un identificador especial útil al Concepto
    :param identificador2: Atributo opcional para especificar otro identificador especial útil al Concepto
    :param descripcion_extranjera: Valor opcional si se requeire agregar información descripriva del Concepto en un idioma diferente al español
    :param valor_unitario_moneda_extranjera: Atributo opcional para determinar el Valor Unitario en alguna moneada extranjera
    :param importe_moneda_extranjera: Atributo opcional para determinar el importe total del concepto en una moneda extranjera
    :param mensaje: Atributo opcional para especificar cualquier mensaje de tipo comercial relacionado al Concepto
    :param unidad_medida: Atributo opcional para determinar alguna unidad de medida adicional que se desee especificar en el Concepto
    :param codigo_ean: Atributo opcional para especificar si se desea el código de barras EAN (European Article Number)
    :param sku: Atributo opcional para especificar el 'Stock-keeping unit' o SKU registrado internamente por el negocio
    :param nombre_transportista_c: Atributo opcional para proporcionar el nombre o clave del servicio de transporte usado para el traslado del atrículo definido en el Concepto
    :param numero_entrega_c: Atributo opcional para determinar el número de registro originado en el momento de entrega del producto relacionado al Concepto facturado
    :param fecha_entrega_c: Atributo opcional para indicar la fecha de entrega del producto relacionado al concepto facturado
    :param datos_extra_c: Elemento para determinar datos adicionales que no están contemplados en el esquema pero que se desean especificar en el Comprobante
    """
    
    def __init__(
            self,
            indicador: str = None,
            identificador1: str = None,
            identificador2: str = None,
            descripcion_extranjera: str = None,
            valor_unitario_moneda_extranjera: Decimal | int = None,
            importe_moneda_extranjera: Decimal | int = None,
            mensaje: str = None,
            unidad_medida: str = None,
            codigo_ean: str = None,
            sku: str = None,
            nombre_transportista_c: str = None,
            numero_entrega_c: str = None,
            fecha_entrega_c: date = None,
            datos_extra_c: Extra | dict | Sequence[Extra | dict] = None,
    ): 
        super().__init__({
            'Indicador': indicador,
            'Identificador1': identificador1,
            'Identificador2': identificador2,
            'DescripcionExtranjera': descripcion_extranjera,
            'ValorUnitarioMonedaExtranjera': valor_unitario_moneda_extranjera,
            'ImporteMonedaExtranjera': importe_moneda_extranjera,
            'Mensaje': mensaje,
            'UnidadMedida': unidad_medida,
            'CodigoEAN': codigo_ean,
            'Sku': sku,
            'NombreTransportistaC': nombre_transportista_c,
            'NumeroEntregaC': numero_entrega_c,
            'FechaEntregaC': fecha_entrega_c,
            'DatosExtraC': datos_extra_c,
        })
        

class Conceptos(ScalarMap):
    """
    
    :param concepto: Nodo de información para especificar información adicional a un concepto del Comprobante
    :param numero_conceptos: Atributo opcional definido para especificar el número de líneas de concepto presentes en el documento.
    """
    
    def __init__(
            self,
            concepto: Concepto | dict | Sequence[Concepto | dict],
            numero_conceptos: int = None,
    ): 
        super().__init__({
            'Concepto': concepto,
            'NumeroConceptos': numero_conceptos,
        })
        

class Receptor(ScalarMap):
    """
    Nodo opcional para agregar información relacionada al receptor del documento.
    
    :param comprador: Atributo opcional para colocar la clave ó código del comprador.
    :param num_cliente: Atributo opcional para colocar la clave o número de cliente asignado al receptor por parte del emisor del documento.
    :param datos_contacto_r: Elemento opcional para agregar datos de contacto del receptor.
    :param domicilio_fiscal_r: Elemento opcional para especificar la información del domicilio del receptor.
    :param destino:
    """
    
    def __init__(
            self,
            comprador: str = None,
            num_cliente: str = None,
            datos_contacto_r: DatosContacto | dict = None,
            domicilio_fiscal_r: Ubicacion | dict = None,
            destino: Ubicacion | dict | Sequence[Ubicacion | dict] = None,
    ): 
        super().__init__({
            'Comprador': comprador,
            'NumCliente': num_cliente,
            'DatosContactoR': datos_contacto_r,
            'DomicilioFiscalR': domicilio_fiscal_r,
            'Destino': destino,
        })
        

class SucursalE(ScalarMap):
    """
    Nodo opcional para agregar información de la sucursal en la que fue expedido el documento
    
    :param alias: Atributo opcional para especificar el nombre o clave de la sucursal en la que fue expedido el documento
    :param domicilio_sucursal: Elemento opcional para especificar la información del domicilio de la sucursal en la que fue expedido el documento
    :param datos_contacto: Elemento opcional para especificar datos de contacto de la sucursal en la que fue expedido el documento
    """
    
    def __init__(
            self,
            alias: str = None,
            domicilio_sucursal: Ubicacion | dict = None,
            datos_contacto: DatosContacto | dict = None,
    ): 
        super().__init__({
            'Alias': alias,
            'DomicilioSucursal': domicilio_sucursal,
            'DatosContacto': datos_contacto,
        })
        

class Emisor(ScalarMap):
    """
    Nodo opcional para proporcionar información adicional relacionada al emisor.
    
    :param vendedor: Atributo opcional para indicar el nombre o clave del Agente de Ventas relacionado con el documento
    :param numero_proveedor: Atributo opcional para colocar la clave o número de proveedor que el emisor tiene asignado por su cliente.
    :param tipo_proveedor: Atributo opcional para colocar el tipo de proveedor que el emisor tiene asignado por su cliente.
    :param gln: Atributo opcional para colocar el número GLN del proveedor.
    :param datos_contacto_e: Nodo opcional para agregar información de contacto del emisor
    :param domicilio_fiscal_e: Nodo opcional para agregar información del domicilo fiscal del emisor
    :param domicilio_origen_e: Elemento opcional para especificar la información del domicilio de origen de envío de la mercancía.
    :param sucursal_e: Nodo opcional para agregar información de la sucursal en la que fue expedido el documento
    """
    
    def __init__(
            self,
            vendedor: str = None,
            numero_proveedor: str = None,
            tipo_proveedor: str = None,
            gln: str = None,
            datos_contacto_e: DatosContacto | dict = None,
            domicilio_fiscal_e: Ubicacion | dict = None,
            domicilio_origen_e: Ubicacion | dict = None,
            sucursal_e: SucursalE | dict = None,
    ): 
        super().__init__({
            'Vendedor': vendedor,
            'NumeroProveedor': numero_proveedor,
            'TipoProveedor': tipo_proveedor,
            'Gln': gln,
            'DatosContactoE': datos_contacto_e,
            'DomicilioFiscalE': domicilio_fiscal_e,
            'DomicilioOrigenE': domicilio_origen_e,
            'SucursalE': sucursal_e,
        })
        

class ClavesDescripcion(ScalarMap):
    """
    Nodo opcional para expresar las descripciones de los valores del Comprobante que tienen un catálogo oficial SAT relacionado.
    
    :param c_forma_pago: Atributo opcional para expresar la descripción de la clave del atributo FormaPago del Comprobante conforme al catálogo c_FormaPago.
    :param c_moneda: Atributo opcional para expresar la descripción de la clave del atributo Moneda del Comprobante conforme al catálogo c_Moneda.
    :param c_tipo_de_comprobante: Atributo opcional para expresar la descripción de la clave del atributo TipoDeComprobante del Comprobante conforme al catálogo c_TipoDeComprobante.
    :param c_metodo_pago: Atributo opcional para expresar la descripción de la clave del atributo MetodoPago del Comprobante conforme al catálogo c_MetodoPago.
    :param c_lugar_expedicion: Atributo opcional para expresar la Ciudad y Estado al que corresponda el Código Postal señalado en el atributo LugarExpedicion del Comprobante conforme al catálogo c_CodigoPostal.
    :param c_tipo_relacion: Atributo opcional para expresar la descripción que corresponda a la clave del Tipo de Relación entre CFDIs señalado en el atributo TipoRelacion del nodo CfdiRelacionados del Comprobante conforme al catálogo c_TipoRelacion.
    :param c_regimen_fiscal: Atributo opcional para expresar la descripción que corresponda a la clave del Régimen Fiscal del nodo Emisor del Comprobante conforme al catálogo c_RegimenFiscal.
    :param c_residencia_fiscal: Atributo opcional para expresar la descripción que corresponda a la clave del País del atributo ResidenciaFiscal del nodo Receptor del Comprobante cuando este sea extranjero y conforme al catálogo c_Pais.
    :param c_uso_cfdi: Atributo opcional para expresar la descripción que corresponda a la clave del Uso del CFDI del atributo UsoCFDI del nodo Receptor del Comprobante conforme al catálogo c_UsoCFDI.
    """
    
    def __init__(
            self,
            c_forma_pago: str = None,
            c_moneda: str = None,
            c_tipo_de_comprobante: str = None,
            c_metodo_pago: str = None,
            c_lugar_expedicion: str = None,
            c_tipo_relacion: str = None,
            c_regimen_fiscal: str = None,
            c_residencia_fiscal: str = None,
            c_uso_cfdi: str = None,
    ): 
        super().__init__({
            'CFormaPago': c_forma_pago,
            'CMoneda': c_moneda,
            'CTipoDeComprobante': c_tipo_de_comprobante,
            'CMetodoPago': c_metodo_pago,
            'CLugarExpedicion': c_lugar_expedicion,
            'CTipoRelacion': c_tipo_relacion,
            'CRegimenFiscal': c_regimen_fiscal,
            'CResidenciaFiscal': c_residencia_fiscal,
            'CUsoCFDI': c_uso_cfdi,
        })
        

class Generales(ScalarMap):
    """
    Nodo opcional para proporcionar información general que aplique al documento.
    
    :param tipo_documento: Atributo opcional para indicar el nombre comercial del CFDI descrito en letra. Por ejemplo: Factura, Nota de Crédito, Recibo de Arrendamiento, etc.
    :param total_con_letra: Atributo opcional para indicar el importe total del CFDI descrito en letra.
    :param observaciones: Atributo opcional para agregar cualquier información de texto que sea útil para el CFDI
    :param numero_orden: Atributo opcional para identificar el número de orden comercial relacionado con el documento
    :param nombre_transportista: Atributo opcional para especificar el nombre o identificador del servico de transporte de la mercancía que ampara el documento..
    :param embarque: Atributo opcional para especificar el dato o código de embarque.
    :param numero_entrega: Atributo opcional para identificar el número de la orden de entrega de la mercancía que ampara el documento.
    :param terminos_pago: Atributo opcional para identificar los terminos de Pago del documento.
    :param fecha_entrega: Atributo opcional para identificar la fecha de entrega de la mercancía que ampara el documento.
    :param fecha_tipo_cambio: Atributo opcional para identificar la fecha del tipo de cambio aplicado en el atributo TipoCambio del nodo Comprobante del CFDI cuando la Moneda corresponda a un valor diferente a Pesos Mexicanos.
    """
    
    def __init__(
            self,
            tipo_documento: str = None,
            total_con_letra: str = None,
            observaciones: str = None,
            numero_orden: str = None,
            nombre_transportista: str = None,
            embarque: str = None,
            numero_entrega: str = None,
            terminos_pago: str = None,
            fecha_entrega: date = None,
            fecha_tipo_cambio: date = None,
    ): 
        super().__init__({
            'TipoDocumento': tipo_documento,
            'TotalConLetra': total_con_letra,
            'Observaciones': observaciones,
            'NumeroOrden': numero_orden,
            'NombreTransportista': nombre_transportista,
            'Embarque': embarque,
            'NumeroEntrega': numero_entrega,
            'TerminosPago': terminos_pago,
            'FechaEntrega': fecha_entrega,
            'FechaTipoCambio': fecha_tipo_cambio,
        })
        

class Diverza(CFDI):
    """
    
    :param generales: Nodo opcional para proporcionar información general que aplique al documento.
    :param claves_descripcion: Nodo opcional para expresar las descripciones de los valores del Comprobante que tienen un catálogo oficial SAT relacionado.
    :param emisor: Nodo opcional para proporcionar información adicional relacionada al emisor.
    :param receptor: Nodo opcional para agregar información relacionada al receptor del documento.
    :param conceptos:
    :param complemento:
    """
    
    tag = '{http://www.diverza.com/ns/addenda/diverza/1}diverza'
    version = '1.1'
    
    def __init__(
            self,
            generales: Generales | dict = None,
            claves_descripcion: ClavesDescripcion | dict = None,
            emisor: Emisor | dict = None,
            receptor: Receptor | dict = None,
            conceptos: Conceptos | dict = None,
            complemento: Extra | dict | Sequence[Extra | dict] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'Generales': generales,
            'ClavesDescripcion': claves_descripcion,
            'Emisor': emisor,
            'Receptor': receptor,
            'Conceptos': conceptos,
            'Complemento': complemento,
        })
        

