"""destruccion http://www.sat.gob.mx/certificadodestruccion"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class InformacionAduanera(ScalarMap):
    """
    Nodo opcional para expresar la información aduanera aplicable cuando se trate de un vehículo importado que se destruyó.
    
    :param num_ped_imp: Atributo requerido para expresar el número de documento aduanero que ampara la importación del vehículo a destruir.
    :param fecha: Atributo requerido para expresar la fecha de expedición del documento aduanero que ampara la importación del vehículo a destruir.
    :param aduana: Atributo requerido para precisar la aduana a través de la cual se regularizó la legal estancia en el país del vehículo destruido.
    """
    
    def __init__(
            self,
            num_ped_imp: str,
            fecha: date,
            aduana: str,
    ): 
        super().__init__({
            'NumPedImp': num_ped_imp,
            'Fecha': fecha,
            'Aduana': aduana,
        })
        

class VehiculoDestruido(ScalarMap):
    """
    Nodo requerido para expresar la información del vehículo que se destruyó.
    
    :param marca: Atributo requerido para expresar la marca del vehículo que se destruyó.
    :param tipo_o_clase: Atributo requerido para expresar el tipo o clase del vehículo que se destruyó.
    :param ano: Atributo requerido para la expresión del año del vehículo.
    :param num_placas: Atributo requerido para expresar el número de placas metálicas de identificación del servicio público federal o, en su caso, del servicio público de autotransporte de pasajero urbano o suburbano.
    :param num_fol_tarj_cir: Atributo requerido para expresar el número de folio de la tarjeta de circulación.
    :param modelo: Atributo opcional para expresar el modelo del vehículo que se destruyó.
    :param niv: Atributo opcional para expresar el número de identificación vehicular del vehículo (Cuando exista el NIV deberá incluirse este invariablemente).
    :param num_serie: Atributo opcional para expresar el número de serie de la carrocería del vehículo (en caso de contar con dicho número se deberá ingresar)
    :param num_motor: Atributo opcional para expresar el número de motor del vehículo (en caso de contar con dicho número se deberá ingresar).
    """
    
    def __init__(
            self,
            marca: str,
            tipo_o_clase: str,
            ano: int,
            num_placas: str,
            num_fol_tarj_cir: str,
            modelo: str = None,
            niv: str = None,
            num_serie: str = None,
            num_motor: str = None,
    ): 
        super().__init__({
            'Marca': marca,
            'TipooClase': tipo_o_clase,
            'Año': ano,
            'NumPlacas': num_placas,
            'NumFolTarjCir': num_fol_tarj_cir,
            'Modelo': modelo,
            'NIV': niv,
            'NumSerie': num_serie,
            'NumMotor': num_motor,
        })
        

class Certificadodedestruccion(CFDI):
    """
    Complemento para incorporar la información que integra el certificado de destrucción de vehículos destruidos por los centros de destrucción autorizados por el SAT.
    
    :param serie: Atributo requerido para expresar la serie de acuerdo al catálogo.
    :param num_fol_des_veh: Atributo requerido que expresa el número de folio para la destrucción del vehículo emitido por el Servicio de Administración Tributaria.
    :param vehiculo_destruido: Nodo requerido para expresar la información del vehículo que se destruyó.
    :param informacion_aduanera: Nodo opcional para expresar la información aduanera aplicable cuando se trate de un vehículo importado que se destruyó.
    """
    
    tag = '{http://www.sat.gob.mx/certificadodestruccion}certificadodedestruccion'
    version = '1.0'
    
    def __init__(
            self,
            serie: str,
            num_fol_des_veh: str,
            vehiculo_destruido: VehiculoDestruido | dict,
            informacion_aduanera: InformacionAduanera | dict = None,
    ): 
        super().__init__({
            'Version': self.version,
            'Serie': serie,
            'NumFolDesVeh': num_fol_des_veh,
            'VehiculoDestruido': vehiculo_destruido,
            'InformacionAduanera': informacion_aduanera,
        })
        

