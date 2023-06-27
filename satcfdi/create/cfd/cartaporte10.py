"""cartaporte http://www.sat.gob.mx/CartaPorte"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Domicilio(ScalarMap):
    """
    Nodo opcional para registrar el domicilio de la(s) persona(s) a quién(es) se debe notificar de la llegada del medio de transporte con los bienes o mercancías que se trasladan.
    
    :param calle: Atributo requerido que sirve para precisar la calle en que está ubicado el domicilio de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan.
    :param estado: Atributo requerido para precisar el estado, entidad, región, comunidad, u otra figura análoga en donde se encuentra ubicado el domicilio de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan.
    :param pais: Atributo requerido que sirve para precisar la clave del país en donde se encuentra ubicado el domicilio de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan, conforme al catálogo c_Pais publicado en el portal del SAT en Internet que está basado en la especificación ISO 3166-1.
    :param codigo_postal: Atributo requerido para asentar el código postal (PO, BOX) en donde se encuentra ubicado el domicilio de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan.
    :param numero_exterior: Atributo opcional que sirve para expresar el número exterior en donde se ubica el domicilio de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan.
    :param numero_interior: Atributo opcional que sirve para expresar el número interior, en caso de existir, en donde se ubica el domicilio de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan.
    :param colonia: Atributo opcional que sirve para expresar la clave de la colonia o dato análogo en donde se ubica el domicilio de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan.
    :param localidad: Atributo opcional para precisar la clave de la ciudad, población, distrito u análogo en donde se encuentra ubicado el domicilio de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan.
    :param referencia: Atributo opcional para expresar una referencia geográfica adicional que permita una más fácil o precisa ubicación de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan; por ejemplo, las coordenadas GPS.
    :param municipio: Atributo opcional para precisar la clave del municipio, delegación o alcaldía, condado u otro análogo en donde se encuentra ubicado el domicilio de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan.
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
        

class Notificado(ScalarMap):
    """
    Nodo opcional para indicar los datos de identificación de la(s) persona(s) a quién(es) se debe notificar de la llegada del medio de transporte con los bienes o mercancías que se trasladan.
    
    :param rfc_notificado: Atributo condicional para registrar el RFC de la persona a la que se debe notificar del arribo del medio de transporte con los bienes o mercancías que se trasladan.
    :param nombre_notificado: Atributo opcional para registrar el nombre de la persona a la que se debe notificar del arribo del medio de transporte con los bienes o mercancías que se trasladan.
    :param num_reg_id_trib_notificado: Atributo condicional para incorporar el número de identificación o registro fiscal del país de residencia para los efectos fiscales de la persona notificada del arribo del medio de transporte con los bienes o mercancías que se trasladan, cuando sea residente en el extranjero.
    :param residencia_fiscal_notificado: Atributo condicional para registrar la clave del país de residencia para efectos fiscales de la persona notificada del arribo del transporte, conforme con el catálogo c_Pais publicado en el portal del SAT en Internet que está basado en la especificación ISO 3166-1.
    :param domicilio: Nodo opcional para registrar el domicilio de la(s) persona(s) a quién(es) se debe notificar de la llegada del medio de transporte con los bienes o mercancías que se trasladan.
    """
    
    def __init__(
            self,
            rfc_notificado: str = None,
            nombre_notificado: str = None,
            num_reg_id_trib_notificado: str = None,
            residencia_fiscal_notificado: str = None,
            domicilio: Domicilio | dict = None,
    ): 
        super().__init__({
            'RFCNotificado': rfc_notificado,
            'NombreNotificado': nombre_notificado,
            'NumRegIdTribNotificado': num_reg_id_trib_notificado,
            'ResidenciaFiscalNotificado': residencia_fiscal_notificado,
            'Domicilio': domicilio,
        })
        

class Arrendatario(ScalarMap):
    """
    Nodo condicional para indicar los datos del (los) arrendatario(s) del medio de transporte, siempre que el emisor del comprobante sea distinto al dueño del transporte.
    
    :param rfc_arrendatario: Atributo condicional para registrar el RFC del arrendatario del medio de transporte.
    :param nombre_arrendatario: Atributo opcional para registrar el nombre del arrendatario del medio de transporte.
    :param num_reg_id_trib_arrendatario: Atributo condicional para incorporar el número de identificación o registro fiscal del país de residencia para los efectos fiscales del arrendatario del medio de transporte, cuando sea residente en el extranjero.
    :param residencia_fiscal_arrendatario: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del arrendatario del transporte, conforme con el catálogo c_Pais publicado en el portal del SAT en Internet que está basado en la especificación ISO 3166-1.
    :param domicilio: Nodo opcional para registrar el domicilio del arrendatario del transporte.
    """
    
    def __init__(
            self,
            rfc_arrendatario: str = None,
            nombre_arrendatario: str = None,
            num_reg_id_trib_arrendatario: str = None,
            residencia_fiscal_arrendatario: str = None,
            domicilio: Domicilio | dict = None,
    ): 
        super().__init__({
            'RFCArrendatario': rfc_arrendatario,
            'NombreArrendatario': nombre_arrendatario,
            'NumRegIdTribArrendatario': num_reg_id_trib_arrendatario,
            'ResidenciaFiscalArrendatario': residencia_fiscal_arrendatario,
            'Domicilio': domicilio,
        })
        

class Propietario(ScalarMap):
    """
    Nodo condicional para indicar los datos del (los) propietario(s) del medio de transporte, siempre que el emisor del comprobante sea distinto al dueño del transporte.
    
    :param rfc_propietario: Atributo condicional para registrar el RFC del propietario del medio de transporte.
    :param nombre_propietario: Atributo opcional para registrar el nombre del propietario del medio de transporte.
    :param num_reg_id_trib_propietario: Atributo condicional para incorporar el número de identificación o registro fiscal del país de residencia para los efectos fiscales del propietario del transporte, cuando sea residente en el extranjero.
    :param residencia_fiscal_propietario: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del propietario del transporte, conforme con el catálogo c_Pais publicado en el portal del SAT en Internet que está basado en la especificación ISO 3166-1.
    :param domicilio: Nodo opcional para registrar el domicilio del propietario para el traslado de la mercancía.
    """
    
    def __init__(
            self,
            rfc_propietario: str = None,
            nombre_propietario: str = None,
            num_reg_id_trib_propietario: str = None,
            residencia_fiscal_propietario: str = None,
            domicilio: Domicilio | dict = None,
    ): 
        super().__init__({
            'RFCPropietario': rfc_propietario,
            'NombrePropietario': nombre_propietario,
            'NumRegIdTribPropietario': num_reg_id_trib_propietario,
            'ResidenciaFiscalPropietario': residencia_fiscal_propietario,
            'Domicilio': domicilio,
        })
        

