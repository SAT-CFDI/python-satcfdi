"""cartaporte31 http://www.sat.gob.mx/CartaPorte31"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Domicilio(ScalarMap):
    """
    Nodo opcional para registrar información del domicilio del(los) tipo(s) de figura transporte que intervenga(n) en el traslado de los bienes y/o mercancías.
    
    :param estado: Atributo requerido para registrar el estado, entidad, región, comunidad, o dato análogo en donde se encuentra ubicado el domicilio del(los) tipo(s) de figura transporte.
    :param pais: Atributo requerido que sirve para registrar la clave del país en donde se encuentra ubicado el domicilio del(los) tipo(s) de figura transporte, conforme al catálogo c_Pais del CFDI publicado en el portal del SAT en Internet de acuerdo a la especificación ISO 3166-1.
    :param codigo_postal: Atributo requerido para registrar el código postal en donde se encuentra ubicado el domicilio del(los) tipo(s) de figura transporte.
    :param calle: Atributo opcional que sirve para registrar la calle en la que está ubicado el domicilio del(los) tipo(s) de figura transporte.
    :param numero_exterior: Atributo opcional que sirve para registrar el número exterior en donde se ubica el domicilio del(los) tipo(s) de figura transporte.
    :param numero_interior: Atributo opcional que sirve para registrar el número interior, en caso de existir, en donde se ubica el domicilio del(los) tipo(s) de figura transporte.
    :param colonia: Atributo opcional que sirve para expresar la clave de la colonia o dato análogo en donde se ubica el domicilio del(los) tipo(s) de figura transporte.
    :param localidad: Atributo opcional para registrar la clave de la ciudad, población, distrito o dato análogo de donde se encuentra ubicado el domicilio del(los) tipo(s) de figura transporte.
    :param referencia: Atributo opcional para registrar una referencia geográfica adicional que permita una fácil o precisa ubicación del domicilio del(los) tipo(s) de figura transporte; por ejemplo, las coordenadas del GPS.
    :param municipio: Atributo opcional para registrar la clave del municipio, delegación o alcaldía, condado o dato análogo en donde se encuentra ubicado el domicilio del(los) tipo(s) de figura transporte.
    """
    
    def __init__(
            self,
            estado: str,
            pais: str,
            codigo_postal: str,
            calle: str = None,
            numero_exterior: str = None,
            numero_interior: str = None,
            colonia: str = None,
            localidad: str = None,
            referencia: str = None,
            municipio: str = None,
    ): 
        super().__init__({
            'Estado': estado,
            'Pais': pais,
            'CodigoPostal': codigo_postal,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'NumeroInterior': numero_interior,
            'Colonia': colonia,
            'Localidad': localidad,
            'Referencia': referencia,
            'Municipio': municipio,
        })
        

class TiposFigura(ScalarMap):
    """
    Nodo condicional para indicar los datos del(los) tipo(s) de figura(s) que participan en el traslado de los bienes y/o mercancías en los distintos medios de transporte.
    
    :param tipo_figura: Atributo requerido para registrar la clave de la figura de transporte que interviene en el traslado de los bienes y/o mercancías.
    :param nombre_figura: Atributo requerido para registrar el nombre de la figura de transporte que interviene en el traslado de los bienes y/o mercancías.
    :param rfc_figura: Atributo condicional para registrar el RFC de la figura de transporte que interviene en el traslado de los bienes y/o mercancías.
    :param num_licencia: Atributo condicional para expresar el número de la licencia o el permiso otorgado al operador del autotransporte de carga en el que realiza el traslado de los bienes y/o mercancías.
    :param num_reg_id_trib_figura: Atributo condicional para registrar el número de identificación o registro fiscal del país de residencia de la figura de transporte que interviene en el traslado de los bienes y/o mercancías, cuando se trate de residentes en el extranjero para los efectos fiscales correspondientes.
    :param residencia_fiscal_figura: Atributo condicional para registrar la clave del país de residencia de la figura de transporte que interviene en el traslado de los bienes y/o mercancías para los efectos fiscales correspondientes.
    :param partes_transporte: Nodo condicional para indicar los datos de las partes del transporte de las cuales el emisor del comprobante es distinto al dueño de las mismas, por ejemplo: vehículos, máquinas, contenedores, plataformas, entre otros, etc; mismos que son utilizados para el traslado de los bienes y/o mercancías.
    :param domicilio: Nodo opcional para registrar información del domicilio del(los) tipo(s) de figura transporte que intervenga(n) en el traslado de los bienes y/o mercancías.
    """
    
    def __init__(
            self,
            tipo_figura: str,
            nombre_figura: str,
            rfc_figura: str = None,
            num_licencia: str = None,
            num_reg_id_trib_figura: str = None,
            residencia_fiscal_figura: str = None,
            partes_transporte: str | Sequence[str] = None,
            domicilio: Domicilio | dict = None,
    ): 
        super().__init__({
            'TipoFigura': tipo_figura,
            'NombreFigura': nombre_figura,
            'RFCFigura': rfc_figura,
            'NumLicencia': num_licencia,
            'NumRegIdTribFigura': num_reg_id_trib_figura,
            'ResidenciaFiscalFigura': residencia_fiscal_figura,
            'PartesTransporte': partes_transporte,
            'Domicilio': domicilio,
        })
        

class DerechosDePaso(ScalarMap):
    """
    Nodo opcional para registrar los tipos de derechos de paso cubiertos por el transportista en las vías férreas de las cuales no es concesionario o asignatario, así como la distancia establecida en kilómetros.
    
    :param tipo_derecho_de_paso: Atributo requerido para registrar la clave del derecho de paso pagado por el transportista en las vías férreas de las cuales no es concesionario o asignatario.
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
    Nodo condicional para especificar el tipo de contenedor o vagón en el que se trasladan los bienes y/o mercancías por vía férrea.
    
    :param tipo_contenedor: Atributo requerido para registrar la clave con la que se identifica al tipo de contenedor o el vagón en el que se realiza el traslado de los bienes y/o mercancías.
    :param peso_contenedor_vacio: Atributo requerido para registrar en kilogramos, el peso del contenedor vacío en el que se trasladan los bienes y/o mercancías.
    :param peso_neto_mercancia: Atributo requerido para registrar en kilogramos el peso neto de los bienes y/o mercancías que son trasladados en el contenedor.
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
    Nodo requerido para registrar la información que permite identificar el (los) carro(s) en el (los) que se trasladan los bienes y/o mercancías por vía férrea.
    
    :param tipo_carro: Atributo requerido para registrar la clave del tipo de carro utilizado para el traslado de los bienes y/o mercancías por vía férrea.
    :param matricula_carro: Atributo requerido para registrar el número de contenedor, carro de ferrocarril o número económico del vehículo en el que se trasladan los bienes y/o mercancías por vía férrea.
    :param guia_carro: Atributo requerido para registrar el número de guía asignado al contenedor, carro de ferrocarril o vehículo, en el que se trasladan los bienes y/o mercancías por vía férrea.
    :param toneladas_netas_carro: Atributo requerido para registrar la cantidad de las toneladas netas depositadas en el contenedor, carro de ferrocarril o vehículo en el que se trasladan los bienes y/o mercancías por vía férrea.
    :param contenedor: Nodo condicional para especificar el tipo de contenedor o vagón en el que se trasladan los bienes y/o mercancías por vía férrea.
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
    Nodo condicional para registrar la información que permita la identificación del carro o contenedor en el que se trasladan los bienes y/o mercancías por vía férrea.
    
    :param tipo_de_servicio: Atributo requerido para registrar la clave del tipo de servicio utilizado para el traslado de los bienes y/o mercancías por vía férrea.
    :param tipo_de_trafico: Atributo requerido para registrar la clave del tipo de tráfico (interrelación entre concesionarios) para realizar el traslado de los bienes y/o mercancías por vía férrea dentro del territorio nacional.
    :param carro: Nodo requerido para registrar la información que permite identificar el (los) carro(s) en el (los) que se trasladan los bienes y/o mercancías por vía férrea.
    :param nombre_aseg: Atributo opcional para registrar el nombre de la aseguradora que cubre los riesgos para el traslado de los bienes y/o mercancías por vía férrea.
    :param num_poliza_seguro: Atributo opcional para registrar el número de póliza asignada por la aseguradora para la protección e indemnización por responsabilidad civil en el traslado de los bienes y/o mercancías que se realiza por vía férrea.
    :param derechos_de_paso: Nodo opcional para registrar los tipos de derechos de paso cubiertos por el transportista en las vías férreas de las cuales no es concesionario o asignatario, así como la distancia establecida en kilómetros.
    """
    
    def __init__(
            self,
            tipo_de_servicio: str,
            tipo_de_trafico: str,
            carro: Carro | dict | Sequence[Carro | dict],
            nombre_aseg: str = None,
            num_poliza_seguro: str = None,
            derechos_de_paso: DerechosDePaso | dict | Sequence[DerechosDePaso | dict] = None,
    ): 
        super().__init__({
            'TipoDeServicio': tipo_de_servicio,
            'TipoDeTrafico': tipo_de_trafico,
            'Carro': carro,
            'NombreAseg': nombre_aseg,
            'NumPolizaSeguro': num_poliza_seguro,
            'DerechosDePaso': derechos_de_paso,
        })
        

class TransporteAereo(ScalarMap):
    """
    Nodo condicional para registrar la información que permita la identificación del transporte aéreo por medio del cual se trasladan los bienes y/o mercancías.
    
    :param perm_sct: Atributo requerido para registrar la clave del permiso proporcionado por la Secretaría de Infraestructura, Comunicaciones y Transportes (SICT), o la autoridad análoga, la cual debe corresponder con la aeronave que se está utilizando para realizar el traslado de los bienes y/o mercancías por vía aérea.
    :param num_permiso_sct: Atributo requerido para registrar el número de permiso o valor análogo proporcionado por la Secretaría de Infraestructura, Comunicaciones y Transportes (SICT), o la autoridad análoga, según corresponda, para el transporte de bienes y/o mercancías por vía aérea.
    :param numero_guia: Atributo requerido para registrar el número de guía aérea con el que se trasladan los bienes y/o mercancías.
    :param codigo_transportista: Atributo requerido para registrar el valor del código que tiene asignado el transportista el cual debe contener alguna de las claves contenidas en el catálogo correspondiente.
    :param matricula_aeronave: Atributo opcional para registrar el número de la matrícula de la aeronave con la que se realiza el traslado de los bienes y/o mercancías en territorio nacional el cual tiene una longitud de 10 posiciones y se compone de valores alfanuméricos, más el carácter especial denominado guion medio “-“.
    :param nombre_aseg: Atributo opcional para registrar el nombre de la aseguradora que cubre los riesgos de la aeronave con la que transportan los bienes y/o mercancías.
    :param num_poliza_seguro: Atributo opcional para registrar el número de póliza asignado por la aseguradora que cubre la protección e indemnización por responsabilidad civil de la aeronave que transporta los bienes y/o mercancías.
    :param lugar_contrato: Atributo opcional para registrar el lugar, entidad, región, localidad o análogo, donde se celebró el contrato para realizar el traslado de los bienes y/o mercancías.
    :param rfc_embarcador: Atributo opcional para registrar el RFC del embarcador de los bienes y/o mercancías que se trasladan.
    :param num_reg_id_trib_embarc: Atributo condicional para incorporar el número de identificación o registro fiscal del país de residencia cuando el embarcador sea residente en el extranjero para los efectos fiscales correspondientes de los bienes y/o mercancías que se trasladan.
    :param residencia_fiscal_embarc: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del embarcador de los bienes y/o mercancías.
    :param nombre_embarcador: Atributo opcional para registrar el nombre del embarcador de los bienes y/o mercancías que se trasladan, ya sea nacional o extranjero.
    """
    
    def __init__(
            self,
            perm_sct: str,
            num_permiso_sct: str,
            numero_guia: str,
            codigo_transportista: str,
            matricula_aeronave: str = None,
            nombre_aseg: str = None,
            num_poliza_seguro: str = None,
            lugar_contrato: str = None,
            rfc_embarcador: str = None,
            num_reg_id_trib_embarc: str = None,
            residencia_fiscal_embarc: str = None,
            nombre_embarcador: str = None,
    ): 
        super().__init__({
            'PermSCT': perm_sct,
            'NumPermisoSCT': num_permiso_sct,
            'NumeroGuia': numero_guia,
            'CodigoTransportista': codigo_transportista,
            'MatriculaAeronave': matricula_aeronave,
            'NombreAseg': nombre_aseg,
            'NumPolizaSeguro': num_poliza_seguro,
            'LugarContrato': lugar_contrato,
            'RFCEmbarcador': rfc_embarcador,
            'NumRegIdTribEmbarc': num_reg_id_trib_embarc,
            'ResidenciaFiscalEmbarc': residencia_fiscal_embarc,
            'NombreEmbarcador': nombre_embarcador,
        })
        

class RemolqueCCP(ScalarMap):
    """
    Nodo requerido para expresar la información del(los) remolque(s) o semirremolque(s) que se adapta(n) al autotransporte que realizó el traslado de los bienes y/o mercancías registrado en el CFDI con complemento Carta Porte, únicamente aplica para traslado mediante ferri.
    
    :param sub_tipo_rem_ccp: Atributo requerido para expresar la clave del subtipo de remolque o semirremolques que se emplean con el autotransporte que realizó el traslado de los bienes y/o mercancías registrado en el CFDI con complemento Carta Porte, únicamente aplica para traslado mediante ferri.
    :param placa_ccp: Atributo requerido para registrar los caracteres alfanuméricos, sin guiones ni espacios de la placa del remolque o semirremolque registrado en el CFDI con complemento Carta Porte, únicamente aplica para traslado mediante ferri.
    """
    
    def __init__(
            self,
            sub_tipo_rem_ccp: str,
            placa_ccp: str,
    ): 
        super().__init__({
            'SubTipoRemCCP': sub_tipo_rem_ccp,
            'PlacaCCP': placa_ccp,
        })
        

class TransporteMaritimo(ScalarMap):
    """
    Nodo condicional para registrar la información que permita la identificación de la embarcación a través de la cual se trasladan los bienes y/o mercancías por vía marítima.
    
    :param tipo_embarcacion: Atributo requerido para registrar la clave de identificación del tipo de embarcación que es utilizado para trasladar los bienes y/o mercancías.
    :param matricula: Atributo requerido para registrar el número de la matrícula o registro de la embarcación que es utilizada para transportar los bienes y/o mercancías.
    :param numero_omi: Atributo requerido para registrar el número de identificación asignado por la Organización Marítima Internacional, a la embarcación encargada de transportar los bienes y/o mercancías.
    :param nacionalidad_embarc: Atributo requerido para registrar la clave del país correspondiente a la nacionalidad de la embarcación que transporta los bienes y/o mercancías.
    :param unidades_de_arq_bruto: Atributo requerido para registrar el valor de las unidades de arqueo bruto conforme a las medidas internacionales definidas por el ITC para cada tipo de buque o embarcación en la que se transportan los bienes y/o mercancías.
    :param tipo_carga: Atributo requerido para especificar el tipo de carga en el cual se clasifican los bienes y/o mercancías que se transportan en la embarcación.
    :param nombre_agente_naviero: Atributo requerido para registrar el nombre del agente naviero consignatario autorizado para gestionar el traslado de los bienes y/o mercancías por vía marítima.
    :param num_autorizacion_naviero: Atributo requerido para expresar el número de la autorización como agente naviero consignatario emitida por la autoridad correspondiente.
    :param perm_sct: Atributo opcional para registrar la clave del permiso proporcionado por la Secretaría de Infraestructura, Comunicaciones y Transportes (SICT), la cual debe corresponder con la embarcación que se está utilizando para el traslado de los bienes y/o mercancías, de acuerdo al catálogo correspondiente.
    :param num_permiso_sct: Atributo opcional para registrar el número del permiso otorgado por la Secretaría de Infraestructura, Comunicaciones y Transportes (SICT), a la embarcación utilizada para el traslado de los bienes y/o mercancías.
    :param nombre_aseg: Atributo opcional para registrar el nombre de la aseguradora que cubre la protección e indemnización por responsabilidad civil de la embarcación en el traslado de los bienes y/o mercancías.
    :param num_poliza_seguro: Atributo opcional para registrar el número de póliza asignada por la aseguradora que cubre la protección e indemnización por responsabilidad civil de la embarcación en el traslado de los bienes y/o mercancías.
    :param anio_embarcacion: Atributo opcional para registrar el año de la embarcación en la que se transportan los bienes y/o mercancías.
    :param nombre_embarc: Atributo opcional para registrar el nombre de la embarcación en la que se realiza el traslado de los bienes y/o mercancías.
    :param eslora: Atributo opcional para registrar la longitud de eslora, definida en pies, con la que cuenta la embarcación o el buque en el que se transportan los bienes y/o mercancías.
    :param manga: Atributo opcional para registrar la longitud de manga, definida en pies, con la que cuenta la embarcación o el buque en el que se transportan los bienes y/o mercancías.
    :param calado: Atributo opcional para registrar la longitud del calado, definida en pies, con la que cuenta la embarcación o el buque en el que se transportan los bienes y/o mercancías.
    :param puntal: Atributo opcional para registrar la longitud del puntal, definida en pies, con la que cuenta la embarcación o el buque en el que se transportan los bienes y/o mercancías.
    :param linea_naviera: Atributo opcional para registrar el nombre de la línea naviera autorizada de gestionar el traslado de los bienes y/o mercancías por vía marítima.
    :param num_viaje: Atributo opcional para registrar el número del viaje con el que se identifica el traslado de los bienes y/o mercancías en el buque o la embarcación.
    :param num_conoc_embarc: Atributo opcional para registrar el número de conocimiento de embarque con el que se identifica el traslado de los bienes y/o mercancías.
    :param permiso_temp_navegacion: Atributo condicional para registrar el permiso temporal de navegación de la embarcación o buque que transporta los bienes y/o mercancías.
    :param contenedor: Nodo opcional para registrar los datos del contenedor en el que se transportan los bienes y/o mercancías.
    """
    
    def __init__(
            self,
            tipo_embarcacion: str,
            matricula: str,
            numero_omi: str,
            nacionalidad_embarc: str,
            unidades_de_arq_bruto: Decimal | int,
            tipo_carga: str,
            nombre_agente_naviero: str,
            num_autorizacion_naviero: str,
            perm_sct: str = None,
            num_permiso_sct: str = None,
            nombre_aseg: str = None,
            num_poliza_seguro: str = None,
            anio_embarcacion: int = None,
            nombre_embarc: str = None,
            eslora: Decimal | int = None,
            manga: Decimal | int = None,
            calado: Decimal | int = None,
            puntal: Decimal | int = None,
            linea_naviera: str = None,
            num_viaje: str = None,
            num_conoc_embarc: str = None,
            permiso_temp_navegacion: str = None,
            contenedor: Contenedor | dict | Sequence[Contenedor | dict] = None,
    ): 
        super().__init__({
            'TipoEmbarcacion': tipo_embarcacion,
            'Matricula': matricula,
            'NumeroOMI': numero_omi,
            'NacionalidadEmbarc': nacionalidad_embarc,
            'UnidadesDeArqBruto': unidades_de_arq_bruto,
            'TipoCarga': tipo_carga,
            'NombreAgenteNaviero': nombre_agente_naviero,
            'NumAutorizacionNaviero': num_autorizacion_naviero,
            'PermSCT': perm_sct,
            'NumPermisoSCT': num_permiso_sct,
            'NombreAseg': nombre_aseg,
            'NumPolizaSeguro': num_poliza_seguro,
            'AnioEmbarcacion': anio_embarcacion,
            'NombreEmbarc': nombre_embarc,
            'Eslora': eslora,
            'Manga': manga,
            'Calado': calado,
            'Puntal': puntal,
            'LineaNaviera': linea_naviera,
            'NumViaje': num_viaje,
            'NumConocEmbarc': num_conoc_embarc,
            'PermisoTempNavegacion': permiso_temp_navegacion,
            'Contenedor': contenedor,
        })
        

class Remolque(ScalarMap):
    """
    Nodo requerido para expresar la información del(los) remolque(s) o semirremolque(s) que se adapta(n) al autotransporte para realizar el traslado de los bienes y/o mercancías.
    
    :param sub_tipo_rem: Atributo requerido para expresar la clave del subtipo de remolque o semirremolques que se emplean con el autotransporte para el traslado de los bienes y/o mercancías.
    :param placa: Atributo requerido para registrar los caracteres alfanuméricos, sin guiones ni espacios de la placa vehicular del remolque o semirremolque que es utilizado para transportar los bienes y/o mercancías.
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
        

