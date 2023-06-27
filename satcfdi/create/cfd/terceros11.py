"""terceros http://www.sat.gob.mx/terceros"""
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
        

class Parte(ScalarMap):
    """
    Nodo opcional para expresar las partes o componentes que integran la totalidad del concepto expresado en el CFD o CFDI
    
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
        

class InformacionAduanera(ScalarMap):
    """
    Nodo opcional para introducir la información aduanera aplicable cuando se trate de ventas de primera mano de mercancías importadas.
    
    """
    
    def __init__(
            self,
            hello_there_super: TInformacionAduanera | dict
    ): 
        super().__init__({
        })
        

class InformacionFiscalTercero(ScalarMap):
    """
    Nodo opcional para expresar información fiscal de terceros
    
    """
    
    def __init__(
            self,
            hello_there_super: TUbicacionFiscal | dict
    ): 
        super().__init__({
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
    
    :param retenciones: Nodo opcional para capturar los impuestos retenidos aplicables
    :param traslados: Nodo opcional para asentar o referir los impuestos trasladados aplicables
    """
    
    def __init__(
            self,
            retenciones: Retencion | dict | Sequence[Retencion | dict] = None,
            traslados: Traslado | dict | Sequence[Traslado | dict] = None,
    ): 
        super().__init__({
            'Retenciones': retenciones,
            'Traslados': traslados,
        })
        

class PorCuentadeTerceros(CFDI):
    """
    Complemento concepto para la emisión de Comprobante Fiscal Digital (CFD) y Comprobante Fiscal Digital a través de Internet (CFDI) por orden y cuenta de terceros.
    
    :param rfc: Atributo requerido para la Clave del Registro Federal de Contribuyentes correspondiente al contribuyente emisor del comprobante sin guiones o espacios.
    :param impuestos: Nodo requerido para capturar los impuestos aplicables.
    :param nombre: Atributo opcional para el nombre o razón social del contribuyente emisor del comprobante.
    :param informacion_fiscal_tercero: Nodo opcional para expresar información fiscal de terceros
    :param informacion_aduanera: Nodo opcional para introducir la información aduanera aplicable cuando se trate de ventas de primera mano de mercancías importadas.
    :param parte: Nodo opcional para expresar las partes o componentes que integran la totalidad del concepto expresado en el CFD o CFDI
    :param cuenta_predial: Nodo opcional para asentar el número de cuenta predial con el que fue registrado el inmueble, en el sistema catastral de la entidad federativa de que trate.
    """
    
    tag = '{http://www.sat.gob.mx/terceros}PorCuentadeTerceros'
    version = '1.1'
    
    def __init__(
            self,
            rfc: str,
            impuestos: Impuestos | dict,
            nombre: str = None,
            informacion_fiscal_tercero: InformacionFiscalTercero | dict = None,
            informacion_aduanera: InformacionAduanera | dict = None,
            parte: Parte | dict | Sequence[Parte | dict] = None,
            cuenta_predial: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'Rfc': rfc,
            'Impuestos': impuestos,
            'Nombre': nombre,
            'InformacionFiscalTercero': informacion_fiscal_tercero,
            'InformacionAduanera': informacion_aduanera,
            'Parte': parte,
            'CuentaPredial': cuenta_predial,
        })
        