class Operador(ScalarMap):
    """
    Nodo requerido para indicar los datos del operador del autotransporte de carga federal en el que se trasladan los bienes o mercancías.
    
    :param rfc_operador: Atributo condicional para registrar el RFC del operador del autotransporte de carga federal en el que se trasladan los bienes o mercancías.
    :param num_licencia: Atributo condicional para expresar el número de folio de la licencia o el permiso otorgado al operador del autotransporte de carga federal en el que se trasladan los bienes o mercancías.
    :param nombre_operador: Atributo opcional para registrar el nombre del operador del autotransporte de carga federal en el que se trasladan los bienes o mercancías.
    :param num_reg_id_trib_operador: Atributo condicional para incorporar el número de identificación o registro fiscal del país de residencia para los efectos fiscales del operador del autotransporte de carga federal en el que se trasladan los bienes o mercancías, cuando sea residente en el extranjero.
    :param residencia_fiscal_operador: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del operador del autotransporte de carga federal en el que se trasladan los bienes o mercancías, conforme con el catálogo c_Pais publicado en el portal del SAT en Internet que está basado en la especificación ISO 3166-1.
    :param domicilio: Nodo opcional para registrar la información del domicilio del operador del autotransporte de carga federal en el que se trasladan los bienes o mercancías.
    """
    
    def __init__(
            self,
            rfc_operador: str = None,
            num_licencia: str = None,
            nombre_operador: str = None,
            num_reg_id_trib_operador: str = None,
            residencia_fiscal_operador: str = None,
            domicilio: Domicilio | dict = None,
    ): 
        super().__init__({
            'RFCOperador': rfc_operador,
            'NumLicencia': num_licencia,
            'NombreOperador': nombre_operador,
            'NumRegIdTribOperador': num_reg_id_trib_operador,
            'ResidenciaFiscalOperador': residencia_fiscal_operador,
            'Domicilio': domicilio,
        })
        

class Operadores(ScalarMap):
    """
    Nodo condicional para indicar los datos del(los) operador(es) del autotransporte de carga federal en el que se trasladan los bienes o mercancías.
    
    :param operador: Nodo requerido para indicar los datos del operador del autotransporte de carga federal en el que se trasladan los bienes o mercancías.
    """
    
    def __init__(
            self,
            operador: Operador | dict | Sequence[Operador | dict],
    ): 
        super().__init__({
            'Operador': operador,
        })
        

class FiguraTransporte(ScalarMap):
    """
    Nodo opcional para indicar los datos de la figura del transporte que interviene en el traslado de los bienes o mercancías, cuando el dueño del medio de transporte es diferente del emisor del comprobante con el complemento carta porte.
    
    :param cve_transporte: Atributo requerido para expresar la clave que identifica el medio por el cual se transportan los bienes o mercancías.
    :param operadores: Nodo condicional para indicar los datos del(los) operador(es) del autotransporte de carga federal en el que se trasladan los bienes o mercancías.
    :param propietario: Nodo condicional para indicar los datos del (los) propietario(s) del medio de transporte, siempre que el emisor del comprobante sea distinto al dueño del transporte.
    :param arrendatario: Nodo condicional para indicar los datos del (los) arrendatario(s) del medio de transporte, siempre que el emisor del comprobante sea distinto al dueño del transporte.
    :param notificado: Nodo opcional para indicar los datos de identificación de la(s) persona(s) a quién(es) se debe notificar de la llegada del medio de transporte con los bienes o mercancías que se trasladan.
    """
    
    def __init__(
            self,
            cve_transporte: str,
            operadores: Operadores | dict | Sequence[Operadores | dict] = None,
            propietario: Propietario | dict | Sequence[Propietario | dict] = None,
            arrendatario: Arrendatario | dict | Sequence[Arrendatario | dict] = None,
            notificado: Notificado | dict | Sequence[Notificado | dict] = None,
    ): 
        super().__init__({
            'CveTransporte': cve_transporte,
            'Operadores': operadores,
            'Propietario': propietario,
            'Arrendatario': arrendatario,
            'Notificado': notificado,
        })
        

class DerechosDePaso(ScalarMap):
    """
    Nodo opcional para registrar los tipos de derechos de paso cubiertos por el transportista en las vías férreas de las cuales no es concesionario o asignatario, así como la distancia establecida en kilómetros.
    
    :param tipo_derecho_de_paso: Atributo requerido para registrar el valor de la clave del derecho de paso pagado por el transportista en las vías férreas de las cuales no es concesionario o asignatario.
    :param kilometraje_pagado: Atributo requerido para registrar el total de kilómetros pagados por el transportista en las vías férreas de las cuales no es concesionario o asignatario con el derecho de paso.
    """
    
    def __init__(
            self,
            tipo_derecho_de_paso: str,
            kilometraje_pagado: Decimal | int,
    ): 
        super().__init__({
            'TipoDerechoDePaso': tipo_derecho_de_paso,
            'KilometrajePagado': kilometraje_pagado,
        })
        

class Contenedor(ScalarMap):
    """
    Nodo opcional para especificar el tipo de contenedor o vagón en el que se trasladan los bienes o mercancías vía férrea.
    
    :param tipo_contenedor: Atributo requerido para registrar la clave con las que se identifica el tipo de contenedor o vagón en el que se traslada los bienes o mercancías.
    :param peso_contenedor_vacio: Atributo requerido para registrar el peso en kilogramos del contenedor vacío en el que se trasladan los bienes o mercancías.
    :param peso_neto_mercancia: Atributo requerido para registrar el peso neto en kilogramos de los bienes o mercancías que trasladan en el contenedor.
    """
    
    def __init__(
            self,
            tipo_contenedor: str,
            peso_contenedor_vacio: Decimal | int,
            peso_neto_mercancia: Decimal | int,
    ): 
        super().__init__({
            'TipoContenedor': tipo_contenedor,
            'PesoContenedorVacio': peso_contenedor_vacio,
            'PesoNetoMercancia': peso_neto_mercancia,
        })
        

