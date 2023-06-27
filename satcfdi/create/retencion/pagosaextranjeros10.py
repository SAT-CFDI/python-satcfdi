"""pagosaextranjeros http://www.sat.gob.mx/esquemas/retencionpago/1/pagosaextranjeros"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Beneficiario(ScalarMap):
    """
    Nodo opcional para precisar la información del representante para efectos fiscales en México
    
    :param rfc: Atributo requerido para expresar la clave del registro federal de contribuyentes del representante legal en México
    :param curp: Atributo requerido para la expresión de la CURP del representante legal
    :param nom_den_raz_soc_b: Atributo requerido para expresar el nombre, denominación o razón social del contribuyente en México
    :param concepto_pago: Atributo requerido para expresar el tipo de contribuyente sujeto a la retención, conforme al catálogo.
    :param descripcion_concepto: Atributo requerido para expresar la descripción de la definición del pago del residente en el extranjero
    """
    
    def __init__(
            self,
            rfc: str,
            curp: str,
            nom_den_raz_soc_b: str,
            concepto_pago: str,
            descripcion_concepto: str,
    ): 
        super().__init__({
            'RFC': rfc,
            'CURP': curp,
            'NomDenRazSocB': nom_den_raz_soc_b,
            'ConceptoPago': concepto_pago,
            'DescripcionConcepto': descripcion_concepto,
        })
        

class NoBeneficiario(ScalarMap):
    """
    Nodo opcional para expresar la información del residente extranjero efectivo del cobro
    
    :param pais_de_resid_para_efec_fisc: Atributo requerido para expresar la clave del país de residencia del extranjero, conforme al catálogo.
    :param concepto_pago: Atributo requerido para expresar el tipo contribuyente sujeto a la retención, conforme al catálogo.
    :param descripcion_concepto: Atributo requerido para expresar la descripción de la definición del pago del residente en el extranjero
    """
    
    def __init__(
            self,
            pais_de_resid_para_efec_fisc: str,
            concepto_pago: str,
            descripcion_concepto: str,
    ): 
        super().__init__({
            'PaisDeResidParaEfecFisc': pais_de_resid_para_efec_fisc,
            'ConceptoPago': concepto_pago,
            'DescripcionConcepto': descripcion_concepto,
        })
        

class Pagosaextranjeros(CFDI):
    """
    Complemento para expresar los pagos que se realizan a residentes en el extranjero
    
    :param es_benef_efect_del_cobro: Atributo requerido para expresar si el beneficiario del pago es la misma persona que retiene
    :param no_beneficiario: Nodo opcional para expresar la información del residente extranjero efectivo del cobro
    :param beneficiario: Nodo opcional para precisar la información del representante para efectos fiscales en México
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/pagosaextranjeros}Pagosaextranjeros'
    version = '1.0'
    
    def __init__(
            self,
            es_benef_efect_del_cobro: str,
            no_beneficiario: NoBeneficiario | dict = None,
            beneficiario: Beneficiario | dict = None,
    ): 
        super().__init__({
            'Version': self.version,
            'EsBenefEfectDelCobro': es_benef_efect_del_cobro,
            'NoBeneficiario': no_beneficiario,
            'Beneficiario': beneficiario,
        })
        