class Seguros(ScalarMap):
    """
    Nodo requerido para registrar los datos de las pólizas de seguro que cubren los riesgos en el traslado de los bienes y/o mercancías.
    
    :param asegura_resp_civil: Atributo requerido para registrar el nombre de la aseguradora que cubre los riesgos por responsabilidad civil del autotransporte utilizado para el traslado de los bienes y/o mercancías.
    :param poliza_resp_civil: Atributo requerido para registrar el número de póliza asignado por la aseguradora, que cubre los riesgos por responsabilidad civil del autotransporte utilizado para el traslado de los bienes y/o mercancías.
    :param asegura_med_ambiente: Atributo condicional para registrar el nombre de la aseguradora, que cubre los posibles daños al medio ambiente cuando exista al menos una mercancía tipificada como material peligroso se debe registrar la información del atributo “AseguraMedAmbiente” (aplicable para los transportistas de materiales, residuos o remanentes y desechos peligrosos.
    :param poliza_med_ambiente: Atributo condicional para registrar el número de póliza asignado por la aseguradora, que cubre los posibles daños al medio ambiente cuando exista al menos una mercancía tipificada como material peligroso se debe registrar la información del atributo “AseguraMedAmbiente” (aplicable para los transportistas de materiales, residuos o remanentes y desechos peligrosos).
    :param asegura_carga: Atributo opcional para registrar el nombre de la aseguradora que cubre los riesgos de la carga (bienes y/o mercancías) del autotransporte utilizado para el traslado.
    :param poliza_carga: Atributo opcional para expresar el número de póliza asignado por la aseguradora que cubre los riesgos de la carga (bienes y/o mercancías) del autotransporte utilizado para el traslado.
    :param prima_seguro: Atributo opcional para registrar el valor del importe por el cargo adicional convenido entre el transportista y el cliente, el cual será igual al valor de la prima del seguro contratado, conforme a lo establecido en la cláusula novena del Acuerdo por el que se homologa la Carta de Porte regulada por la Ley de Caminos, Puentes y Autotransporte Federal, con el complemento Carta Porte que debe acompañar al Comprobante Fiscal Digital por Internet (CFDI).
    """
    
    def __init__(
            self,
            asegura_resp_civil: str,
            poliza_resp_civil: str,
            asegura_med_ambiente: str = None,
            poliza_med_ambiente: str = None,
            asegura_carga: str = None,
            poliza_carga: str = None,
            prima_seguro: Decimal | int = None,
    ): 
        super().__init__({
            'AseguraRespCivil': asegura_resp_civil,
            'PolizaRespCivil': poliza_resp_civil,
            'AseguraMedAmbiente': asegura_med_ambiente,
            'PolizaMedAmbiente': poliza_med_ambiente,
            'AseguraCarga': asegura_carga,
            'PolizaCarga': poliza_carga,
            'PrimaSeguro': prima_seguro,
        })
        

