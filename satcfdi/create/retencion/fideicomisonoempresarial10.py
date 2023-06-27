"""fideicomisonoempresarial http://www.sat.gob.mx/esquemas/retencionpago/1/fideicomisonoempresarial"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class RetEfectFideicomiso(ScalarMap):
    """
    Nodo requerido para expresar las retenciones efectuadas al fideicomiso
    
    :param mont_ret_rel_pag_fideic: Atributo requerido para expresar el monto de la retenciones con relación al fideicomiso
    :param desc_ret_rel_pag_fideic: Atributo requerido para expresar la descripción de las retenciones con relación al fideicomiso
    """
    
    def __init__(
            self,
            mont_ret_rel_pag_fideic: Decimal | int,
            desc_ret_rel_pag_fideic: str,
    ): 
        super().__init__({
            'MontRetRelPagFideic': mont_ret_rel_pag_fideic,
            'DescRetRelPagFideic': desc_ret_rel_pag_fideic,
        })
        

class DeduccOSalidas(ScalarMap):
    """
    Nodo requerido para expresar el importe de los egresos del periodo de fideicomisos que no realizan actividades empresariales
    
    :param mont_tot_egres_periodo: Atributo requerido para expresar el importe total de los egresos del periodo de fideicomiso que no realizan actividades empresariales
    :param part_prop_del_fideicom: Atributo requerido para expresar la parte proporcional de las deducciones autorizadas del periodo que corresponden al fideicomisario o fideicomitente
    :param prop_del_mont_tot: Atributo requerido para expresar la proporción de participación del fideicomisario o fideicomitente de acuerdo al contrato
    :param integrac_egresos: Nodo requerido para expresar la integración de las deducciones en los ingresos obtenidos por fideicomisos que no realizan actividades empresariales
    """
    
    def __init__(
            self,
            mont_tot_egres_periodo: Decimal | int,
            part_prop_del_fideicom: Decimal | int,
            prop_del_mont_tot: Decimal | int,
            integrac_egresos: str,
    ): 
        super().__init__({
            'MontTotEgresPeriodo': mont_tot_egres_periodo,
            'PartPropDelFideicom': part_prop_del_fideicom,
            'PropDelMontTot': prop_del_mont_tot,
            'IntegracEgresos': integrac_egresos,
        })
        

class IngresosOEntradas(ScalarMap):
    """
    Nodo requerido para expresar el importe de los ingresos del periodo de fideicomisos que no realizan actividades empresariales
    
    :param mont_tot_entradas_periodo: Atributo requerido para expresar el importe total de los ingresos del periodo de los fideicomisos que no realizan actividades empresariales
    :param part_prop_acum_del_fideicom: Atributo requerido para expresar la parte proporcional de los ingresos acumulables del periodo que correspondan al fideicomisario o fideicomitente
    :param prop_del_mont_tot: Atributo requerido para expresar la proporción de participación del fideicomisario o fideicomitente de acuerdo al contrato
    :param integrac_ingresos: Nodo requerido para expresar el detalle de la integración de los ingresos obtenidos en el periodo por fideicomisos que no realizan actividades empresariales
    """
    
    def __init__(
            self,
            mont_tot_entradas_periodo: Decimal | int,
            part_prop_acum_del_fideicom: Decimal | int,
            prop_del_mont_tot: Decimal | int,
            integrac_ingresos: str,
    ): 
        super().__init__({
            'MontTotEntradasPeriodo': mont_tot_entradas_periodo,
            'PartPropAcumDelFideicom': part_prop_acum_del_fideicom,
            'PropDelMontTot': prop_del_mont_tot,
            'IntegracIngresos': integrac_ingresos,
        })
        

class Fideicomisonoempresarial(CFDI):
    """
    Complemento para expresar la información sobre los fideicomisos que no realizan actividades empresariales
    
    :param ingresos_oentradas: Nodo requerido para expresar el importe de los ingresos del periodo de fideicomisos que no realizan actividades empresariales
    :param deducc_osalidas: Nodo requerido para expresar el importe de los egresos del periodo de fideicomisos que no realizan actividades empresariales
    :param ret_efect_fideicomiso: Nodo requerido para expresar las retenciones efectuadas al fideicomiso
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/fideicomisonoempresarial}Fideicomisonoempresarial'
    version = '1.0'
    
    def __init__(
            self,
            ingresos_oentradas: IngresosOEntradas | dict,
            deducc_osalidas: DeduccOSalidas | dict,
            ret_efect_fideicomiso: RetEfectFideicomiso | dict,
    ): 
        super().__init__({
            'Version': self.version,
            'IngresosOEntradas': ingresos_oentradas,
            'DeduccOSalidas': deducc_osalidas,
            'RetEfectFideicomiso': ret_efect_fideicomiso,
        })
        

