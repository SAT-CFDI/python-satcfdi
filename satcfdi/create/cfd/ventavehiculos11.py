"""ventavehiculos http://www.sat.gob.mx/ventavehiculos"""
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
        

class Parte(ScalarMap):
    """
    Nodo opcional para expresar las partes o componentes que integran la totalidad del concepto expresado en el CFDI.
    
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
        

class VentaVehiculos(CFDI):
    """
    Complemento concepto que permite incorporar a los fabricantes, ensambladores o distribuidores autorizados de automóviles nuevos, así como aquéllos que importen automóviles para permanecer en forma definitiva en la franja fronteriza norte del país y en los Estados de Baja California, Baja California Sur y la región parcial del Estado de Sonora, a un Comprobante Fiscal Digital a través de Internet (CFDI) la clave vehicular que corresponda a la versión enajenada y el número de identificación vehicular que corresponda al vehículo enajenado.
    
    :param clave_vehicular: Atributo requerido para precisar Clave vehicular que corresponda a la versión del vehículo enajenado.
    :param niv: Atributo requerido para precisar el número de identificación vehicular que corresponda al vehículo enajenado.
    :param informacion_aduanera: Nodo opcional para introducir la información aduanera aplicable cuando se trate de ventas de primera mano de mercancías importadas.
    :param parte: Nodo opcional para expresar las partes o componentes que integran la totalidad del concepto expresado en el CFDI.
    """
    
    tag = '{http://www.sat.gob.mx/ventavehiculos}VentaVehiculos'
    version = '1.1'
    
    def __init__(
            self,
            clave_vehicular: str,
            niv: str,
            informacion_aduanera: TInformacionAduanera | dict | Sequence[TInformacionAduanera | dict] = None,
            parte: Parte | dict | Sequence[Parte | dict] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'ClaveVehicular': clave_vehicular,
            'Niv': niv,
            'InformacionAduanera': informacion_aduanera,
            'Parte': parte,
        })
        