class IdentificacionVehicular(ScalarMap):
    """
    Nodo requerido para registrar los datos de identificación del autotransporte en el que se trasladan los bienes y/o mercancías.
    
    :param config_vehicular: Atributo requerido para expresar la clave de nomenclatura del autotransporte que es utilizado para transportar los bienes y/o mercancías.
    :param peso_bruto_vehicular: Atributo requerido para indicar en toneladas el peso bruto vehicular permitido del autotransporte de acuerdo a la NOM-SCT-012-2017 que es utilizado para realizar el traslado de los bienes y/o mercancías.
    :param placa_vm: Atributo requerido para registrar solo los caracteres alfanuméricos, sin guiones ni espacios de la placa vehicular del autotransporte que es utilizado para transportar los bienes y/o mercancías.
    :param anio_modelo_vm: Atributo requerido para registrar el año del autotransporte que es utilizado para transportar los bienes y/o mercancías.
    """
    
    def __init__(
            self,
            config_vehicular: str,
            peso_bruto_vehicular: Decimal | int,
            placa_vm: str,
            anio_modelo_vm: int,
    ): 
        super().__init__({
            'ConfigVehicular': config_vehicular,
            'PesoBrutoVehicular': peso_bruto_vehicular,
            'PlacaVM': placa_vm,
            'AnioModeloVM': anio_modelo_vm,
        })
        

