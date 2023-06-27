"""cce http://www.sat.gob.mx/ComercioExterior"""
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
    :param valor_dolares: Atributo requerido que indica el valor total en dólares de Estados Unidos.
    :param fraccion_arancelaria: Atributo opcional que sirve para expresar la fracción arancelaria correspondiente a la descripción de la mercancía exportada, este dato se vuelve requerido cuando se cuente con él o se esté obligado legalmente a contar con él.
    :param cantidad_aduana: Atributo opcional para precisar la cantidad de bienes en la aduana conforme a la UnidadAduana cuando en el nodo Comprobante:Conceptos:Concepto se hubiera registrado información comercial.
    :param unidad_aduana: Atributo opcional para precisar la unidad de medida aplicable para la cantidad expresada en la mercancía en la aduana.
    :param valor_unitario_aduana: Atributo opcional para precisar el valor o precio unitario del bien en la aduana. Se expresa en dólares de Estados Unidos (USD).
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
    :param estado: Atributo requerido para señalar el estado, entidad, región, comunidad u otra figura análoga en donde se encuentra ubicado el domicilio del destinatario de la mercancía. El catálogo se publicará en el portal del SAT y será conforme con la especificación ISO 3166-2.
    :param pais: Atributo requerido que sirve para precisar el país donde se encuentra ubicado el destinatario de la mercancía. El catálogo se publicará en el portal del SAT y será conforme con la especificación ISO 3166-1.
    :param codigo_postal: Atributo requerido que sirve para asentar el código postal (PO, BOX) en donde se encuentra ubicado el domicilio del destinatario de la mercancía.
    :param numero_exterior: Atributo opcional sirve para expresar el número exterior en donde se ubica el domicilio del destinatario de la mercancía.
    :param numero_interior: Atributo opcional sirve para expresar el número interior, en caso de existir, en donde se ubica el domicilio del destinatario de la mercancía.
    :param colonia: Atributo opcional sirve para expresar la colonia o dato análogo en donde se ubica el domicilio del destinatario de la mercancía.
    :param localidad: Atributo opcional que sirve para precisar la ciudad, población, distrito u otro análogo en donde se ubica el domicilio del destinatario de la mercancía.
    :param referencia: Atributo opcional para expresar una referencia geográfica adicional que permita una más fácil o precisa ubicación del domicilio del destinatario de la mercancía, por ejemplo las coordenadas GPS.
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
    :param rfc: Atributo opcional para expresar el RFC del destinatario de la mercancía exportada.
    :param curp: Atributo opcional para expresar la CURP del destinatario de la mercancía cuando es persona física.
    :param nombre: Atributo opcional para expresar el nombre completo, denominación o razón social del destinatario de la mercancía exportada.
    """
    
    def __init__(
            self,
            domicilio: Domicilio | dict,
            num_reg_id_trib: str = None,
            rfc: str = None,
            curp: str = None,
            nombre: str = None,
    ): 
        super().__init__({
            'Domicilio': domicilio,
            'NumRegIdTrib': num_reg_id_trib,
            'Rfc': rfc,
            'Curp': curp,
            'Nombre': nombre,
        })
        

class Emisor(ScalarMap):
    """
    Nodo opcional para capturar los datos complementarios del emisor del comprobante.
    
    :param curp: Atributo opcional para expresar la CURP del emisor del CFDI cuando es una persona física.
    """
    
    def __init__(
            self,
            curp: str = None,
    ): 
        super().__init__({
            'Curp': curp,
        })
        

class Receptor(ScalarMap):
    """
    Nodo requerido para capturar los datos complementarios del receptor del CFDI.
    
    :param num_reg_id_trib: Atributo requerido para incorporar el número de identificación o registro fiscal del país de residencia para efectos fiscales del receptor del CFDI.
    :param curp: Atributo opcional para expresar la CURP del receptor del CFDI cuando es una persona física.
    """
    
    def __init__(
            self,
            num_reg_id_trib: str,
            curp: str = None,
    ): 
        super().__init__({
            'NumRegIdTrib': num_reg_id_trib,
            'Curp': curp,
        })
        

class ComercioExterior(CFDI):
    """
    Complemento para incorporar la información en el caso de Exportación de Mercancías en definitiva.
    
    :param tipo_operacion: Atributo requerido que indica el tipo de operación de comercio exterior que se realiza, puede ser importación o exportación, A = exportación de servicios. 2 = exportación.
    :param receptor: Nodo requerido para capturar los datos complementarios del receptor del CFDI.
    :param clave_de_pedimento: Atributo que indica la clave de pedimento que se haya declarado conforme al apéndice 2 del anexo 22 de las reglas generales de comercio exterior.
    :param certificado_origen: Atributo derivado de la excepción de certificados de Origen de los Tratados de Libre Comercio que ha celebrado México con diversos países. 0 = No Funge como certificado de origen 1 = Funge como certificado de origen.
    :param num_certificado_origen: Atributo opcional para expresar el folio del certificado de origen o el folio fiscal del CFDI con el que se pagó la expedición del certificado de origen.
    :param numero_exportador_confiable: Atributo opcional que indica el número de exportador confiable, conforme al artículo 22 del Anexo 1 del Tratado de Libre Comercio con la Asociación Europea y a la Decisión de la Comunidad Europea.
    :param incoterm: Atributo que indica la clave del INCOTERM aplicable a la factura.
    :param subdivision: Atributo que indica si la factura tiene o no subdivisión. Valores posibles:0 - no tiene subdivisión,1 - si tiene subdivisión.
    :param observaciones: Atributo opcional en caso de ingresar alguna información adicional, como alguna leyenda que debe incluir el CFDI.
    :param tipo_cambio_usd: Atributo que indica el número de pesos mexicanos que equivalen a un dólar de Estados Unidos, de acuerdo al artículo 20 del Código Fiscal de la Federación.
    :param total_usd: Atributo que indica el importe total del comprobante en dólares de Estados Unidos.
    :param emisor: Nodo opcional para capturar los datos complementarios del emisor del comprobante.
    :param destinatario: Nodo opcional para capturar los datos del destinatario de la mercancía cuando éste sea distinto del receptor del CFDI.
    :param mercancias: Nodo opcional para capturar la información de la declaración de las mercancías exportadas.
    """
    
    tag = '{http://www.sat.gob.mx/ComercioExterior}ComercioExterior'
    version = '1.0'
    
    def __init__(
            self,
            tipo_operacion: str,
            receptor: Receptor | dict,
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
            destinatario: Destinatario | dict = None,
            mercancias: Mercancia | dict | Sequence[Mercancia | dict] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'TipoOperacion': tipo_operacion,
            'Receptor': receptor,
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
            'Destinatario': destinatario,
            'Mercancias': mercancias,
        })
        