class Carro(ScalarMap):
    """
    Nodo requerido para registrar la información que permite identificar los carros en los que se trasladan los bienes o mercancías vía férrea.
    
    :param tipo_carro: Atributo requerido para registrar la clave del tipo de carro utilizado para el traslado de los bienes o mercancías vía férrea.
    :param matricula_carro: Atributo requerido para expresar el número de contenedor, carro de ferrocarril o número económico del vehículo en el que se trasladan los bienes o mercancías vía férrea.
    :param guia_carro: Atributo requerido para expresar el número de guía asignado al contenedor, carro de ferrocarril o vehículo en el que se trasladan los bienes o mercancías vía férrea.
    :param toneladas_netas_carro: Atributo requerido para registrar la cantidad de las toneladas netas contenidas en el contenedor, carro de ferrocarril o vehículo en el que se trasladan los bienes o mercancías vía férrea.
    :param contenedor: Nodo opcional para especificar el tipo de contenedor o vagón en el que se trasladan los bienes o mercancías vía férrea.
    """
    
    def __init__(
            self,
            tipo_carro: str,
            matricula_carro: str,
            guia_carro: str,
            toneladas_netas_carro: Decimal | int,
            contenedor: Contenedor | dict | Sequence[Contenedor | dict] = None,
    ): 
        super().__init__({
            'TipoCarro': tipo_carro,
            'MatriculaCarro': matricula_carro,
            'GuiaCarro': guia_carro,
            'ToneladasNetasCarro': toneladas_netas_carro,
            'Contenedor': contenedor,
        })
        

class TransporteFerroviario(ScalarMap):
    """
    Nodo condicional para registrar la información que permita la identificación del carro o contenedor en el que se transportan los bienes o mercancías vía férrea.
    
    :param tipo_de_servicio: Atributo requerido para registrar la clave del tipo de servicio proporcionado para el traslado de los bienes o mercancías vía férrea.
    :param carro: Nodo requerido para registrar la información que permite identificar los carros en los que se trasladan los bienes o mercancías vía férrea.
    :param nombre_aseg: Atributo opcional para expresar el nombre de la aseguradora que cubre los riesgos para el traslado de los bienes o mercancías vía férrea.
    :param num_poliza_seguro: Atributo opcional para registrar el número de póliza asignado por la aseguradora para la protección e indemnización por responsabilidad civil para el traslado de los bienes o mercancías vía férrea.
    :param concesionario: Atributo condicional para registrar la clave del RFC del concesionario o asignatario del transporte, siempre que el traslado de la mercancía se efectúe por un concesionario diferente al emisor del comprobante.
    :param derechos_de_paso: Nodo opcional para registrar los tipos de derechos de paso cubiertos por el transportista en las vías férreas de las cuales no es concesionario o asignatario, así como la distancia establecida en kilómetros.
    """
    
    def __init__(
            self,
            tipo_de_servicio: str,
            carro: Carro | dict | Sequence[Carro | dict],
            nombre_aseg: str = None,
            num_poliza_seguro: str = None,
            concesionario: str = None,
            derechos_de_paso: DerechosDePaso | dict | Sequence[DerechosDePaso | dict] = None,
    ): 
        super().__init__({
            'TipoDeServicio': tipo_de_servicio,
            'Carro': carro,
            'NombreAseg': nombre_aseg,
            'NumPolizaSeguro': num_poliza_seguro,
            'Concesionario': concesionario,
            'DerechosDePaso': derechos_de_paso,
        })
        

class TransporteAereo(ScalarMap):
    """
    Nodo condicional para registrar la información que permita la identificación del transporte aéreo por medio del cual se trasladan los bienes o mercancías.
    
    :param perm_sct: Atributo requerido para precisar la clave del tipo de permiso proporcionado por la SCT o la autoridad análoga, para el transporte de bienes o mercancías vía aérea.
    :param num_permiso_sct: Atributo requerido para precisar el número de permiso o algún valor análogo proporcionado por la SCT o la autoridad análoga, para el transporte de bienes o mercancías vía aérea.
    :param matricula_aeronave: Atributo requerido para registrar el número de matrícula de la aeronave que opera en territorio nacional y que se compone de valores alfanuméricos más el carácter especial de guion medio “-“, con una longitud de 10 posiciones.
    :param numero_guia: Atributo requerido para registrar el número de guía aérea con el que se trasladan los bienes o mercancías.
    :param codigo_transportista: Atributo requerido para precisar el valor del código que tiene asignado el transportista y debe contener una clave válida del catálogo “catCartaPorte:c_CodigoTransporteAereo”.
    :param nombre_aseg: Atributo opcional para expresar el nombre de la aseguradora que cubre los riesgos del medio que transporta los bienes o mercancías.
    :param num_poliza_seguro: Atributo opcional para registrar el número de póliza asignado por la aseguradora para la protección e indemnización por responsabilidad civil de la aeronave que transporta los bienes o mercancías.
    :param lugar_contrato: Atributo opcional para registrar el lugar, entidad, región, localidad o análoga, donde se celebró el contrato para el traslado de los bienes o mercancías.
    :param rfc_transportista: Atributo opcional para registrar el RFC del transportista de los bienes o mercancías, en caso de que sea diferente del emisor del CFDI.
    :param num_reg_id_trib_transpor: Atributo condicional para incorporar el número de identificación o registro fiscal del país de residencia para los efectos fiscales del transportista, cuando sea residente en el extranjero.
    :param residencia_fiscal_transpor: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del transportista, conforme con el catálogo c_Pais publicado en el portal del SAT en Internet que está basado en la especificación ISO 3166-1.
    :param nombre_transportista: Atributo opcional para registrar el nombre del transportista ya sea nacional o extranjero.
    :param rfc_embarcador: Atributo opcional para registrar el RFC del embarcador de los bienes o mercancías que se trasladan y debe estar en la lista de contribuyentes inscritos no cancelados del SAT (l_RFC).
    :param num_reg_id_trib_embarc: Atributo condicional para incorporar el número de identificación o registro fiscal del país de residencia para los efectos fiscales del embarcador de los bienes o mercancías que se trasladan, cuando sea residente en el extranjero.
    :param residencia_fiscal_embarc: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del embarcador de los bienes o mercancías, conforme con el catálogo c_Pais publicado en el portal del SAT en Internet que está basado en la especificación ISO 3166-1.
    :param nombre_embarcador: Atributo opcional para registrar el nombre del embarcador de los bienes o mercancías que se trasladan, ya sea nacional o extranjero.
    """
    
    def __init__(
            self,
            perm_sct: str,
            num_permiso_sct: str,
            matricula_aeronave: str,
            numero_guia: str,
            codigo_transportista: str,
            nombre_aseg: str = None,
            num_poliza_seguro: str = None,
            lugar_contrato: str = None,
            rfc_transportista: str = None,
            num_reg_id_trib_transpor: str = None,
            residencia_fiscal_transpor: str = None,
            nombre_transportista: str = None,
            rfc_embarcador: str = None,
            num_reg_id_trib_embarc: str = None,
            residencia_fiscal_embarc: str = None,
            nombre_embarcador: str = None,
    ): 
        super().__init__({
            'PermSCT': perm_sct,
            'NumPermisoSCT': num_permiso_sct,
            'MatriculaAeronave': matricula_aeronave,
            'NumeroGuia': numero_guia,
            'CodigoTransportista': codigo_transportista,
            'NombreAseg': nombre_aseg,
            'NumPolizaSeguro': num_poliza_seguro,
            'LugarContrato': lugar_contrato,
            'RFCTransportista': rfc_transportista,
            'NumRegIdTribTranspor': num_reg_id_trib_transpor,
            'ResidenciaFiscalTranspor': residencia_fiscal_transpor,
            'NombreTransportista': nombre_transportista,
            'RFCEmbarcador': rfc_embarcador,
            'NumRegIdTribEmbarc': num_reg_id_trib_embarc,
            'ResidenciaFiscalEmbarc': residencia_fiscal_embarc,
            'NombreEmbarcador': nombre_embarcador,
        })
        

