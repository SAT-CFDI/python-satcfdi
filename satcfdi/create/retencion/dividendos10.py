"""dividendos http://www.sat.gob.mx/esquemas/retencionpago/1/dividendos"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Remanente(ScalarMap):
    """
    Nodo opcional que expresa el resultado obtenido de la diferencia entre ingresos y egresos de las personas morales que distribuyan anticipos o rendimientos o sociedades de producción, sociedades y asociaciones civiles.
    
    :param proporcion_rem: Atributo opcional que expresa el porcentaje de participación de sus integrantes o accionistas
    """
    
    def __init__(
            self,
            proporcion_rem: Decimal | int = None,
    ): 
        super().__init__({
            'ProporcionRem': proporcion_rem,
        })
        

class DividOUtil(ScalarMap):
    """
    Nodo opcional que expresa los dividendos o utilidades distribuidas del periodo o ejercicio
    
    :param cve_tip_div_outil: Atributo requerido para expresar la clave del tipo de dividendo o utilidad distribuida de acuerdo al catálogo.
    :param mont_isr_acred_ret_mexico: Atributo requerido para expresar el importe o retención del dividendo o utilidad en territorio nacional
    :param mont_isr_acred_ret_extranjero: Atributo requerido para expresar el importe o retención del dividendo o utilidad en territorio extranjero
    :param tipo_soc_distr_div: Atributo requerido para expresar si el dividendo es distribuido por sociedades nacionales o extranjeras.
    :param mont_ret_ext_div_ext: Atributo opcional para expresar el monto de la retención en el extranjero sobre dividendos del extranjero
    :param mont_isr_acred_nal: Atributo opcional para expresar el monto del ISR acreditable nacional
    :param mont_div_acum_nal: Atributo opcional para expresar el monto del dividendo acumulable nacional
    :param mont_div_acum_ext: Atributo opcional para expresar el monto del dividendo acumulable extranjero
    """
    
    def __init__(
            self,
            cve_tip_div_outil: str,
            mont_isr_acred_ret_mexico: Decimal | int,
            mont_isr_acred_ret_extranjero: Decimal | int,
            tipo_soc_distr_div: str,
            mont_ret_ext_div_ext: Decimal | int = None,
            mont_isr_acred_nal: Decimal | int = None,
            mont_div_acum_nal: Decimal | int = None,
            mont_div_acum_ext: Decimal | int = None,
    ): 
        super().__init__({
            'CveTipDivOUtil': cve_tip_div_outil,
            'MontISRAcredRetMexico': mont_isr_acred_ret_mexico,
            'MontISRAcredRetExtranjero': mont_isr_acred_ret_extranjero,
            'TipoSocDistrDiv': tipo_soc_distr_div,
            'MontRetExtDivExt': mont_ret_ext_div_ext,
            'MontISRAcredNal': mont_isr_acred_nal,
            'MontDivAcumNal': mont_div_acum_nal,
            'MontDivAcumExt': mont_div_acum_ext,
        })
        

class Dividendos(CFDI):
    """
    Complemento para expresar el total de ganancias y utilidades generadas por rendimientos en base a inversiones en instrumentos de inversión
    
    :param divid_o_util: Nodo opcional que expresa los dividendos o utilidades distribuidas del periodo o ejercicio
    :param remanente: Nodo opcional que expresa el resultado obtenido de la diferencia entre ingresos y egresos de las personas morales que distribuyan anticipos o rendimientos o sociedades de producción, sociedades y asociaciones civiles.
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/dividendos}Dividendos'
    version = '1.0'
    
    def __init__(
            self,
            divid_o_util: DividOUtil | dict = None,
            remanente: Remanente | dict = None,
    ): 
        super().__init__({
            'Version': self.version,
            'DividOUtil': divid_o_util,
            'Remanente': remanente,
        })
        

