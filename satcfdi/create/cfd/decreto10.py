"""decreto http://www.sat.gob.mx/renovacionysustitucionvehiculos"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class VehiculoNuvoSemEnajenadoFabAlPerm(ScalarMap):
    """
    Datos del vehículo nuevo o seminuevo que enajena el fabricante, ensamblador o distribuidor autorizado al permisionario.
    
    :param ano: Atributo requerido para la expresión del año ó año modelo del vehículo nuevo o seminuevo que enajena el fabricante, ensamblador o distribuidor autorizado.
    :param num_placas: Atributo requerido para expresar el número de placa metálicas de identificación del servicio público federal o, en su caso, del servicio público de autotransporte de pasajeros urbano o suburbano del vehículo nuevo o seminuevo que enajena el fabricante, ensamblador o distribuidor autorizado.
    :param modelo: Atributo opcional para expresar el modelo del vehículo nuevo o seminuevo que enajena el fabricante, ensamblador o distribuidor autorizado.
    :param rfc: Atributo opcional para la Clave del Registro Federal de Contribuyentes del arrendatario en el caso de que el adquiriente del vehículo nuevo o seminuevo sea una arrendadora financiera.
    """
    
    def __init__(
            self,
            ano: int,
            num_placas: str,
            modelo: str = None,
            rfc: str = None,
    ): 
        super().__init__({
            'Año': ano,
            'NumPlacas': num_placas,
            'Modelo': modelo,
            'RFC': rfc,
        })
        

class VehiculoUsadoEnajenadoPermAlFab(ScalarMap):
    """
    Datos del vehículo usado que enajena el permisionario a cuenta del precio del vehículo nuevo o seminuevo.
    
    :param precio_veh_usado: Atributo requerido que expresa el precio del vehículo usado que el permisionario enajena al fabricante, ensamblador o distribuidor autorizado a cuenta del precio del vehículo nuevo o seminuevo.
    :param tipo_veh: Atributo requerido que expresar, según el Decreto, las características del vehículo usado que el permisionario enajena al fabricante, ensamblador o distribuidor autorizado a cuenta del precio del vehículo nuevo o seminuevo, de acuerdo con el catálogo “4. Tipo de vehículo conforme al Decreto por el que se otorgan medidas para la sustitución de vehículos de autotransporte de pasaje y carga”.
    :param marca: Atributo requerido para expresar la marca del vehículo usado que se enajena.
    :param tipo_o_clase: Atributo requerido para expresar el tipo o clase del vehículo usado que se enajena.
    :param ano: Atributo requerido para la expresión del año ó año modelo del vehículo usado que se enajena.
    :param num_placas: Atributo requerido para expresar el número de placas metálicas de identificación del servicio público federal o, en su caso, del servicio público de autotransporte de pasajeros urbano o suburbano del vehículo usado que se enajena.
    :param num_fol_tarj_cir: Atributo requerido para expresar el número de folio de la tarjeta de circulación del vehículo usado que se enajena.
    :param num_fol_aviso_int: Atributo requerido para expresar el número de folio del acuse de recibo del Aviso de Intención para acceder al programa de destrucción.
    :param num_ped_im: Atributo requerido para expresar el número de documento aduanero con el cual se importó en definitiva el vehículo usado.
    :param aduana: Atributo requerido para precisar la aduana por la que se efectuó la importación del vehículo usado.
    :param fecha_regul_veh: Atributo requerido para expresar la fecha del pedimento en el que se regularizó la legal importación definitiva del vehículo usado. Se expresa en la forma aaaa-mm-dd de acuerdo a a especificación ISO 8601
    :param foliofiscal: Atributo requerido para expresar el número de folio fiscal del CFDI expedido por el Centro de Destrucción Autorizado al que se ha incorporado el Complemento Certificado de Destrucción del vehículo usado que enajena el permisionario.
    :param modelo: Atributo opcional para la expresión del modelo del vehículo usado que se enajena.
    :param niv: Atributo opcional para expresar el número de identificación vehicular del vehículo usado que se enajena. (Cuando exista el NIV deberá incluirse este invariablemente).
    :param num_serie: Atributo opcional para expresar el número de serie de la carrocería del vehículo usado que se enajena. (En caso de contar con dicho número se deberá ingresar convirtiéndose en requerido).
    :param num_motor: Atributo opcional para expresar el número de motor del vehículo usado que se enajena (En caso de contar con dicho número se deberá ingresar volviéndose requerido).
    """
    
    def __init__(
            self,
            precio_veh_usado: Decimal | int,
            tipo_veh: str,
            marca: str,
            tipo_o_clase: str,
            ano: int,
            num_placas: str,
            num_fol_tarj_cir: str,
            num_fol_aviso_int: str,
            num_ped_im: str,
            aduana: str,
            fecha_regul_veh: date,
            foliofiscal: str,
            modelo: str = None,
            niv: str = None,
            num_serie: str = None,
            num_motor: str = None,
    ): 
        super().__init__({
            'PrecioVehUsado': precio_veh_usado,
            'TipoVeh': tipo_veh,
            'Marca': marca,
            'TipooClase': tipo_o_clase,
            'Año': ano,
            'NumPlacas': num_placas,
            'NumFolTarjCir': num_fol_tarj_cir,
            'NumFolAvisoint': num_fol_aviso_int,
            'NumPedIm': num_ped_im,
            'Aduana': aduana,
            'FechaRegulVeh': fecha_regul_veh,
            'Foliofiscal': foliofiscal,
            'Modelo': modelo,
            'NIV': niv,
            'NumSerie': num_serie,
            'NumMotor': num_motor,
        })
        

class DecretoSustitVehicular(ScalarMap):
    """
    Nodo opcional para expresar los datos aplicables al estimulo por la aplicación del Decreto por el que se otorgan medidas para la sustitución de vehículos de autotransporte de pasaje y carga.
    
    :param veh_enaj: Atributo requerido para expresar si el vehículo que el fabricante, ensamblador o distribuidor autorizado enajena al permisionario es nuevo o seminuevo, de acuerdo con el catálogo “2. Vehículo enajenado”.
    :param vehiculo_usado_enajenado_perm_al_fab: Datos del vehículo usado que enajena el permisionario a cuenta del precio del vehículo nuevo o seminuevo.
    :param vehiculo_nuvo_sem_enajenado_fab_al_perm: Datos del vehículo nuevo o seminuevo que enajena el fabricante, ensamblador o distribuidor autorizado al permisionario.
    """
    
    def __init__(
            self,
            veh_enaj: str,
            vehiculo_usado_enajenado_perm_al_fab: VehiculoUsadoEnajenadoPermAlFab | dict,
            vehiculo_nuvo_sem_enajenado_fab_al_perm: VehiculoNuvoSemEnajenadoFabAlPerm | dict,
    ): 
        super().__init__({
            'VehEnaj': veh_enaj,
            'VehiculoUsadoEnajenadoPermAlFab': vehiculo_usado_enajenado_perm_al_fab,
            'VehiculoNuvoSemEnajenadoFabAlPerm': vehiculo_nuvo_sem_enajenado_fab_al_perm,
        })
        

class VehiculosUsadosEnajenadoPermAlFab(ScalarMap):
    """
    Datos del vehículo o vehículos usados que enajena el permisionario a cuenta del precio del vehículo nuevo o seminuevo (pueden enajenarse 1 o más vehículos, por lo que de ser 2 o más se deberán llenar tantos elementos como vehículos usados se enajenen).
    
    :param precio_veh_usado: Atributo requerido que expresa el precio del vehículo usado que el permisionario enajena al fabricante, ensamblador o distribuidor autorizado a cuenta del precio del vehículo nuevo o seminuevo.
    :param tipo_veh: Atributo requerido para expresar, según el Decreto, el tipo de vehículo usado que enajena el permisionario, de acuerdo con el catálogo “3. Tipo de Vehículo conforme al Decreto por el que se fomenta la renovación del parque vehicular del autotransporte”.
    :param marca: Atributo requerido para expresar la marca del vehículo usado que se enajena.
    :param tipo_o_clase: Atributo requerido para expresar el tipo o clase del vehículo usado que se enajena.
    :param ano: Atributo requerido para la expresión del año ó año modelo del vehículo usado que se enajena.
    :param num_placas: Atributo requerido para expresar el número de placas metálicas de identificación del servicio público federal o, en su caso, del servicio público de autotransporte de pasajeros urbano o suburbano del vehículo usado que se enajena.
    :param num_fol_tarj_cir: Atributo requerido para expresar el número de folio de la tarjeta de circulación del vehículo usado que se enajena.
    :param foliofiscal: Atributo requerido para expresar el número de folio fiscal del CFDI expedido por el Centro de Destrucción Autorizado al que se ha incorporado el Complemento Certificado de Destrucción del vehículo usado que enajena el permisionario.
    :param modelo: Atributo opcional para la expresión del modelo del vehículo usado que se enajena.
    :param niv: Atributo opcional para expresar el número de identificación vehicular del vehículo usado que se enajena. (Cuando exista el NIV deberá incluirse este invariablemente).
    :param num_serie: Atributo opcional para expresar el número de serie de la carrocería del vehículo usado que se enajena. (En caso de contar con dicho número se deberá ingresar convirtiéndose en requerido).
    :param num_motor: Atributo opcional para expresar el número de motor del vehículo usado que se enajena (En caso de contar con dicho número se deberá ingresar volviéndose requerido).
    :param num_ped_im: Atributo opcional para expresar el número de documento aduanero con el cual se importó en definitiva el vehículo usado, en su caso.
    :param aduana: Atributo opcional para precisar la aduana por la que se efectuó la importación del vehículo usado, en su caso.
    :param fecha_regul_veh: Atributo opcional para expresar la fecha del pedimento en el que se regularizó la legal importación definitiva del vehículo usado, en su caso. Se expresa en la forma aaaa-mm-dd de acuerdo a especificación ISO 8601.
    """
    
    def __init__(
            self,
            precio_veh_usado: Decimal | int,
            tipo_veh: str,
            marca: str,
            tipo_o_clase: str,
            ano: int,
            num_placas: str,
            num_fol_tarj_cir: str,
            foliofiscal: str,
            modelo: str = None,
            niv: str = None,
            num_serie: str = None,
            num_motor: str = None,
            num_ped_im: str = None,
            aduana: str = None,
            fecha_regul_veh: date = None,
    ): 
        super().__init__({
            'PrecioVehUsado': precio_veh_usado,
            'TipoVeh': tipo_veh,
            'Marca': marca,
            'TipooClase': tipo_o_clase,
            'Año': ano,
            'NumPlacas': num_placas,
            'NumFolTarjCir': num_fol_tarj_cir,
            'Foliofiscal': foliofiscal,
            'Modelo': modelo,
            'NIV': niv,
            'NumSerie': num_serie,
            'NumMotor': num_motor,
            'NumPedIm': num_ped_im,
            'Aduana': aduana,
            'FechaRegulVeh': fecha_regul_veh,
        })
        

class DecretoRenovVehicular(ScalarMap):
    """
    Nodo opcional para expresar los datos aplicables al estimulo por la aplicación del Decreto por el que se fomenta la renovación del parque vehicular del autotransporte.
    
    :param veh_enaj: Atributo requerido para expresar si el vehículo que el fabricante, ensamblador o distribuidor autorizado enajena al permisionario es nuevo o seminuevo, de acuerdo con el catálogo “2. Vehículo enajenado”.
    :param vehiculos_usados_enajenado_perm_al_fab: Datos del vehículo o vehículos usados que enajena el permisionario a cuenta del precio del vehículo nuevo o seminuevo (pueden enajenarse 1 o más vehículos, por lo que de ser 2 o más se deberán llenar tantos elementos como vehículos usados se enajenen).
    :param vehiculo_nuvo_sem_enajenado_fab_al_perm: Datos del vehículo nuevo o seminuevo que enajena el fabricante, ensamblador o distribuidor autorizado al permisionario.
    """
    
    def __init__(
            self,
            veh_enaj: str,
            vehiculos_usados_enajenado_perm_al_fab: VehiculosUsadosEnajenadoPermAlFab | dict | Sequence[VehiculosUsadosEnajenadoPermAlFab | dict],
            vehiculo_nuvo_sem_enajenado_fab_al_perm: VehiculoNuvoSemEnajenadoFabAlPerm | dict,
    ): 
        super().__init__({
            'VehEnaj': veh_enaj,
            'VehiculosUsadosEnajenadoPermAlFab': vehiculos_usados_enajenado_perm_al_fab,
            'VehiculoNuvoSemEnajenadoFabAlPerm': vehiculo_nuvo_sem_enajenado_fab_al_perm,
        })
        

class Renovacionysustitucionvehiculos(CFDI):
    """
    Complemento para incorporar la información relativa a los estímulos por la renovación del parque vehicular del autotransporte y por el que se otorgan medidas para la sustitución de vehículos de autotransporte de pasaje y carga.
    
    :param tipo_de_decreto: Atributo requerido que indica el Decreto de cuya aplicación se trate, de acuerdo con el catálogo “1. Tipo de Decreto”.
    :param decreto_renov_vehicular: Nodo opcional para expresar los datos aplicables al estimulo por la aplicación del Decreto por el que se fomenta la renovación del parque vehicular del autotransporte.
    :param decreto_sustit_vehicular: Nodo opcional para expresar los datos aplicables al estimulo por la aplicación del Decreto por el que se otorgan medidas para la sustitución de vehículos de autotransporte de pasaje y carga.
    """
    
    tag = '{http://www.sat.gob.mx/renovacionysustitucionvehiculos}renovacionysustitucionvehiculos'
    version = '1.0'
    
    def __init__(
            self,
            tipo_de_decreto: str,
            decreto_renov_vehicular: DecretoRenovVehicular | dict = None,
            decreto_sustit_vehicular: DecretoSustitVehicular | dict = None,
    ): 
        super().__init__({
            'Version': self.version,
            'TipoDeDecreto': tipo_de_decreto,
            'DecretoRenovVehicular': decreto_renov_vehicular,
            'DecretoSustitVehicular': decreto_sustit_vehicular,
        })
        