class TransporteMaritimo(ScalarMap):
    """
    Nodo condicional para registrar la información que permita la identificación de la embarcación por medio del cual se transportan los bienes o mercancías, vía marítima.
    
    :param tipo_embarcacion: Atributo requerido para registrar la clave de identificación del transporte del tipo de embarcación que es utilizado para trasladar los bienes o mercancías.
    :param matricula: Atributo requerido para registrar el número de la matrícula o registro de la embarcación que es utilizada para transportar los bienes o mercancías.
    :param numero_omi: Atributo requerido para registrar el número de identificación asignado por la Organización Marítima Internacional a la embarcación encargada de transportar los bienes o mercancías.
    :param nacionalidad_embarc: Atributo requerido para expresar el país correspondiente a la nacionalidad de la embarcación que transporta los bienes o mercancías.
    :param unidades_de_arq_bruto: Atributo requerido para registrar el valor de las unidades de arqueo bruto conforme a las medidas internacionales definidas por el ITC para cada tipo de buque o embarcación en la que se transportan los bienes o mercancías.
    :param tipo_carga: Atributo requerido para especificar el tipo de carga bajo el cual se tipifican los bienes o mercancías que se transportan en la embarcación.
    :param num_cert_itc: Atributo requerido para registrar el número del certificado emitido por la ITC para la embarcación o buque que transporta los bienes o mercancías.
    :param nombre_agente_naviero: Atributo requerido para registrar el nombre del agente naviero autorizado para gestionar el traslado de los bienes o mercancías vía marítima.
    :param num_autorizacion_naviero: Atributo requerido para expresar el número de registro de autorización como agente naviero consignatario emitido por la SCT.
    :param contenedor: Nodo requerido para registrar los datos del contenedor en el que transportan los bienes o mercancías.
    :param perm_sct: Atributo opcional para precisar la clave del tipo de permiso proporcionado por la SCT, el cual debe corresponder a la navegación que se está utilizando para el traslado de los bienes o mercancías registrado en el catálogo catCartaPorte:c_TipoPermiso.
    :param num_permiso_sct: Atributo opcional para precisar el número de permiso proporcionado por la SCT para la navegación.
    :param nombre_aseg: Atributo opcional para expresar el nombre de la aseguradora que cubre el seguro de protección e indemnización por responsabilidad civil de la embarcación.
    :param num_poliza_seguro: Atributo opcional para registrar el número de póliza asignado por la aseguradora para la protección e indemnización por responsabilidad civil de la embarcación.
    :param anio_embarcacion: Atributo opcional para expresar el año de la embarcación en la que se transportan los bienes o mercancías.
    :param nombre_embarc: Atributo opcional para expresar el nombre de la embarcación en la que se transportan los bienes o mercancías.
    :param eslora: Atributo opcional para registrar la longitud de eslora, definida en pies, con la que cuenta la embarcación o buque en el que se transportan los bienes o mercancías.
    :param manga: Atributo opcional para registrar la longitud de manga, definida en pies, con la que cuenta la embarcación o buque en el que se transportan los bienes o mercancías.
    :param calado: Atributo opcional para registrar la longitud del calado, definida en pies, con la que cuenta la embarcación o buque en el que se transportan los bienes o mercancías.
    :param linea_naviera: Atributo opcional para expresar el nombre de la línea naviera autorizada de gestionar el traslado de los bienes o mercancías vía marítima.
    :param num_viaje: Atributo opcional para expresar el número del viaje con el que se identifica el traslado de los bienes o mercancías en el buque o embarcación.
    :param num_conoc_embarc: Atributo opcional para expresar el número de conocimiento de embarque que identifica el traslado de los bienes o mercancías.
    """
    
    def __init__(
            self,
            tipo_embarcacion: str,
            matricula: str,
            numero_omi: str,
            nacionalidad_embarc: str,
            unidades_de_arq_bruto: Decimal | int,
            tipo_carga: str,
            num_cert_itc: str,
            nombre_agente_naviero: str,
            num_autorizacion_naviero: str,
            contenedor: Contenedor | dict | Sequence[Contenedor | dict],
            perm_sct: str = None,
            num_permiso_sct: str = None,
            nombre_aseg: str = None,
            num_poliza_seguro: str = None,
            anio_embarcacion: int = None,
            nombre_embarc: str = None,
            eslora: Decimal | int = None,
            manga: Decimal | int = None,
            calado: Decimal | int = None,
            linea_naviera: str = None,
            num_viaje: str = None,
            num_conoc_embarc: str = None,
    ): 
        super().__init__({
            'TipoEmbarcacion': tipo_embarcacion,
            'Matricula': matricula,
            'NumeroOMI': numero_omi,
            'NacionalidadEmbarc': nacionalidad_embarc,
            'UnidadesDeArqBruto': unidades_de_arq_bruto,
            'TipoCarga': tipo_carga,
            'NumCertITC': num_cert_itc,
            'NombreAgenteNaviero': nombre_agente_naviero,
            'NumAutorizacionNaviero': num_autorizacion_naviero,
            'Contenedor': contenedor,
            'PermSCT': perm_sct,
            'NumPermisoSCT': num_permiso_sct,
            'NombreAseg': nombre_aseg,
            'NumPolizaSeguro': num_poliza_seguro,
            'AnioEmbarcacion': anio_embarcacion,
            'NombreEmbarc': nombre_embarc,
            'Eslora': eslora,
            'Manga': manga,
            'Calado': calado,
            'LineaNaviera': linea_naviera,
            'NumViaje': num_viaje,
            'NumConocEmbarc': num_conoc_embarc,
        })
        

