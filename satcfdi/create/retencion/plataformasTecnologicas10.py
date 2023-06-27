"""plataformasTecnologicas http://www.sat.gob.mx/esquemas/retencionpago/1/PlataformasTecnologicas10"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class ComisionDelServicio(ScalarMap):
    """
    Nodo condicional para detallar la información de la comisión pagada por el uso de plataformas tecnológicas por cada servicio prestado o enajenación relacionado.
    
    :param importe: Atributo requerido para detallar el valor del importe cobrado por la comisión del uso del servicio de las plataformas tecnológicas.
    :param base: Atributo opcional para registrar la base de la comisión del servicio de la plataforma, pagadas por personas físicas o personas morales utilizando plataformas tecnológicas.
    :param porcentaje: Atributo opcional para detallar el valor del porcentaje cobrado por la comisión del uso del servicio de las plataformas tecnológicas.
    """
    
    def __init__(
            self,
            importe: Decimal | int,
            base: Decimal | int = None,
            porcentaje: Decimal | int = None,
    ): 
        super().__init__({
            'Importe': importe,
            'Base': base,
            'Porcentaje': porcentaje,
        })
        

class ContribucionGubernamental(ScalarMap):
    """
    Nodo opcional para detallar la información de las contribuciones gubernamentales pagadas por los servicios realizados por personas físicas utilizando plataformas tecnológicas; por ejemplo, impuesto sobre hospedaje.
    
    :param imp_contrib: Atributo requerido para registrar el importe de la contribución gubernamental pagada por los servicios realizados por personas físicas utilizando plataformas tecnológicas.
    :param entidad_donde_paga_la_contribucion: Atributo requerido para registrar la clave de la Entidad Federativa donde se efectúa el pago de la contribución gubernamental.
    """
    
    def __init__(
            self,
            imp_contrib: Decimal | int,
            entidad_donde_paga_la_contribucion: str,
    ): 
        super().__init__({
            'ImpContrib': imp_contrib,
            'EntidadDondePagaLaContribucion': entidad_donde_paga_la_contribucion,
        })
        

class ImpuestosTrasladadosdelServicio(ScalarMap):
    """
    Nodo condicional para detallar la información de los impuestos trasladados respecto de las operaciones realizadas por personas físicas o personas morales utilizando plataformas tecnológicas.
    
    :param base: Atributo requerido para señalar la base para el cálculo del impuesto, la determinación de la base se realiza de acuerdo con las disposiciones fiscales vigentes. No se permiten valores negativos.
    :param impuesto: Atributo requerido para señalar la clave del tipo de impuesto trasladado aplicable al bien o servicio.
    :param tasa_cuota: Atributo requerido para señalar el valor de la tasa o cuota del impuesto que se traslada para el bien o servicio.
    :param importe: Atributo requerido para señalar el importe del impuesto trasladado que aplica al bien o servicio. No se permiten valores negativos.
    """
    
    tipo_factor = 'Tasa'
    def __init__(
            self,
            base: Decimal | int,
            impuesto: str,
            tasa_cuota: Decimal | int,
            importe: Decimal | int,
    ): 
        super().__init__({
            'Base': base,
            'Impuesto': impuesto,
            'TipoFactor': self.tipo_factor,
            'TasaCuota': tasa_cuota,
            'Importe': importe,
        })
        

class DetallesDelServicio(ScalarMap):
    """
    Nodo requerido para detallar la información de la enajenación de bienes y los tipos de servicios realizadas por personas físicas o personas morales utilizando plataformas tecnológicas.
    
    :param forma_pago_serv: Atributo requerido para expresar la clave de la forma de pago con la que se liquida el servicio prestado o la enajenación de bienes.
    :param tipo_de_serv: Atributo requerido para expresar la clave del tipo de servicio prestado o la enajenación de bienes, según corresponda.
    :param fecha_serv: Atributo requerido para expresar la fecha en la que el cliente paga el servicio o el bien.
    :param precio_serv_sin_iva: Atributo requerido para expresar el precio del bien o servicio (sin incluir IVA).
    :param sub_tip_serv: Atributo condicional para identificar el subtipo del servicio prestado.
    :param rfc_tercero_autorizado: Atributo opcional para registrar el RFC del tercero autorizado como personal de apoyo, por quien está registrado en la plataforma tecnológica para prestar servicios o en su caso, enajenar bienes.
    :param impuestos_trasladadosdel_servicio: Nodo condicional para detallar la información de los impuestos trasladados respecto de las operaciones realizadas por personas físicas o personas morales utilizando plataformas tecnológicas.
    :param contribucion_gubernamental: Nodo opcional para detallar la información de las contribuciones gubernamentales pagadas por los servicios realizados por personas físicas utilizando plataformas tecnológicas; por ejemplo, impuesto sobre hospedaje.
    :param comision_del_servicio: Nodo condicional para detallar la información de la comisión pagada por el uso de plataformas tecnológicas por cada servicio prestado o enajenación relacionado.
    """
    
    def __init__(
            self,
            forma_pago_serv: str,
            tipo_de_serv: str,
            fecha_serv: date,
            precio_serv_sin_iva: Decimal | int,
            sub_tip_serv: str = None,
            rfc_tercero_autorizado: str = None,
            impuestos_trasladadosdel_servicio: ImpuestosTrasladadosdelServicio | dict = None,
            contribucion_gubernamental: ContribucionGubernamental | dict = None,
            comision_del_servicio: ComisionDelServicio | dict = None,
    ): 
        super().__init__({
            'FormaPagoServ': forma_pago_serv,
            'TipoDeServ': tipo_de_serv,
            'FechaServ': fecha_serv,
            'PrecioServSinIVA': precio_serv_sin_iva,
            'SubTipServ': sub_tip_serv,
            'RFCTerceroAutorizado': rfc_tercero_autorizado,
            'ImpuestosTrasladadosdelServicio': impuestos_trasladadosdel_servicio,
            'ContribucionGubernamental': contribucion_gubernamental,
            'ComisionDelServicio': comision_del_servicio,
        })
        

class ServiciosPlataformasTecnologicas(CFDI):
    """
    Complemento para expresar la información sobre la enajenación de bienes y los servicios prestados por personas físicas o personas morales que utilicen plataformas tecnológicas.
    
    :param periodicidad: Atributo requerido para especificar el periodo de retención.
    :param num_serv: Atributo requerido para expresar el número de operaciones celebradas por concepto de servicios o enajenación de bienes realizadas en el periodo.
    :param mon_tot_serv_siva: Atributo requerido para expresar monto total de las operaciones realizadas en el periodo, sin incluir el monto del IVA; según corresponda.
    :param total_iva_trasladado: Atributo requerido para expresar el monto total del IVA trasladado por las operaciones realizadas en el periodo.
    :param total_iva_retenido: Atributo requerido para expresar el monto total del IVA retenido por las operaciones realizadas en el periodo.
    :param total_isr_retenido: Atributo requerido para expresar el monto total del ISR retenido por las operaciones realizadas en el periodo.
    :param dif_iva_entregado_prest_serv: Atributo requerido para expresar la diferencia del IVA entregado al prestador del servicio o enajenante de bienes en el periodo.
    :param mon_totalpor_uso_plataforma: Atributo requerido para expresar el monto total cobrado al prestador del servicio o enajenante de bienes por el uso de la plataforma en el periodo.
    :param servicios: Nodo requerido para detallar la información de operaciones celebradas por personas físicas o personas morales que utilicen plataformas tecnológicas.
    :param mon_total_contribucion_gubernamental: Atributo condicional para expresar la suma de los atributos “ImpContrib“ del nodo hijo “ContribucionGubernamental” del periodo que corresponda.
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/PlataformasTecnologicas10}ServiciosPlataformasTecnologicas'
    version = '1.0'
    
    def __init__(
            self,
            periodicidad: str,
            num_serv: int,
            mon_tot_serv_siva: Decimal | int,
            total_iva_trasladado: Decimal | int,
            total_iva_retenido: Decimal | int,
            total_isr_retenido: Decimal | int,
            dif_iva_entregado_prest_serv: Decimal | int,
            mon_totalpor_uso_plataforma: Decimal | int,
            servicios: DetallesDelServicio | dict | Sequence[DetallesDelServicio | dict],
            mon_total_contribucion_gubernamental: Decimal | int = None,
    ): 
        super().__init__({
            'Version': self.version,
            'Periodicidad': periodicidad,
            'NumServ': num_serv,
            'MonTotServSIVA': mon_tot_serv_siva,
            'TotalIVATrasladado': total_iva_trasladado,
            'TotalIVARetenido': total_iva_retenido,
            'TotalISRRetenido': total_isr_retenido,
            'DifIVAEntregadoPrestServ': dif_iva_entregado_prest_serv,
            'MonTotalporUsoPlataforma': mon_totalpor_uso_plataforma,
            'Servicios': servicios,
            'MonTotalContribucionGubernamental': mon_total_contribucion_gubernamental,
        })
        

