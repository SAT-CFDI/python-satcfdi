"""planesderetiro11 http://www.sat.gob.mx/esquemas/retencionpago/1/planesderetiro11"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class AportacionesODepositos(ScalarMap):
    """
    Nodo para identificar el tipo de aportación o depósito que realiza el aportante a su plan de retiro, conforme a los artículos 151, 185 de la Ley el Impuesto sobre la Renta, y 258 del Reglamento de la Ley del Impuesto Sobre la Renta.
    
    :param tipo_aportacion_odeposito: Atributo requerido que identifica el tipo de aportación o depósito que se realiza al plan de retiro.
    :param mont_aport_odep: Atributo requerido que expresa el monto de las aportaciones o depósitos efectuados al plan de retiro.
    :param rfc_fiduciaria: Atributo opcional que expresa el RFC de la fiduciaria de fungió como administrador del plan de pensiones, cuando se trate de aportaciones realizadas de conformidad con el artículo 258 del Reglamento de la LISR, se vuelve requerido cuando el administrador del plan es una fiduciaria.
    """
    
    def __init__(
            self,
            tipo_aportacion_odeposito: str,
            mont_aport_odep: Decimal | int,
            rfc_fiduciaria: str = None,
    ): 
        super().__init__({
            'TipoAportacionODeposito': tipo_aportacion_odeposito,
            'MontAportODep': mont_aport_odep,
            'RFCFiduciaria': rfc_fiduciaria,
        })
        

class Planesderetiro(CFDI):
    """
    Complemento para expresar la información sobre los planes personales de retiro
    
    :param sistema_financ: Atributo requerido para expresar si los planes personales de retiro son del sistema financiero
    :param mont_int_reales_deveng_anioo_inm_ant: Atributo requerido para expresar el monto de los intereses reales devengados o percibidos durante el año inmediato anterior de los planes personales de retiro
    :param hubo_retiros_anio_inm_ant_per: Atributo requerido para expresar si se realizaron retiros de recursos invertidos y sus rendimientos en el ejercicio inmediato anterior antes de cumplir los requisitos de permanencia
    :param hubo_retiros_anio_inm_ant: Atributo requerido que expresa si se realizaron retiros en el ejercicio inmediato anterior
    :param mont_tot_aport_anio_inm_anterior: Atributo opcional que expresa el monto total de las aportaciones actualizadas en el año inmediato anterior de los planes personales de retiro
    :param mont_tot_retirado_anio_inm_ant_per: Atributo condicional que expresa el monto total del retiro realizado antes de cumplir con los requisitos de permanencia
    :param mont_tot_exent_retirado_anio_inm_ant: Atributo condicional que expresa el monto total exento del retiro realizado en el ejercicio inmediato anterior
    :param mont_tot_exedente_anio_inm_ant: Atributo condicional que expresa el monto total excedente del monto exento del retiro realizado en el ejercicio inmediato anterior
    :param mont_tot_retirado_anio_inm_ant: Atributo opcional que expresa el monto total de retiros realizados en el ejercicio inmediato anterior
    :param num_referencia: Atributo opcional que expresa el número de referencia, contrato o cuenta con la que identifica la institución a su cliente.
    :param aportaciones_odepositos: Nodo para identificar el tipo de aportación o depósito que realiza el aportante a su plan de retiro, conforme a los artículos 151, 185 de la Ley el Impuesto sobre la Renta, y 258 del Reglamento de la Ley del Impuesto Sobre la Renta.
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/planesderetiro11}Planesderetiro'
    version = '1.1'
    
    def __init__(
            self,
            sistema_financ: str,
            mont_int_reales_deveng_anioo_inm_ant: Decimal | int,
            hubo_retiros_anio_inm_ant_per: str,
            hubo_retiros_anio_inm_ant: str,
            mont_tot_aport_anio_inm_anterior: Decimal | int = None,
            mont_tot_retirado_anio_inm_ant_per: Decimal | int = None,
            mont_tot_exent_retirado_anio_inm_ant: Decimal | int = None,
            mont_tot_exedente_anio_inm_ant: Decimal | int = None,
            mont_tot_retirado_anio_inm_ant: Decimal | int = None,
            num_referencia: str = None,
            aportaciones_odepositos: AportacionesODepositos | dict | Sequence[AportacionesODepositos | dict] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'SistemaFinanc': sistema_financ,
            'MontIntRealesDevengAniooInmAnt': mont_int_reales_deveng_anioo_inm_ant,
            'HuboRetirosAnioInmAntPer': hubo_retiros_anio_inm_ant_per,
            'HuboRetirosAnioInmAnt': hubo_retiros_anio_inm_ant,
            'MontTotAportAnioInmAnterior': mont_tot_aport_anio_inm_anterior,
            'MontTotRetiradoAnioInmAntPer': mont_tot_retirado_anio_inm_ant_per,
            'MontTotExentRetiradoAnioInmAnt': mont_tot_exent_retirado_anio_inm_ant,
            'MontTotExedenteAnioInmAnt': mont_tot_exedente_anio_inm_ant,
            'MontTotRetiradoAnioInmAnt': mont_tot_retirado_anio_inm_ant,
            'NumReferencia': num_referencia,
            'AportacionesODepositos': aportaciones_odepositos,
        })
        