class Remolque(ScalarMap):
    """
    Nodo requerido para expresar la información del remolque o semirremolques que se emplean con el autotransporte para el traslado de los bienes o mercancías.
    
    :param sub_tipo_rem: Atributo requerido para expresar la clave del subtipo de remolque o semirremolques que se emplean con el autotransporte para el traslado de los bienes o mercancías.
    :param placa: Atributo requerido para registrar el valor de la placa vehicular del remolque o semirremolque que es utilizado para transportar los bienes o mercancías, se deben registrar solo los caracteres alfanuméricos, sin guiones y espacios.
    """
    
    def __init__(
            self,
            sub_tipo_rem: str,
            placa: str,
    ): 
        super().__init__({
            'SubTipoRem': sub_tipo_rem,
            'Placa': placa,
        })
        

class IdentificacionVehicular(ScalarMap):
    """
    Nodo requerido para registrar los datos de identificación del autotransporte en el que se trasladan los bienes o mercancías.
    
    :param config_vehicular: Atributo requerido para expresar la clave de nomenclatura del autotransporte que es utilizado para transportar los bienes o mercancías.
    :param placa_vm: Atributo requerido para registrar el valor de la placa vehicular del autotransporte que es utilizado para transportar los bienes o mercancías, se deben registrar solo los caracteres alfanuméricos, sin guiones y espacios.
    :param anio_modelo_vm: Atributo requerido para registrar el año del autotransporte que es utilizado para transportar los bienes o mercancías.
    """
    
    def __init__(
            self,
            config_vehicular: str,
            placa_vm: str,
            anio_modelo_vm: int,
    ): 
        super().__init__({
            'ConfigVehicular': config_vehicular,
            'PlacaVM': placa_vm,
            'AnioModeloVM': anio_modelo_vm,
        })
        

class AutotransporteFederal(ScalarMap):
    """
    Nodo condicional para registrar la información que permita la identificación del autotransporte de carga federal, por medio del cual se transportan los bienes o mercancías, que transitan a través de las carreteras federales del territorio nacional.
    
    :param perm_sct: Atributo requerido para precisar la clave del tipo de permiso proporcionado por la SCT, el cual debe corresponder de acuerdo al tipo de autotransporte utilizado para el traslado de los bienes o mercancías registrado en el catálogo catCartaPorte:c_TipoPermiso.
    :param num_permiso_sct: Atributo requerido para precisar el número del permiso otorgado por la SCT, el cual se debe capturar de acuerdo al tipo de autotransporte utilizado para el traslado de los bienes o mercancías.
    :param nombre_aseg: Atributo requerido para expresar el nombre de la aseguradora que cubre los riesgos del autotransporte utilizado para el traslado de los bienes o mercancías.
    :param num_poliza_seguro: Atributo requerido para registrar el número de póliza asignado por la aseguradora, que cubre los riesgos del autotransporte utilizado para el traslado de los bienes o mercancías.
    :param identificacion_vehicular: Nodo requerido para registrar los datos de identificación del autotransporte en el que se trasladan los bienes o mercancías.
    :param remolques: Nodo opcional para registrar los datos del (los) remolque(s) o semirremolque(s) que se emplean con el autotransporte para el traslado de los bienes o mercancías.
    """
    
    def __init__(
            self,
            perm_sct: str,
            num_permiso_sct: str,
            nombre_aseg: str,
            num_poliza_seguro: str,
            identificacion_vehicular: IdentificacionVehicular | dict,
            remolques: Remolque | dict | Sequence[Remolque | dict] = None,
    ): 
        super().__init__({
            'PermSCT': perm_sct,
            'NumPermisoSCT': num_permiso_sct,
            'NombreAseg': nombre_aseg,
            'NumPolizaSeguro': num_poliza_seguro,
            'IdentificacionVehicular': identificacion_vehicular,
            'Remolques': remolques,
        })
        

class DetalleMercancia(ScalarMap):
    """
    Nodo condicional para registrar mayor detalle de los bienes o mercancías que se transportan y será requerido cuando el traslado sea vía marítima.
    
    :param unidad_peso: Atributo requerido para expresar la clave de unidad de medida estandarizada del peso de los bienes o mercancías que se trasladan.
    :param peso_bruto: Atributo requerido para expresar el peso total bruto de los bienes o mercancías que se trasladan.
    :param peso_neto: Atributo requerido para expresar el peso total neto de los bienes o mercancías que se trasladan.
    :param peso_tara: Atributo requerido para expresar el peso bruto, menos el peso neto de las mercancías que se trasladan.
    :param num_piezas: Atributo opcional para registrar el número de piezas de los bienes o mercancías que se trasladan.
    """
    
    def __init__(
            self,
            unidad_peso: str,
            peso_bruto: Decimal | int,
            peso_neto: Decimal | int,
            peso_tara: Decimal | int,
            num_piezas: int = None,
    ): 
        super().__init__({
            'UnidadPeso': unidad_peso,
            'PesoBruto': peso_bruto,
            'PesoNeto': peso_neto,
            'PesoTara': peso_tara,
            'NumPiezas': num_piezas,
        })
        

