"""intereseshipotecarios http://www.sat.gob.mx/esquemas/retencionpago/1/intereseshipotecarios"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Intereseshipotecarios(CFDI):
    """
    Complemento para expresar la información sobre Intereses reales deducibles por crédito hipotecarios
    
    :param credito_de_inst_financ: Atributo requerido para expresar si el crédito otorgado fue por institución financiera
    :param saldo_insoluto: Atributo requerido para expresar el saldo insoluto al 31 de diciembre del ejercicio inmediato anterior o fecha de contratación si se llevo a cabo en el ejercicio en curso
    :param prop_deduc_del_credit: Atributo opcional que expresa la proporción deducible del crédito aplicable sobre los intereses reales devengados y pagados
    :param mont_tot_int_nominales_dev: Atributo opcional que expresa el monto total de intereses nominales devengados
    :param mont_tot_int_nominales_dev_y_pag: Atributo opcional que expresa el monto total de intereses nominales devengados y pagados
    :param mont_tot_int_real_pag_deduc: Atributo opcional que expresa el monto total de intereses reales pagados deducibles
    :param num_contrato: Atributo opcional que expresa el número de contrato del crédito hipotecario
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/intereseshipotecarios}Intereseshipotecarios'
    version = '1.0'
    
    def __init__(
            self,
            credito_de_inst_financ: str,
            saldo_insoluto: Decimal | int,
            prop_deduc_del_credit: Decimal | int = None,
            mont_tot_int_nominales_dev: Decimal | int = None,
            mont_tot_int_nominales_dev_y_pag: Decimal | int = None,
            mont_tot_int_real_pag_deduc: Decimal | int = None,
            num_contrato: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'CreditoDeInstFinanc': credito_de_inst_financ,
            'SaldoInsoluto': saldo_insoluto,
            'PropDeducDelCredit': prop_deduc_del_credit,
            'MontTotIntNominalesDev': mont_tot_int_nominales_dev,
            'MontTotIntNominalesDevYPag': mont_tot_int_nominales_dev_y_pag,
            'MontTotIntRealPagDeduc': mont_tot_int_real_pag_deduc,
            'NumContrato': num_contrato,
        })
        

