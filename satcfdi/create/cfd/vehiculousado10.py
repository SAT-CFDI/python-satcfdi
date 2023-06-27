"""vehiculousado http://www.sat.gob.mx/vehiculousado"""
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
    :param fecha: Atributo requerido para expresar la fecha de expedición del documento aduanero que ampara la importación del bien.
    :param aduana: Atributo opcional para precisar la aduana por la que se efectuó la importación del bien.
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
        

class VehiculoUsado(CFDI):
    """
    Complemento opcional que permite incorporar información a los contribuyentes que enajenen vehículos nuevos a personas físicas que no tributen en los términos de las Secciones I y II del Capítulo II del Título IV de la ley del ISR, y que reciban en contraprestación como resultados de esa enajenación un vehículo usado y dinero
    
    :param monto_adquisicion: Atributo requerido para expresar el monto de adquisición del vehículo usado según factura original, primera venta
    :param monto_enajenacion: Atributo requerido para expresar el monto de enajenación del vehículo usado
    :param clave_vehicular: Atributo requerido para expresar la clave vehicular del vehículo usado
    :param marca: Atributo requerido para expresar la marca del vehículo usado
    :param tipo: Atributo requerido para expresar el tipo del vehículo usado
    :param modelo: Atributo requerido para expresar el año modelo del vehículo usado
    :param valor: Atributo requerido para expresar el valor del vehículo, establecido en la Guía EBC o Libro Azul (Guía de Información a Comerciantes de Automóviles y Camiones y Aseguradores de la República Mexicana) vigente, emitida por la Asociación Nacional de Comerciantes en Automóviles y Camiones nuevos y usados A.C.
    :param numero_motor: Atributo opcional para expresar el número de motor del vehículo usado (en caso de contar con dicho número se deberá ingresar)
    :param numero_serie: Atributo opcional para expresar el número de serie de la carrocería del vehículo usado (en caso de contar con dicho número se deberá ingresar)
    :param niv: Atributo opcional para expresar el número de identificación vehicular del vehículo usado (Cuando exista el NIV deberá incluirse este invariablemente)
    :param informacion_aduanera: Nodo opcional para introducir la información aduanera aplicable cuando se trate de ventas de primera mano de mercancías importadas.
    """
    
    tag = '{http://www.sat.gob.mx/vehiculousado}VehiculoUsado'
    version = '1.0'
    
    def __init__(
            self,
            monto_adquisicion: Decimal | int,
            monto_enajenacion: Decimal | int,
            clave_vehicular: str,
            marca: str,
            tipo: str,
            modelo: str,
            valor: Decimal | int,
            numero_motor: str = None,
            numero_serie: str = None,
            niv: str = None,
            informacion_aduanera: TInformacionAduanera | dict | Sequence[TInformacionAduanera | dict] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'MontoAdquisicion': monto_adquisicion,
            'MontoEnajenacion': monto_enajenacion,
            'ClaveVehicular': clave_vehicular,
            'Marca': marca,
            'Tipo': tipo,
            'Modelo': modelo,
            'Valor': valor,
            'NumeroMotor': numero_motor,
            'NumeroSerie': numero_serie,
            'NIV': niv,
            'InformacionAduanera': informacion_aduanera,
        })
        