class CantidadTransporta(ScalarMap):
    """
    Nodo condicional para registrar la cantidad de los bienes o mercancías que se trasladan en los distintos medios de transporte, que será distribuida o captada en distintos puntos, a fin de identificar el punto de origen y destino de dichos bienes o mercancías, y se podrá registrar este nodo tantas veces sea necesario.
    
    :param cantidad: Atributo requerido para expresar el número de bienes o mercancías que se trasladan en los distintos medios de transporte.
    :param id_origen: Atributo requerido para expresar la clave del identificador del origen de los bienes o mercancías que se trasladan por los distintos medios de transporte, de acuerdo al valor registrado en el nodo “Origen”, del elemento “Ubicacion”.
    :param id_destino: Atributo requerido para expresar la clave del identificador del destino de los bienes o mercancías que se trasladan por los distintos medios de transporte, de acuerdo al valor registrado en el nodo “Origen”, del elemento “Ubicacion”.
    :param cves_transporte: Atributo condicional para expresar la clave que identifica el medio por el cual se transportan los bienes o mercancías, dicha clave debe ser distinta a “05” que corresponde a “Ducto”.
    """
    
    def __init__(
            self,
            cantidad: Decimal | int,
            id_origen: str,
            id_destino: str,
            cves_transporte: str = None,
    ): 
        super().__init__({
            'Cantidad': cantidad,
            'IDOrigen': id_origen,
            'IDDestino': id_destino,
            'CvesTransporte': cves_transporte,
        })
        

class Mercancia(ScalarMap):
    """
    Nodo requerido para registrar información de los bienes o mercancías que se trasladan en los distintos medios de transporte.
    
    :param peso_en_kg: Atributo requerido para indicar el peso en kilogramos de los bienes o mercancías que se trasladan en los distintos medios de transporte.
    :param bienes_transp: Atributo condicional para expresar la clave de producto de los bienes o mercancías que se trasladan en los distintos medios de transporte.
    :param clave_stcc: Atributo opcional para expresar la clave de producto conforme al catálogo de la STCC cuando el medio de transporte es ferroviario.
    :param descripcion: Atributo condicional para describir los bienes o mercancías que se trasladan en los distintos medios de transporte.
    :param cantidad: Atributo condicional para expresar la cantidad de los bienes o mercancías que se trasladan en los distintos medios de transporte.
    :param clave_unidad: Atributo condicional para precisar la clave de unidad de medida estandarizada aplicable para la cantidad de los bienes o mercancías que se trasladan en los distintos medios de transporte. La unidad debe corresponder con la descripción de los bienes o mercancías registrados.
    :param unidad: Atributo opcional para precisar la unidad de medida propia de los bienes o mercancías que se trasladan en los distintos medios de transporte, aplicable para la cantidad. La unidad debe corresponder con la descripción de los bienes o mercancías.
    :param dimensiones: Atributo opcional para expresar las medidas del empaque de los bienes o mercancías que se trasladan vía aérea. Se debe registrar la longitud, la altura y la anchura en centímetros o en pulgadas separados dichos valores por una diagonal, i.e. 30/40/30cm
    :param material_peligroso: Atributo condicional para precisar si los bienes o mercancías que se trasladan son considerados material peligroso.
    :param cve_material_peligroso: Atributo condicional para precisar la clave del tipo de material peligroso que se transporta.
    :param embalaje: Atributo condicional para precisar la clave del tipo de embalaje que se requiere para transportar el material o residuo peligroso.
    :param descrip_embalaje: Atributo opcional para expresar la descripción del embalaje en el que se transporta los bienes o mercancías que se consideran material o residuo peligroso.
    :param valor_mercancia: Atributo condicional para expresar el monto del valor de los bienes o mercancías que se trasladan en los distintos medios de transporte, de acuerdo al valor mercado, el valor pactado en la contraprestación o al valor estimado que determine el contribuyente.
    :param moneda: Atributo condicional para identificar la clave de la moneda utilizada para expresar el valor de los bienes o mercancías que se trasladan en los distintos medios de transporte, cuando se usa moneda nacional se registra MXN, conforme con la especificación ISO 4217.
    :param fraccion_arancelaria: Atributo condicional que sirve para expresar la clave de la fracción arancelaria correspondiente a la descripción de los bienes o mercancías que se trasladan en los distintos medios de transporte como importación o exportación, este dato se vuelve requerido cuando el atributo “EntradaSalidaMerc” contenga información. Debe ser conforme con el catálogo c_FraccionArancelaria publicado en el portal del SAT en Internet.
    :param uuid_comercio_ext: Atributo condicional para expresar el folio fiscal o UUID del comprobante de comercio exterior que se relaciona, este dato se vuelve requerido cuando el atributo “EntradaSalidaMerc” contenga el valor “Salida”.
    :param cantidad_transporta: Nodo condicional para registrar la cantidad de los bienes o mercancías que se trasladan en los distintos medios de transporte, que será distribuida o captada en distintos puntos, a fin de identificar el punto de origen y destino de dichos bienes o mercancías, y se podrá registrar este nodo tantas veces sea necesario.
    :param detalle_mercancia: Nodo condicional para registrar mayor detalle de los bienes o mercancías que se transportan y será requerido cuando el traslado sea vía marítima.
    """
    
    def __init__(
            self,
            peso_en_kg: Decimal | int,
            bienes_transp: str = None,
            clave_stcc: str = None,
            descripcion: str = None,
            cantidad: Decimal | int = None,
            clave_unidad: str = None,
            unidad: str = None,
            dimensiones: str = None,
            material_peligroso: str = None,
            cve_material_peligroso: str = None,
            embalaje: str = None,
            descrip_embalaje: str = None,
            valor_mercancia: Decimal | int = None,
            moneda: str = None,
            fraccion_arancelaria: str = None,
            uuid_comercio_ext: str = None,
            cantidad_transporta: CantidadTransporta | dict | Sequence[CantidadTransporta | dict] = None,
            detalle_mercancia: DetalleMercancia | dict = None,
    ): 
        super().__init__({
            'PesoEnKg': peso_en_kg,
            'BienesTransp': bienes_transp,
            'ClaveSTCC': clave_stcc,
            'Descripcion': descripcion,
            'Cantidad': cantidad,
            'ClaveUnidad': clave_unidad,
            'Unidad': unidad,
            'Dimensiones': dimensiones,
            'MaterialPeligroso': material_peligroso,
            'CveMaterialPeligroso': cve_material_peligroso,
            'Embalaje': embalaje,
            'DescripEmbalaje': descrip_embalaje,
            'ValorMercancia': valor_mercancia,
            'Moneda': moneda,
            'FraccionArancelaria': fraccion_arancelaria,
            'UUIDComercioExt': uuid_comercio_ext,
            'CantidadTransporta': cantidad_transporta,
            'DetalleMercancia': detalle_mercancia,
        })
        