class Autotransporte(ScalarMap):
    """
    Nodo condicional para registrar la información que permita la identificación del autotransporte de carga, por medio del cual se trasladan los bienes y/o mercancías, que transitan a través de las carreteras del territorio nacional.
    
    :param perm_sct: Atributo requerido para registrar la clave del tipo de permiso proporcionado por la Secretaría de Infraestructura, Comunicaciones y Transportes (SICT) o la autoridad análoga, el cual debe corresponder con el tipo de autotransporte utilizado para el traslado de los bienes y/o mercancías de acuerdo al catálogo correspondiente.
    :param num_permiso_sct: Atributo requerido para registrar el número del permiso otorgado por la Secretaría de Infraestructura, Comunicaciones y Transportes (SICT) o la autoridad correspondiente, al autotransporte utilizado para el traslado de los bienes y/o mercancías.
    :param identificacion_vehicular: Nodo requerido para registrar los datos de identificación del autotransporte en el que se trasladan los bienes y/o mercancías.
    :param seguros: Nodo requerido para registrar los datos de las pólizas de seguro que cubren los riesgos en el traslado de los bienes y/o mercancías.
    :param remolques: Nodo condicional para registrar los datos del(los) remolque(s) o semirremolque(s) que se adaptan al autotransporte para realizar el traslado de los bienes y/o mercancías.
    """
    
    def __init__(
            self,
            perm_sct: str,
            num_permiso_sct: str,
            identificacion_vehicular: IdentificacionVehicular | dict,
            seguros: Seguros | dict,
            remolques: Remolque | dict | Sequence[Remolque | dict] = None,
    ): 
        super().__init__({
            'PermSCT': perm_sct,
            'NumPermisoSCT': num_permiso_sct,
            'IdentificacionVehicular': identificacion_vehicular,
            'Seguros': seguros,
            'Remolques': remolques,
        })
        

class DetalleMercancia(ScalarMap):
    """
    Nodo condicional para registrar especificaciones de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    
    :param unidad_peso_merc: Atributo requerido para registrar la clave de la unidad de medida estandarizada del peso de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    :param peso_bruto: Atributo requerido para registrar el peso bruto total de los bienes y/o mercancías que se trasladan a través de los diferentes medios de transporte.
    :param peso_neto: Atributo requerido para registrar el peso neto total de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    :param peso_tara: Atributo requerido para registrar el peso bruto, menos el peso neto de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    :param num_piezas: Atributo opcional para registrar el número de piezas de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    """
    
    def __init__(
            self,
            unidad_peso_merc: str,
            peso_bruto: Decimal | int,
            peso_neto: Decimal | int,
            peso_tara: Decimal | int,
            num_piezas: int = None,
    ): 
        super().__init__({
            'UnidadPesoMerc': unidad_peso_merc,
            'PesoBruto': peso_bruto,
            'PesoNeto': peso_neto,
            'PesoTara': peso_tara,
            'NumPiezas': num_piezas,
        })
        

