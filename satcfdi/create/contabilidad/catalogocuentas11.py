"""catalogocuentas www.sat.gob.mx/esquemas/ContabilidadE/1_1/CatalogoCuentas"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Ctas(ScalarMap):
    """
    Nodo obligatorio para expresar el detalle de cada cuenta y subcuenta del catálogo.
    
    :param cod_agrup: Atributo requerido para expresar el código asociador de cuentas y subcuentas conforme al catálogo publicado en la página de internet del SAT. Se debe asociar cada cuenta y subcuenta que sea más apropiado de acuerdo con la naturaleza y preponderancia de la cuenta o subcuenta.
    :param num_cta: Atributo requerido, es la clave con que se distingue la cuenta o subcuenta en la contabilidad
    :param desc: Atributo requerido para expresar el nombre de la cuenta o subcuenta
    :param nivel: Atributo requerido para expresar el nivel en el que se encuentra la cuenta o subcuenta en el catálogo.
    :param natur: Atributo requerido para expresar la naturaleza de la cuenta o subcuenta. (D - Deudora, A - Acreedora). ( Activo = D ) ( Pasivo = A ) ( Capital = A ) ( Ingreso = A ) ( Costo = D ) ( Gasto = D ) ( Resultado Integral de Financiamiento = D y/o A ) ( Cuentas de orden = D y/o A ).
    :param sub_cta_de: Atributo opcional en el caso de subcuentas. Sirve para expresar la clave de la cuenta a la que pertenece dicha subcuenta. Se convierte en requerido cuando se cuente con la información.
    """
    
    def __init__(
            self,
            cod_agrup: str,
            num_cta: str,
            desc: str,
            nivel: int,
            natur: str,
            sub_cta_de: str = None,
    ): 
        super().__init__({
            'CodAgrup': cod_agrup,
            'NumCta': num_cta,
            'Desc': desc,
            'Nivel': nivel,
            'Natur': natur,
            'SubCtaDe': sub_cta_de,
        })
        

class Catalogo(CFDI):
    """
    Estándar de catálogo de cuentas que se entrega como parte de la contabilidad electrónica.
    
    :param rfc: Atributo requerido para expresar el RFC del contribuyente que envía los datos
    :param mes: Atributo requerido para expresar el mes en que inicia la vigencia del catálogo para la balanza
    :param anio: Atributo requerido para expresar el año en que inicia la vigencia del catálogo para la balanza
    :param ctas: Nodo obligatorio para expresar el detalle de cada cuenta y subcuenta del catálogo.
    :param sello: Atributo opcional para contener el sello digital del archivo de contabilidad electrónica. El sello deberá ser expresado cómo una cadena de texto en formato Base 64
    :param no_certificado: Atributo opcional para expresar el número de serie del certificado de sello digital que ampara el archivo de contabilidad electrónica, de acuerdo al acuse correspondiente a 20 posiciones otorgado por el sistema del SAT.
    :param certificado: Atributo opcional que sirve para expresar el certificado de sello digital que ampara al archivo de contabilidad electrónica como texto, en formato base 64.
    """
    
    tag = '{www.sat.gob.mx/esquemas/ContabilidadE/1_1/CatalogoCuentas}Catalogo'
    version = '1.1'
    
    def __init__(
            self,
            rfc: str,
            mes: str,
            anio: int,
            ctas: Ctas | dict | Sequence[Ctas | dict],
            sello: str = None,
            no_certificado: str = None,
            certificado: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'RFC': rfc,
            'Mes': mes,
            'Anio': anio,
            'Ctas': ctas,
            'Sello': sello,
            'NoCertificado': no_certificado,
            'Certificado': certificado,
        })
        