class Mercancias(ScalarMap):
    """
    Nodo requerido para registrar la información de los bienes o mercancías que se trasladan en los distintos medios de transporte.
    
    :param num_total_mercancias: Atributo requerido para expresar el número total de los bienes o mercancías que se trasladan en los distintos medios de transporte, identificándose por cada nodo "Mercancia" registrado en el complemento.
    :param mercancia: Nodo requerido para registrar información de los bienes o mercancías que se trasladan en los distintos medios de transporte.
    :param peso_bruto_total: Atributo condicional para expresar la suma del peso bruto total de los bienes o mercancías que se trasladan por transporte ferroviario y aéreo.
    :param unidad_peso: Atributo condicional para expresar la clave de unidad de medida estandarizada del peso de los bienes o mercancías que se trasladan vía férrea y aérea.
    :param peso_neto_total: Atributo condicional para registrar la suma de los valores registrados en el atributo “PesoNeto” del nodo “DetalleMercancia” del elemento “Mercancia”.
    :param cargo_por_tasacion: Atributo opcional para expresar el importe pagado por la tasación de los bienes o mercancías que se trasladan vía aérea.
    :param autotransporte_federal: Nodo condicional para registrar la información que permita la identificación del autotransporte de carga federal, por medio del cual se transportan los bienes o mercancías, que transitan a través de las carreteras federales del territorio nacional.
    :param transporte_maritimo: Nodo condicional para registrar la información que permita la identificación de la embarcación por medio del cual se transportan los bienes o mercancías, vía marítima.
    :param transporte_aereo: Nodo condicional para registrar la información que permita la identificación del transporte aéreo por medio del cual se trasladan los bienes o mercancías.
    :param transporte_ferroviario: Nodo condicional para registrar la información que permita la identificación del carro o contenedor en el que se transportan los bienes o mercancías vía férrea.
    """
    
    def __init__(
            self,
            num_total_mercancias: int,
            mercancia: Mercancia | dict | Sequence[Mercancia | dict],
            peso_bruto_total: Decimal | int = None,
            unidad_peso: str = None,
            peso_neto_total: Decimal | int = None,
            cargo_por_tasacion: Decimal | int = None,
            autotransporte_federal: AutotransporteFederal | dict = None,
            transporte_maritimo: TransporteMaritimo | dict = None,
            transporte_aereo: TransporteAereo | dict = None,
            transporte_ferroviario: TransporteFerroviario | dict = None,
    ): 
        super().__init__({
            'NumTotalMercancias': num_total_mercancias,
            'Mercancia': mercancia,
            'PesoBrutoTotal': peso_bruto_total,
            'UnidadPeso': unidad_peso,
            'PesoNetoTotal': peso_neto_total,
            'CargoPorTasacion': cargo_por_tasacion,
            'AutotransporteFederal': autotransporte_federal,
            'TransporteMaritimo': transporte_maritimo,
            'TransporteAereo': transporte_aereo,
            'TransporteFerroviario': transporte_ferroviario,
        })
        

class Destino(ScalarMap):
    """
    Nodo condicional para registrar la información detallada del Destino de los bienes o mercancías que se trasladan.
    
    :param fecha_hora_prog_llegada: Atributo requerido para la expresión de la fecha y hora en la que estima arriben a su destino los bienes o mercancías. Se expresa en la forma AAAA-MM-DDThh:mm:ss.
    :param id_destino: Atributo condicional para registrar una clave que sirva para identificar el punto de llegada de los bienes o mercancías que se trasladan por los distintos medios de transporte, mediante un folio, el cual estará compuesto de la siguiente forma: el acrónimo “DE” seguido de 6 dígitos numéricos asignados por el contribuyente que emite el comprobante para su identificación.
    :param rfc_destinatario: Atributo condicional para registrar el RFC del destinatario al que se le entregarán los bienes o mercancías que se trasladan.
    :param nombre_destinatario: Atributo opcional para registrar el nombre del destinatario de los bienes o mercancías que se trasladan.
    :param num_reg_id_trib: Atributo condicional para incorporar el número de identificación o registro fiscal del país de residencia para los efectos fiscales del destinatario de los bienes o mercancías que se trasladan, cuando sea residente en el extranjero.
    :param residencia_fiscal: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del destinatario de los bienes o mercancías, conforme con el catálogo c_Pais publicado en el portal del SAT en Internet que está basado en la especificación ISO 3166-1.
    :param num_estacion: Atributo condicional para registrar la clave del número de la estación de llegada por la que se trasladan los bienes o mercancías en los distintos medios de transporte, esto de acuerdo al valor de la columna Clave identificación que permite asociarla al tipo de transporte.
    :param nombre_estacion: Atributo condicional para registrar el nombre de la estación por la que se trasladan los bienes o mercancías en los distintos medios de transporte.
    :param navegacion_trafico: Atributo condicional para registrar el tipo de puerto por el que se documentan los bienes o mercancías vía marítima.
    """
    
    def __init__(
            self,
            fecha_hora_prog_llegada: datetime,
            id_destino: str = None,
            rfc_destinatario: str = None,
            nombre_destinatario: str = None,
            num_reg_id_trib: str = None,
            residencia_fiscal: str = None,
            num_estacion: str = None,
            nombre_estacion: str = None,
            navegacion_trafico: str = None,
    ): 
        super().__init__({
            'FechaHoraProgLlegada': fecha_hora_prog_llegada,
            'IDDestino': id_destino,
            'RFCDestinatario': rfc_destinatario,
            'NombreDestinatario': nombre_destinatario,
            'NumRegIdTrib': num_reg_id_trib,
            'ResidenciaFiscal': residencia_fiscal,
            'NumEstacion': num_estacion,
            'NombreEstacion': nombre_estacion,
            'NavegacionTrafico': navegacion_trafico,
        })
        

