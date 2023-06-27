"""cce11 http://www.sat.gob.mx/ComercioExterior11"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class DescripcionesEspecificas(ScalarMap):
    """
    Nodo opcional que indica la lista de descripciones específicas de la mercancía. Una mercancía puede tener más de una descripción específica.
    
    :param marca: Atributo requerido que indica la marca de la mercancía.
    :param modelo: Atributo opcional que indica el modelo de la mercancía.
    :param sub_modelo: Atributo opcional que indica el submodelo de la mercancía.
    :param numero_serie: Atributo opcional que indica el número de serie de la mercancía.
    """
    
    def __init__(
            self,
            marca: str,
            modelo: str = None,
            sub_modelo: str = None,
            numero_serie: str = None,
    ): 
        super().__init__({
            'Marca': marca,
            'Modelo': modelo,
            'SubModelo': sub_modelo,
            'NumeroSerie': numero_serie,
        })
        

class Mercancia(ScalarMap):
    """
    Nodo requerido para capturar la información de la declaración de cada mercancía exportada.
    
    :param no_identificacion: Atributo requerido que sirve para expresar el número de parte, la clave de identificación que asigna la empresa o el número de serie de la mercancía exportada.
    :param valor_dolares: Atributo requerido que indica el valor total en dólares de Estados Unidos (USD).
    :param fraccion_arancelaria: Atributo condicional que sirve para expresar la clave de la fracción arancelaria correspondiente a la descripción de la mercancía exportada, este dato se vuelve requerido cuando se cuente con él o se esté obligado legalmente a contar con él.Debe ser conforme con el catálogo c_FraccionArancelaria publicado en el portal del SAT en internet.
    :param cantidad_aduana: Atributo opcional para precisar la cantidad de bienes en la aduana conforme a la UnidadAduana cuando en el nodo Comprobante:Conceptos:Concepto se hubiera registrado información comercial.
    :param unidad_aduana: Atributo condicional para precisar la clave de la unidad de medida aplicable para la cantidad expresada en la mercancía en la aduana, conforme con el catálogo c_UnidadAduana publicado en el portal del SAT en internet.
    :param valor_unitario_aduana: Atributo condicional para precisar el valor o precio unitario del bien en la aduana. Se expresa en dólares de Estados Unidos (USD), el cual puede estar registrado hasta centésimas.
    :param descripciones_especificas: Nodo opcional que indica la lista de descripciones específicas de la mercancía. Una mercancía puede tener más de una descripción específica.
    """
    
    def __init__(
            self,
            no_identificacion: str,
            valor_dolares: Decimal | int,
            fraccion_arancelaria: str = None,
            cantidad_aduana: Decimal | int = None,
            unidad_aduana: str = None,
            valor_unitario_aduana: Decimal | int = None,
            descripciones_especificas: DescripcionesEspecificas | dict | Sequence[DescripcionesEspecificas | dict] = None,
    ): 
        super().__init__({
            'NoIdentificacion': no_identificacion,
            'ValorDolares': valor_dolares,
            'FraccionArancelaria': fraccion_arancelaria,
            'CantidadAduana': cantidad_aduana,
            'UnidadAduana': unidad_aduana,
            'ValorUnitarioAduana': valor_unitario_aduana,
            'DescripcionesEspecificas': descripciones_especificas,
        })
        

class Domicilio(ScalarMap):
    """
    Nodo requerido para expresar el domicilio del destinatario de la mercancía.
    
    :param calle: Atributo requerido sirve para precisar la calle en que está ubicado el domicilio del destinatario de la mercancía.
    :param estado: Atributo requerido para señalar el estado, entidad, región, comunidad u otra figura análoga en donde se encuentra ubicado el domicilio del destinatario de la mercancía. El catálogo se publica en el portal del SAT en internet y es conforme con la especificación ISO 3166-2.
    :param pais: Atributo requerido que sirve para precisar la clave del país donde se encuentra ubicado el destinatario de la mercancía, conforme con el catálogo c_Pais publicado en el portal del SAT en internet que está basado en la especificación ISO 3166-1.
    :param codigo_postal: Atributo requerido que sirve para asentar el código postal (PO, BOX) en donde se encuentra ubicado el domicilio del destinatario de la mercancía.
    :param numero_exterior: Atributo opcional sirve para expresar el número exterior en donde se ubica el domicilio del destinatario de la mercancía.
    :param numero_interior: Atributo opcional sirve para expresar el número interior, en caso de existir, en donde se ubica el domicilio del destinatario de la mercancía.
    :param colonia: Atributo opcional sirve para expresar la colonia o dato análogo en donde se ubica el domicilio del destinatario de la mercancía.
    :param localidad: Atributo opcional que sirve para precisar la ciudad, población, distrito u otro análogo en donde se ubica el domicilio del destinatario de la mercancía.
    :param referencia: Atributo opcional para expresar una referencia geográfica adicional que permita una fácil o precisa ubicación del domicilio del destinatario de la mercancía, por ejemplo las coordenadas GPS.
    :param municipio: Atributo opcional que sirve para precisar el municipio, delegación, condado u otro análogo en donde se encuentra ubicado el destinatario de la mercancía.
    """
    
    def __init__(
            self,
            calle: str,
            estado: str,
            pais: str,
            codigo_postal: str,
            numero_exterior: str = None,
            numero_interior: str = None,
            colonia: str = None,
            localidad: str = None,
            referencia: str = None,
            municipio: str = None,
    ): 
        super().__init__({
            'Calle': calle,
            'Estado': estado,
            'Pais': pais,
            'CodigoPostal': codigo_postal,
            'NumeroExterior': numero_exterior,
            'NumeroInterior': numero_interior,
            'Colonia': colonia,
            'Localidad': localidad,
            'Referencia': referencia,
            'Municipio': municipio,
        })
        

class Destinatario(ScalarMap):
    """
    Nodo opcional para capturar los datos del destinatario de la mercancía cuando éste sea distinto del receptor del CFDI.
    
    :param domicilio: Nodo requerido para expresar el domicilio del destinatario de la mercancía.
    :param num_reg_id_trib: Atributo opcional para incorporar el número de identificación o registro fiscal del país de residencia para efectos fiscales del destinatario de la mercancía exportada.
    :param nombre: Atributo opcional para expresar el nombre completo, denominación o razón social del destinatario de la mercancía exportada.
    """
    
    def __init__(
            self,
            domicilio: Domicilio | dict | Sequence[Domicilio | dict],
            num_reg_id_trib: str = None,
            nombre: str = None,
    ): 
        super().__init__({
            'Domicilio': domicilio,
            'NumRegIdTrib': num_reg_id_trib,
            'Nombre': nombre,
        })
        

class Receptor(ScalarMap):
    """
    Nodo condicional para capturar los datos complementarios del receptor del CFDI.
    
    :param num_reg_id_trib: Atributo condicional para incorporar el número de identificación o registro fiscal del país de residencia para efectos fiscales del receptor del CFDI.
    :param domicilio: Nodo requerido para expresar el domicilio del receptor del comprobante.
    """
    
    def __init__(
            self,
            num_reg_id_trib: str = None,
            domicilio: Domicilio | dict = None,
    ): 
        super().__init__({
            'NumRegIdTrib': num_reg_id_trib,
            'Domicilio': domicilio,
        })
        

class Propietario(ScalarMap):
    """
    Nodo condicional para capturar los datos del o los propietarios de la mercancía que se traslada y ésta no sea objeto de enajenación o siéndolo sea a título gratuito, cuando el emisor del CFDI es un tercero.
    
    :param num_reg_id_trib: Atributo requerido para incorporar el número de identificación o registro fiscal del país de residencia para efectos fiscales del propietario de la mercancía trasladada.
    :param residencia_fiscal: Atributo requerido para registrar la clave del país de residencia para efectos fiscales del propietario de la mercancía, conforme con el catálogo c_Pais publicado en el portal del SAT en internet que está basado en la especificación ISO 3166-1.
    """
    
    def __init__(
            self,
            num_reg_id_trib: str,
            residencia_fiscal: str,
    ): 
        super().__init__({
            'NumRegIdTrib': num_reg_id_trib,
            'ResidenciaFiscal': residencia_fiscal,
        })
        

class Emisor(ScalarMap):
    """
    Nodo opcional para capturar los datos complementarios del emisor del comprobante.
    
    :param curp: Atributo condicional para expresar la CURP del emisor del CFDI cuando es una persona física.
    :param domicilio: Nodo condicional para expresar el domicilio del emisor del comprobante, es requerido cuando el complemento se registre en un CFDI 4.0.
    """
    
    def __init__(
            self,
            curp: str = None,
            domicilio: Domicilio | dict = None,
    ): 
        super().__init__({
            'Curp': curp,
            'Domicilio': domicilio,
        })
        

class ComercioExterior(CFDI):
    """
    Complemento para incorporar la información en el caso de Exportación de Mercancías en definitiva.
    
    :param tipo_operacion: Atributo requerido que indica la clave del tipo de operación de Comercio Exterior que se realiza, conforme con el catálogo c_TipoOperacion publicado en el portal del SAT en internet.
    :param motivo_traslado: Atributo condicional que indica la clave del motivo por el cual en la exportación definitiva de mercancías con clave de pedimento A1, éstas no son objeto de enajenación o siéndolo sean a título gratuito, desde el domicilio del emisor hacia el domicilio del receptor o del destinatario. La clave del motivo es conforme con el catálogo c_MotivoTraslado publicado en el portal del SAT en internet.
    :param clave_de_pedimento: Atributo condicional que indica la clave de pedimento que se haya declarado conforme con el catálogo c_ClavePedimento publicado en el portal del SAT en internet.
    :param certificado_origen: Atributo condicional derivado de la excepción de certificados de Origen de los Tratados de Libre Comercio que ha celebrado México con diversos países. 0 = No Funge como certificado de origen 1 = Funge como certificado de origen.
    :param num_certificado_origen: Atributo condicional para expresar el folio del certificado de origen o el folio fiscal del CFDI con el que se pagó la expedición del certificado de origen.
    :param numero_exportador_confiable: Atributo condicional que indica el número de exportador confiable, conforme al artículo 22 del Anexo 1 del Tratado de Libre Comercio con la Asociación Europea y a la Decisión de la Comunidad Europea.
    :param incoterm: Atributo condicional que indica la clave del INCOTERM aplicable a la factura, conforme con el catálogo c_INCOTERM publicado en el portal del SAT en internet.
    :param subdivision: Atributo condicional que indica si la factura tiene o no subdivisión. Valores posibles: 0 - no tiene subdivisión,1 - si tiene subdivisión.
    :param observaciones: Atributo opcional en caso de ingresar alguna información adicional, como alguna leyenda que debe incluir en el CFDI.
    :param tipo_cambio_usd: Atributo condicional que indica el número de pesos mexicanos que equivalen a un dólar de Estados Unidos, de acuerdo al artículo 20 del Código Fiscal de la Federación.
    :param total_usd: Atributo condicional que indica el importe total del comprobante en dólares de Estados Unidos.
    :param emisor: Nodo opcional para capturar los datos complementarios del emisor del comprobante.
    :param propietario: Nodo condicional para capturar los datos del o los propietarios de la mercancía que se traslada y ésta no sea objeto de enajenación o siéndolo sea a título gratuito, cuando el emisor del CFDI es un tercero.
    :param receptor: Nodo condicional para capturar los datos complementarios del receptor del CFDI.
    :param destinatario: Nodo opcional para capturar los datos del destinatario de la mercancía cuando éste sea distinto del receptor del CFDI.
    :param mercancias: Nodo condicional para capturar la información de la declaración de las mercancías exportadas.
    """
    
    tag = '{http://www.sat.gob.mx/ComercioExterior11}ComercioExterior'
    version = '1.1'
    
    def __init__(
            self,
            tipo_operacion: str,
            motivo_traslado: str = None,
            clave_de_pedimento: str = None,
            certificado_origen: int = None,
            num_certificado_origen: str = None,
            numero_exportador_confiable: str = None,
            incoterm: str = None,
            subdivision: int = None,
            observaciones: str = None,
            tipo_cambio_usd: Decimal | int = None,
            total_usd: Decimal | int = None,
            emisor: Emisor | dict = None,
            propietario: Propietario | dict | Sequence[Propietario | dict] = None,
            receptor: Receptor | dict = None,
            destinatario: Destinatario | dict | Sequence[Destinatario | dict] = None,
            mercancias: Mercancia | dict | Sequence[Mercancia | dict] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'TipoOperacion': tipo_operacion,
            'MotivoTraslado': motivo_traslado,
            'ClaveDePedimento': clave_de_pedimento,
            'CertificadoOrigen': certificado_origen,
            'NumCertificadoOrigen': num_certificado_origen,
            'NumeroExportadorConfiable': numero_exportador_confiable,
            'Incoterm': incoterm,
            'Subdivision': subdivision,
            'Observaciones': observaciones,
            'TipoCambioUSD': tipo_cambio_usd,
            'TotalUSD': total_usd,
            'Emisor': emisor,
            'Propietario': propietario,
            'Receptor': receptor,
            'Destinatario': destinatario,
            'Mercancias': mercancias,
        })
        

