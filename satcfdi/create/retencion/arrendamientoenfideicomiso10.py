"""arrendamientoenfideicomiso http://www.sat.gob.mx/esquemas/retencionpago/1/arrendamientoenfideicomiso"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Arrendamientoenfideicomiso(CFDI):
    """
    Complemento para expresar el arrendamiento de bienes de un periodo o ejercicio determinado (incluye FIBRAS).
    
    :param pag_prov_efec_por_fiduc: Atributo requerido para expresar el importe del pago efectuado por parte del fiduciario al arrendador de bienes en el periodo
    :param rendim_fideicom: Atributo requerido para expresar el importe de los rendimientos obtenidos en el periodo por el arrendamiento de bienes
    :param deducc_corresp: Atributo requerido para expresar el importe de las deducciones correspondientes al arrendamiento de los bienes durante el periodo
    :param mont_tot_ret: Atributo opcional para expresar el monto total de la retención del arrendamiento de los bienes del periodo
    :param mont_res_fisc_dist_fibras: Atributo opcional para expresar el monto del resultado fiscal distribuido por FIBRAS
    :param mont_otros_concept_distr: Atributo opcional para expresar el monto de otros conceptos distribuidos
    :param descr_mont_otros_concept_distr: Atributo opcional para describir los conceptos distribuidos cuando se señalen otros conceptos.
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/arrendamientoenfideicomiso}Arrendamientoenfideicomiso'
    version = '1.0'
    
    def __init__(
            self,
            pag_prov_efec_por_fiduc: Decimal | int,
            rendim_fideicom: Decimal | int,
            deducc_corresp: Decimal | int,
            mont_tot_ret: Decimal | int = None,
            mont_res_fisc_dist_fibras: Decimal | int = None,
            mont_otros_concept_distr: Decimal | int = None,
            descr_mont_otros_concept_distr: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'PagProvEfecPorFiduc': pag_prov_efec_por_fiduc,
            'RendimFideicom': rendim_fideicom,
            'DeduccCorresp': deducc_corresp,
            'MontTotRet': mont_tot_ret,
            'MontResFiscDistFibras': mont_res_fisc_dist_fibras,
            'MontOtrosConceptDistr': mont_otros_concept_distr,
            'DescrMontOtrosConceptDistr': descr_mont_otros_concept_distr,
        })
        