class Origen(ScalarMap):
    """
    Nodo condicional para registrar la información detallada del Origen de los bienes o mercancías que se trasladan.
    
    :param fecha_hora_salida: Atributo requerido para la expresión de la fecha y hora estimada en la que salen los bienes o mercancías del origen. Se expresa en la forma AAAA-MM-DDThh:mm:ss.
    :param id_origen: Atributo condicional para registrar una clave que sirva para identificar el punto de salida de los bienes o mercancías que se trasladan por los distintos medios de transporte, mediante un folio, el cual estará compuesto de la siguiente forma: el acrónimo “OR” seguido de 6 dígitos numéricos asignados por el contribuyente que emite el comprobante para su identificación.
    :param rfc_remitente: Atributo condicional para registrar el RFC del remitente de los bienes o mercancías que se trasladan.
    :param nombre_remitente: Atributo opcional para registrar el nombre del remitente de los bienes o mercancías que se trasladan.
    :param num_reg_id_trib: Atributo condicional para incorporar el número de identificación o registro fiscal del país de residencia para los efectos fiscales del remitente de los bienes o mercancías que se trasladan, cuando sea residente en el extranjero.
    :param residencia_fiscal: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del remitente de los bienes o mercancías, conforme con el catálogo c_Pais publicado en el portal del SAT en Internet que está basado en la especificación ISO 3166-1.
    :param num_estacion: Atributo condicional para registrar la clave del número de la estación de salida por la que se trasladan los bienes o mercancías en los distintos medios de transporte, esto de acuerdo al valor de la columna Clave identificación que permite asociarla al tipo de transporte.
    :param nombre_estacion: Atributo condicional para registrar el nombre de la estación por la que se trasladan los bienes o mercancías en los distintos medios de transporte.
    :param navegacion_trafico: Atributo condicional para registrar el tipo de puerto por el que se documentan los bienes o mercancías vía marítima.
    """
    
    def __init__(
            self,
            fecha_hora_salida: datetime,
            id_origen: str = None,
            rfc_remitente: str = None,
            nombre_remitente: str = None,
            num_reg_id_trib: str = None,
            residencia_fiscal: str = None,
            num_estacion: str = None,
            nombre_estacion: str = None,
            navegacion_trafico: str = None,
    ): 
        super().__init__({
            'FechaHoraSalida': fecha_hora_salida,
            'IDOrigen': id_origen,
            'RFCRemitente': rfc_remitente,
            'NombreRemitente': nombre_remitente,
            'NumRegIdTrib': num_reg_id_trib,
            'ResidenciaFiscal': residencia_fiscal,
            'NumEstacion': num_estacion,
            'NombreEstacion': nombre_estacion,
            'NavegacionTrafico': navegacion_trafico,
        })
        

class Ubicacion(ScalarMap):
    """
    Nodo requerido para registrar la ubicación que sirve para reflejar el domicilio del origen y/o destino parcial o final que tienen los bienes o mercancías que se trasladan por distintos medios de transporte.
    
    :param tipo_estacion: Atributo condicional para precisar el tipo de estación por el que pasan los bienes o mercancías durante su traslado en los distintos medios de transporte.
    :param distancia_recorrida: Atributo condicional para registrar la distancia recorrida en kilómetros de la ubicación de Origen a la de Destino parcial o final, de los distintos medios de transporte que trasladan los bienes o mercancías.
    :param origen: Nodo condicional para registrar la información detallada del Origen de los bienes o mercancías que se trasladan.
    :param destino: Nodo condicional para registrar la información detallada del Destino de los bienes o mercancías que se trasladan.
    :param domicilio: Nodo condicional para registrar información del domicilio de origen y/o destino de los bienes o mercancías que se trasladan en los distintos medios de transporte.
    """
    
    def __init__(
            self,
            tipo_estacion: str = None,
            distancia_recorrida: Decimal | int = None,
            origen: Origen | dict = None,
            destino: Destino | dict = None,
            domicilio: Domicilio | dict = None,
    ): 
        super().__init__({
            'TipoEstacion': tipo_estacion,
            'DistanciaRecorrida': distancia_recorrida,
            'Origen': origen,
            'Destino': destino,
            'Domicilio': domicilio,
        })
        

class CartaPorte(CFDI):
    """
    Complemento para incorporar al Comprobante Fiscal Digital por Internet (CFDI), la información relacionada a los bienes o mercancías, ubicaciones de origen, puntos intermedios y destino, así como lo referente al medio por el que se transportan; ya sea por vía terrestre (carretera federal o líneas férreas), aérea, marítima o fluvial; además de incluir el traslado de Hidrocarburos y Petrolíferos.
    
    :param transp_internac: Atributo requerido para expresar si los bienes o mercancías que son transportadas ingresan o salen del territorio nacional.
    :param ubicaciones: Nodo requerido para registrar las distintas ubicaciones que sirven para reflejar el domicilio del origen y/o destino que tienen los bienes o mercancías que se trasladan por distintos medios de transporte.
    :param mercancias: Nodo requerido para registrar la información de los bienes o mercancías que se trasladan en los distintos medios de transporte.
    :param entrada_salida_merc: Atributo condicional para precisar si los bienes o mercancías ingresan o salen del territorio nacional.
    :param via_entrada_salida: Atributo condicional para precisar la vía de ingreso o salida de los bienes o mercancías en territorio nacional.
    :param total_dist_rec: Atributo condicional para registrar la suma de las distancias recorridas en kilómetros, registradas en el atributo “Ubicaciones:Ubicacion:DistanciaRecorrida” para el traslado de los bienes o mercancías.
    :param figura_transporte: Nodo opcional para indicar los datos de la figura del transporte que interviene en el traslado de los bienes o mercancías, cuando el dueño del medio de transporte es diferente del emisor del comprobante con el complemento carta porte.
    """
    
    tag = '{http://www.sat.gob.mx/CartaPorte}CartaPorte'
    version = '1.0'
    
    def __init__(
            self,
            transp_internac: str,
            ubicaciones: Ubicacion | dict | Sequence[Ubicacion | dict],
            mercancias: Mercancias | dict,
            entrada_salida_merc: str = None,
            via_entrada_salida: str = None,
            total_dist_rec: Decimal | int = None,
            figura_transporte: FiguraTransporte | dict = None,
    ): 
        super().__init__({
            'Version': self.version,
            'TranspInternac': transp_internac,
            'Ubicaciones': ubicaciones,
            'Mercancias': mercancias,
            'EntradaSalidaMerc': entrada_salida_merc,
            'ViaEntradaSalida': via_entrada_salida,
            'TotalDistRec': total_dist_rec,
            'FiguraTransporte': figura_transporte,
        })
        