class CantidadTransporta(ScalarMap):
    """
    Nodo opcional para registrar la cantidad de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte, que será captada o distribuida en distintos puntos, a fin de identificar el punto de origen y destino correspondiente.
    
    :param cantidad: Atributo requerido para expresar el número de bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    :param id_origen: Atributo requerido para expresar la clave del identificador del origen de los bienes y/o mercancías que se trasladan por los distintos medios de transporte, de acuerdo al valor registrado en el atributo “IDUbicacion”, del nodo “Ubicacion”.
    :param id_destino: Atributo requerido para registrar la clave del identificador del destino de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte, de acuerdo al valor registrado en el atributo “IDUbicacion”, del nodo “Ubicacion”.
    :param cves_transporte: Atributo condicional para indicar la clave a través de la cual se identifica el medio por el que se transportan los bienes y/o mercancías.
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
        

class GuiasIdentificacion(ScalarMap):
    """
    Nodo condicional para registrar la información del(los) número(s) de guía(s) que se encuentre(n) asociado(s) al(los) paquete(s) que se traslada(n) dentro del territorio nacional.
    
    :param numero_guia_identificacion: Atributo requerido para expresar el número de guía de cada paquete que se encuentra asociado con el traslado de los bienes y/o mercancías en territorio nacional.
    :param descrip_guia_identificacion: Atributo requerido para expresar la descripción del contenido del paquete o carga registrada en la guía, o en el número de identificación, que se encuentra asociado con el traslado de los bienes y/o mercancías dentro del territorio nacional.
    :param peso_guia_identificacion: Atributo requerido para indicar en kilogramos, el peso del paquete o carga que se está trasladando en territorio nacional y que se encuentra registrado en la guía o el número de identificación correspondiente.
    """
    
    def __init__(
            self,
            numero_guia_identificacion: str,
            descrip_guia_identificacion: str,
            peso_guia_identificacion: Decimal | int,
    ): 
        super().__init__({
            'NumeroGuiaIdentificacion': numero_guia_identificacion,
            'DescripGuiaIdentificacion': descrip_guia_identificacion,
            'PesoGuiaIdentificacion': peso_guia_identificacion,
        })
        

class DocumentacionAduanera(ScalarMap):
    """
    Nodo condicional para registrar la información del(los) documento(s) aduanero(s) que se encuentra(n) asociado(s) al traslado de los bienes y/o mercancías por los distintos medios de transporte de procedencia extranjera para acreditar la legal estancia o tenencia durante su traslado en territorio nacional.
    
    :param tipo_documento: Atributo requerido para expresar el tipo de documento aduanero que se encuentra asociado al traslado de los bienes y/o mercancías de procedencia extranjera durante su traslado en territorio nacional.
    :param num_pedimento: Atributo condicional para expresar el número de pedimento de importación que se encuentra asociado con el traslado de los bienes y/o mercancías de procedencia extranjera para acreditar la legal estancia y tenencia durante su traslado en territorio nacional, el cual se expresa en el siguiente formato: últimos 2 dígitos del año de validación seguidos por dos espacios, 2 dígitos de la aduana de despacho seguidos por dos espacios, 4 dígitos del número de la patente seguidos por dos espacios, 1 dígito que corresponde al último dígito del año en curso, salvo que se trate de un pedimento consolidado iniciado en el año inmediato anterior o del pedimento original de una rectificación, seguido de 6 dígitos de la numeración progresiva por aduana.
    :param ident_doc_aduanero: Atributo condicional para expresar el identificador o folio del documento aduanero que se encuentra asociado al traslado de los bienes y/o mercancías de procedencia extranjera para acreditar la legal estancia o tenencia durante su traslado en territorio nacional.
    :param rfc_impo: Atributo condicional para expresar el RFC del importador de los bienes y/o mercancías que fue registrado en la documentación aduanera correspondiente y este se encuentre en la lista de RFC inscritos no cancelados del SAT (l_RFC).
    """
    
    def __init__(
            self,
            tipo_documento: str,
            num_pedimento: str = None,
            ident_doc_aduanero: str = None,
            rfc_impo: str = None,
    ): 
        super().__init__({
            'TipoDocumento': tipo_documento,
            'NumPedimento': num_pedimento,
            'IdentDocAduanero': ident_doc_aduanero,
            'RFCImpo': rfc_impo,
        })
        

class Mercancia(ScalarMap):
    """
    Nodo requerido para registrar detalladamente la información de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    
    :param bienes_transp: Atributo requerido para registrar la clave de producto de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    :param descripcion: Atributo requerido para detallar las características de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    :param cantidad: Atributo requerido para expresar la cantidad total de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    :param clave_unidad: Atributo requerido para registrar la clave de la unidad de medida estandarizada aplicable para la cantidad de los bienes y/o mercancías que se trasladan en los distintos medios de transporte. La unidad debe corresponder con la descripción de los bienes y/o mercancías registrados.
    :param peso_en_kg: Atributo requerido para indicar en kilogramos el peso estimado de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    :param clave_stcc: Atributo opcional para expresar la clave de producto de la STCC (por sus siglas en inglés, Standard Transportation Commodity Code), cuando el medio de transporte utilizado para el traslado de los bienes y/o mercancías sea ferroviario.
    :param unidad: Atributo opcional para registrar la unidad de medida propia para la cantidad de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte. La unidad debe corresponder con la descripción de los bienes y/o mercancías.
    :param dimensiones: Atributo opcional para expresar las medidas del empaque de los bienes y/o mercancías que se trasladan en los distintos medios de transporte. Se debe registrar la longitud, la altura y la anchura en centímetros o en pulgadas, separados dichos valores con una diagonal, i.e. 30/40/30cm.
    :param material_peligroso: Atributo condicional para precisar que los bienes y/o mercancías que se trasladan son considerados o clasificados como material peligroso.
    :param cve_material_peligroso: Atributo condicional para indicar la clave del tipo de material peligroso que se transporta de acuerdo a la NOM-002-SCT/2011.
    :param embalaje: Atributo condicional para precisar la clave del tipo de embalaje que se requiere para transportar el material o residuo peligroso.
    :param descrip_embalaje: Atributo opcional para expresar la descripción del embalaje de los bienes y/o mercancías que se trasladan y que se consideran material o residuo peligroso.
    :param sector_cofepris: Atributo opcional para expresar la clasificación del producto que se traslada a través de los distintos medios de transporte y que debe contar con autorización por la autoridad correspondiente.
    :param nombre_ingrediente_activo: Atributo condicional para expresar el nombre común del ingrediente activo de los precursores, químicos de uso dual, plaguicidas o fertilizantes que se trasladan a través de los distintos medios de transporte.
    :param nom_quimico: Atributo condicional para expresar el nombre de la sustancia activa de los precursores, químicos de uso dual o sustancias tóxicas que se traslada a través de los distintos medios de transporte.
    :param denominacion_generica_prod: Atributo condicional para expresar el fármaco o la sustancia activa del medicamento, psicotrópico o estupefaciente que se traslada a través de los distintos medios de transporte.
    :param denominacion_distintiva_prod: Atributo condicional para expresar la marca con la que se comercializa el producto o nombre que le asigna el laboratorio o fabricante a sus especialidades farmacéuticas con el fin de distinguirlas de otras similares del medicamento, psicotrópico o estupefaciente que se traslada a través de los distintos medios de transporte.
    :param fabricante: Atributo condicional para expresar el nombre o razón social del establecimiento que realiza la fabricación o manufactura del medicamento, precursor, químico de uso dual, psicotrópico o estupefaciente que se traslada a través de los distintos medios de transporte.
    :param fecha_caducidad: Atributo condicional para registrar la fecha de caducidad del medicamento, psicotrópico o estupefaciente; o para expresar la fecha de reanálisis del precursor o químico de uso dual que se traslada a través de los distintos medios de transporte. Se expresa en la forma AAAA-MM-DD.
    :param lote_medicamento: Atributo condicional para expresar la denominación que identifica y confiere trazabilidad del medicamento, precursor, químico de uso dual, psicotrópico o estupefaciente elaborado en un ciclo de producción, bajo condiciones equivalentes de operación y durante un periodo.
    :param forma_farmaceutica: Atributo condicional para expresar la forma farmacéutica o mezcla del medicamento, precursor, químico de uso dual, psicotrópico o estupefaciente que presenta ciertas características físicas para su adecuada dosificación, conservación y administración.
    :param condiciones_esp_transp: Atributo condicional para expresar la condición en la cual es necesario mantener el medicamento, precursor, químico de uso dual, psicotrópicos o estupefacientes durante el traslado y almacenamiento.
    :param registro_sanitario_folio_autorizacion: Atributo condicional para expresar el registro sanitario o folio de autorización con el que cuenta la empresa para el traslado del medicamento, psicotrópico o estupefaciente.
    :param permiso_importacion: Atributo condicional para registrar el folio del permiso de importación con el que cuenta el medicamento, precursor, químico de uso dual, psicotrópico o estupefaciente.
    :param folio_impo_vucem: Atributo condicional para registrar el número de folio de importación VUCEM para la identificación del documento, para el traslado de medicamentos, precursores o químicos de uso dual, sustancias tóxicas, plaguicidas o fertilizantes.
    :param num_cas: Atributo condicional para expresar el número Chemical Abstracts Service (CAS) con el que se identifica el compuesto químico de la sustancia tóxica.
    :param razon_social_emp_imp: Atributo condicional para expresar el nombre o razón social de la empresa importadora de las sustancias tóxicas.
    :param num_reg_san_plag_cofepris: Atributo condicional para expresar el número de registro sanitario para plaguicidas o fertilizantes cuya importación, comercialización y uso están permitidos en México, mismo que emite la Comisión Intersecretarial para el Control del Proceso y Uso de Plaguicidas, Fertilizantes y Sustancias Tóxicas (CICLOPLAFEST).
    :param datos_fabricante: Atributo condicional para registrar el país y nombre o razón social de quien produce o fabrica el ingrediente activo del plaguicida o fertilizante.
    :param datos_formulador: Atributo condicional para registrar el país y nombre o razón social de quien formula el ingrediente activo del plaguicida o fertilizante.
    :param datos_maquilador: Atributo condicional para registrar el país y nombre o razón social de quien maquila el ingrediente activo del plaguicida o fertilizante.
    :param uso_autorizado: Atributo condicional para registrar el uso autorizado del plaguicida o fertilizante de acuerdo a la regulación del país.
    :param valor_mercancia: Atributo condicional para expresar el monto del valor de los bienes y/o mercancías que se trasladan en los distintos medios de transporte, de acuerdo al valor mercado, al valor pactado en la contraprestación o bien al valor estimado que determine el contribuyente.
    :param moneda: Atributo condicional para identificar la clave de la moneda utilizada para expresar el valor de los bienes y/o mercancías que se trasladan en los distintos medios de transporte. Cuando se usa moneda nacional se registra MXN, de acuerdo a la especificación ISO 4217.
    :param fraccion_arancelaria: Atributo opcional que sirve para expresar la clave de la fracción arancelaria que corresponde con la descripción de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    :param uuid_comercio_ext: Atributo opcional para expresar el folio fiscal (UUID) del comprobante de comercio exterior que se relaciona.
    :param tipo_materia: Atributo condicional para expresar el estado de la materia o producto al realizar una operación de comercio exterior a través de los distintos medios de transporte.
    :param descripcion_materia: Atributo condicional para expresar la descripción del estado de la materia o producto al realizar una operación de comercio exterior a través de los distintos medios de transporte.
    :param documentacion_aduanera: Nodo condicional para registrar la información del(los) documento(s) aduanero(s) que se encuentra(n) asociado(s) al traslado de los bienes y/o mercancías por los distintos medios de transporte de procedencia extranjera para acreditar la legal estancia o tenencia durante su traslado en territorio nacional.
    :param guias_identificacion: Nodo condicional para registrar la información del(los) número(s) de guía(s) que se encuentre(n) asociado(s) al(los) paquete(s) que se traslada(n) dentro del territorio nacional.
    :param cantidad_transporta: Nodo opcional para registrar la cantidad de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte, que será captada o distribuida en distintos puntos, a fin de identificar el punto de origen y destino correspondiente.
    :param detalle_mercancia: Nodo condicional para registrar especificaciones de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    """
    
    def __init__(
            self,
            bienes_transp: str,
            descripcion: str,
            cantidad: Decimal | int,
            clave_unidad: str,
            peso_en_kg: Decimal | int,
            clave_stcc: str = None,
            unidad: str = None,
            dimensiones: str = None,
            material_peligroso: str = None,
            cve_material_peligroso: str = None,
            embalaje: str = None,
            descrip_embalaje: str = None,
            sector_cofepris: str = None,
            nombre_ingrediente_activo: str = None,
            nom_quimico: str = None,
            denominacion_generica_prod: str = None,
            denominacion_distintiva_prod: str = None,
            fabricante: str = None,
            fecha_caducidad: date = None,
            lote_medicamento: str = None,
            forma_farmaceutica: str = None,
            condiciones_esp_transp: str = None,
            registro_sanitario_folio_autorizacion: str = None,
            permiso_importacion: str = None,
            folio_impo_vucem: str = None,
            num_cas: str = None,
            razon_social_emp_imp: str = None,
            num_reg_san_plag_cofepris: str = None,
            datos_fabricante: str = None,
            datos_formulador: str = None,
            datos_maquilador: str = None,
            uso_autorizado: str = None,
            valor_mercancia: Decimal | int = None,
            moneda: str = None,
            fraccion_arancelaria: str = None,
            uuid_comercio_ext: str = None,
            tipo_materia: str = None,
            descripcion_materia: str = None,
            documentacion_aduanera: DocumentacionAduanera | dict | Sequence[DocumentacionAduanera | dict] = None,
            guias_identificacion: GuiasIdentificacion | dict | Sequence[GuiasIdentificacion | dict] = None,
            cantidad_transporta: CantidadTransporta | dict | Sequence[CantidadTransporta | dict] = None,
            detalle_mercancia: DetalleMercancia | dict = None,
    ): 
        super().__init__({
            'BienesTransp': bienes_transp,
            'Descripcion': descripcion,
            'Cantidad': cantidad,
            'ClaveUnidad': clave_unidad,
            'PesoEnKg': peso_en_kg,
            'ClaveSTCC': clave_stcc,
            'Unidad': unidad,
            'Dimensiones': dimensiones,
            'MaterialPeligroso': material_peligroso,
            'CveMaterialPeligroso': cve_material_peligroso,
            'Embalaje': embalaje,
            'DescripEmbalaje': descrip_embalaje,
            'SectorCOFEPRIS': sector_cofepris,
            'NombreIngredienteActivo': nombre_ingrediente_activo,
            'NomQuimico': nom_quimico,
            'DenominacionGenericaProd': denominacion_generica_prod,
            'DenominacionDistintivaProd': denominacion_distintiva_prod,
            'Fabricante': fabricante,
            'FechaCaducidad': fecha_caducidad,
            'LoteMedicamento': lote_medicamento,
            'FormaFarmaceutica': forma_farmaceutica,
            'CondicionesEspTransp': condiciones_esp_transp,
            'RegistroSanitarioFolioAutorizacion': registro_sanitario_folio_autorizacion,
            'PermisoImportacion': permiso_importacion,
            'FolioImpoVUCEM': folio_impo_vucem,
            'NumCAS': num_cas,
            'RazonSocialEmpImp': razon_social_emp_imp,
            'NumRegSanPlagCOFEPRIS': num_reg_san_plag_cofepris,
            'DatosFabricante': datos_fabricante,
            'DatosFormulador': datos_formulador,
            'DatosMaquilador': datos_maquilador,
            'UsoAutorizado': uso_autorizado,
            'ValorMercancia': valor_mercancia,
            'Moneda': moneda,
            'FraccionArancelaria': fraccion_arancelaria,
            'UUIDComercioExt': uuid_comercio_ext,
            'TipoMateria': tipo_materia,
            'DescripcionMateria': descripcion_materia,
            'DocumentacionAduanera': documentacion_aduanera,
            'GuiasIdentificacion': guias_identificacion,
            'CantidadTransporta': cantidad_transporta,
            'DetalleMercancia': detalle_mercancia,
        })
        

class Mercancias(ScalarMap):
    """
    Nodo requerido para registrar la información de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    
    :param peso_bruto_total: Atributo requerido para registrar la suma del peso bruto total estimado de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    :param unidad_peso: Atributo requerido para registrar la clave de la unidad de medida estandarizada del peso de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    :param num_total_mercancias: Atributo requerido para registrar el número total de los bienes y/o mercancías que se trasladan en los distintos medios de transporte, identificándose por cada nodo "Mercancia" registrado en el complemento.
    :param mercancia: Nodo requerido para registrar detalladamente la información de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    :param peso_neto_total: Atributo condicional para registrar la suma de los valores indicados en el atributo “PesoNeto” del nodo “DetalleMercancia”.
    :param cargo_por_tasacion: Atributo opcional para expresar el monto del importe pagado por la tasación de los bienes y/o mercancías que se trasladan vía aérea.
    :param logistica_inversa_recoleccion_devolucion: Atributo condicional para expresar si se hace uso de alguno de los servicios de logística inversa, recolección o devolución para el traslado de los bienes y/o mercancías.
    :param autotransporte: Nodo condicional para registrar la información que permita la identificación del autotransporte de carga, por medio del cual se trasladan los bienes y/o mercancías, que transitan a través de las carreteras del territorio nacional.
    :param transporte_maritimo: Nodo condicional para registrar la información que permita la identificación de la embarcación a través de la cual se trasladan los bienes y/o mercancías por vía marítima.
    :param transporte_aereo: Nodo condicional para registrar la información que permita la identificación del transporte aéreo por medio del cual se trasladan los bienes y/o mercancías.
    :param transporte_ferroviario: Nodo condicional para registrar la información que permita la identificación del carro o contenedor en el que se trasladan los bienes y/o mercancías por vía férrea.
    """
    
    def __init__(
            self,
            peso_bruto_total: Decimal | int,
            unidad_peso: str,
            num_total_mercancias: int,
            mercancia: Mercancia | dict | Sequence[Mercancia | dict],
            peso_neto_total: Decimal | int = None,
            cargo_por_tasacion: Decimal | int = None,
            logistica_inversa_recoleccion_devolucion: str = None,
            autotransporte: Autotransporte | dict = None,
            transporte_maritimo: TransporteMaritimo | dict = None,
            transporte_aereo: TransporteAereo | dict = None,
            transporte_ferroviario: TransporteFerroviario | dict = None,
    ): 
        super().__init__({
            'PesoBrutoTotal': peso_bruto_total,
            'UnidadPeso': unidad_peso,
            'NumTotalMercancias': num_total_mercancias,
            'Mercancia': mercancia,
            'PesoNetoTotal': peso_neto_total,
            'CargoPorTasacion': cargo_por_tasacion,
            'LogisticaInversaRecoleccionDevolucion': logistica_inversa_recoleccion_devolucion,
            'Autotransporte': autotransporte,
            'TransporteMaritimo': transporte_maritimo,
            'TransporteAereo': transporte_aereo,
            'TransporteFerroviario': transporte_ferroviario,
        })
        

class Ubicacion(ScalarMap):
    """
    Nodo requerido para registrar la ubicación que sirve para indicar el domicilio del origen y/o destino parcial o final, que tienen los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    
    :param tipo_ubicacion: Atributo requerido para precisar si el tipo de ubicación corresponde al origen o destino de las ubicaciones para el traslado de los bienes y/o mercancías en los distintos medios de transporte.
    :param rfc_remitente_destinatario: Atributo requerido para registrar el RFC del remitente o destinatario de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    :param fecha_hora_salida_llegada: Atributo requerido para registrar la fecha y hora estimada en la que salen o llegan los bienes y/o mercancías de origen o al destino, respectivamente. Se expresa en la forma AAAA-MM-DDThh:mm:ss.
    :param id_ubicacion: Atributo condicional para registrar una clave que sirva para identificar el punto de salida o entrada de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte, la cual estará integrada de la siguiente forma: para origen el acrónimo “OR” o para destino el acrónimo “DE” seguido de 6 dígitos numéricos asignados por el contribuyente que emite el comprobante para su identificación.
    :param nombre_remitente_destinatario: Atributo opcional para registrar el nombre del remitente o destinatario de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    :param num_reg_id_trib: Atributo condicional para registrar el número de identificación o registro fiscal del país de residencia, para los efectos fiscales del remitente o destinatario de los bienes y/o mercancías que se trasladan cuando se trate de residentes en el extranjero.
    :param residencia_fiscal: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del remitente o destinatario de los bienes y/o mercancías, conforme el catálogo de CFDI c_Pais publicado en el portal del SAT en Internet de acuerdo a la especificación ISO 3166-1.
    :param num_estacion: Atributo condicional para registrar la clave de la estación de origen o destino para el traslado de los bienes y/o mercancías que se realiza a través de los distintos medios de transporte, esto de acuerdo al valor de la columna “Clave identificación” del catálogo c_Estaciones del complemento Carta Porte que permita asociarla al tipo de transporte.
    :param nombre_estacion: Atributo condicional para registrar el nombre de la estación de origen o destino por la que se pasa para efectuar el traslado de los bienes y/o mercancías a través de los distintos medios de transporte, conforme al catálogo c_Estaciones del complemento Carta Porte.
    :param navegacion_trafico: Atributo condicional para registrar el tipo de puerto de origen o destino en el cual se documentan los bienes y/o mercancías que se trasladan vía marítima.
    :param tipo_estacion: Atributo condicional para registrar el tipo de estación por el que pasan los bienes y/o mercancías durante su traslado a través de los distintos medios de transporte.
    :param distancia_recorrida: Atributo condicional para registrar en kilómetros la distancia recorrida entre la ubicación de origen y la de destino parcial o final, por los distintos medios de transporte que trasladan los bienes y/o mercancías.
    :param domicilio: Nodo condicional para registrar información del domicilio de origen y/o destino de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    """
    
    def __init__(
            self,
            tipo_ubicacion: str,
            rfc_remitente_destinatario: str,
            fecha_hora_salida_llegada: datetime,
            id_ubicacion: str = None,
            nombre_remitente_destinatario: str = None,
            num_reg_id_trib: str = None,
            residencia_fiscal: str = None,
            num_estacion: str = None,
            nombre_estacion: str = None,
            navegacion_trafico: str = None,
            tipo_estacion: str = None,
            distancia_recorrida: Decimal | int = None,
            domicilio: Domicilio | dict = None,
    ): 
        super().__init__({
            'TipoUbicacion': tipo_ubicacion,
            'RFCRemitenteDestinatario': rfc_remitente_destinatario,
            'FechaHoraSalidaLlegada': fecha_hora_salida_llegada,
            'IDUbicacion': id_ubicacion,
            'NombreRemitenteDestinatario': nombre_remitente_destinatario,
            'NumRegIdTrib': num_reg_id_trib,
            'ResidenciaFiscal': residencia_fiscal,
            'NumEstacion': num_estacion,
            'NombreEstacion': nombre_estacion,
            'NavegacionTrafico': navegacion_trafico,
            'TipoEstacion': tipo_estacion,
            'DistanciaRecorrida': distancia_recorrida,
            'Domicilio': domicilio,
        })
        

class CartaPorte(CFDI):
    """
    Complemento para incorporar al Comprobante Fiscal Digital por Internet (CFDI), la información relacionada a los bienes y/o mercancías, ubicaciones de origen, puntos intermedios y destinos, así como lo referente al medio por el que se transportan; que circulen por vía terrestre, férrea, aérea o naveguen por vía marítima; además de incluir el traslado de hidrocarburos y petrolíferos.
    
    :param id_ccp: Atributo requerido para expresar los 36 caracteres del folio del complemento Carta Porte (IdCCP) de la transacción de timbrado conforme al estándar RFC 4122, para la identificación del CFDI con complemento Carta Porte.
    :param transp_internac: Atributo requerido para expresar si los bienes y/o mercancías que son transportadas ingresan o salen del territorio nacional.
    :param ubicaciones: Nodo requerido para registrar las distintas ubicaciones que sirven para indicar el domicilio del origen y/o destino que tienen los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    :param mercancias: Nodo requerido para registrar la información de los bienes y/o mercancías que se trasladan en los distintos medios de transporte.
    :param entrada_salida_merc: Atributo condicional para precisar si los bienes y/o mercancías ingresan o salen del territorio nacional.
    :param pais_origen_destino: Atributo condicional para registrar la clave del país de origen o destino de los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    :param via_entrada_salida: Atributo condicional para registrar la vía de ingreso o salida de los bienes y/o mercancías en territorio nacional.
    :param total_dist_rec: Atributo condicional para indicar en kilómetros, la suma de las distancias recorridas, registradas en el atributo “DistanciaRecorrida”, para el traslado de los bienes y/o mercancías.
    :param registro_istmo: Atributo opcional para registrar las regiones, sí el traslado de los bienes y/o mercancías se realiza al interior de los Polos de Desarrollo para el Bienestar del istmo de Tehuantepec.
    :param ubicacion_polo_origen: Atributo condicional para registrar la región en donde inicia el traslado de los bienes y/o mercancias al interior de los Polos de Desarrollo para el Bienestar del istmo de Tehuantepec.
    :param ubicacion_polo_destino: Atributo condicional para registrar la región en donde termina el traslado de los bienes y/o mercancias al interior de los Polos de Desarrollo para el Bienestar del istmo de Tehuantepec.
    :param regimenes_aduaneros: Nodo condicional para registrar los distintos tipos de regímenes aduaneros a los cuales se destinan los bienes y/o mercancías que se trasladan a través de los distintos medios de transporte.
    :param figura_transporte: Nodo condicional para indicar los datos de la(s) figura(s) del transporte que interviene(n) en el traslado de los bienes y/o mercancías realizado a través de los distintos medios de transporte dentro del territorio nacional, cuando el dueño de dicho medio sea diferente del emisor del comprobante con el complemento Carta Porte.
    """
    
    tag = '{http://www.sat.gob.mx/CartaPorte31}CartaPorte'
    version = '3.1'
    
    def __init__(
            self,
            id_ccp: str,
            transp_internac: str,
            ubicaciones: Ubicacion | dict | Sequence[Ubicacion | dict],
            mercancias: Mercancias | dict,
            entrada_salida_merc: str = None,
            pais_origen_destino: str = None,
            via_entrada_salida: str = None,
            total_dist_rec: Decimal | int = None,
            registro_istmo: str = None,
            ubicacion_polo_origen: str = None,
            ubicacion_polo_destino: str = None,
            regimenes_aduaneros: str | Sequence[str] = None,
            figura_transporte: TiposFigura | dict | Sequence[TiposFigura | dict] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'IdCCP': id_ccp,
            'TranspInternac': transp_internac,
            'Ubicaciones': ubicaciones,
            'Mercancias': mercancias,
            'EntradaSalidaMerc': entrada_salida_merc,
            'PaisOrigenDestino': pais_origen_destino,
            'ViaEntradaSalida': via_entrada_salida,
            'TotalDistRec': total_dist_rec,
            'RegistroISTMO': registro_istmo,
            'UbicacionPoloOrigen': ubicacion_polo_origen,
            'UbicacionPoloDestino': ubicacion_polo_destino,
            'RegimenesAduaneros': regimenes_aduaneros,
            'FiguraTransporte': figura_transporte,
        })
        

