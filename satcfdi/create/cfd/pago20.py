"""pago20 http://www.sat.gob.mx/Pagos20"""
from collections.abc import *
from datetime import datetime
from decimal import Decimal

from ..compute import make_impuestos_p, make_pago_totales
from ...utils import iterate
from ...cfdi import CFDI
from ...utils import ScalarMap


class TrasladoDR(ScalarMap):
    """
    Nodo requerido para asentar la información detallada de un traslado de impuesto específico conforme al monto del pago recibido.

    :param base_dr: Atributo requerido para señalar la base para el cálculo del impuesto trasladado conforme al monto del pago, aplicable al documento relacionado, la determinación de la base se realiza de acuerdo con las disposiciones fiscales vigentes. No se permiten valores negativos.
    :param impuesto_dr: Atributo requerido para señalar la clave del tipo de impuesto trasladado conforme al monto del pago, aplicable al documento relacionado.
    :param tipo_factor_dr: Atributo requerido para señalar la clave del tipo de factor que se aplica a la base del impuesto.
    :param tasa_o_cuota_dr: Atributo condicional para señalar el valor de la tasa o cuota del impuesto que se traslada. Es requerido cuando el atributo TipoFactorDR contenga una clave que corresponda a Tasa o Cuota.
    :param importe_dr: Atributo condicional para señalar el importe del impuesto trasladado conforme al monto del pago, aplicable al documento relacionado. No se permiten valores negativos. Es requerido cuando el tipo factor sea Tasa o Cuota.
    """

    def __init__(
            self,
            base_dr: Decimal | int,
            impuesto_dr: str,
            tipo_factor_dr: str,
            tasa_o_cuota_dr: Decimal | int = None,
            importe_dr: Decimal | int = None,
    ):
        super().__init__({
            'BaseDR': base_dr,
            'ImpuestoDR': impuesto_dr,
            'TipoFactorDR': tipo_factor_dr,
            'TasaOCuotaDR': tasa_o_cuota_dr,
            'ImporteDR': importe_dr,
        })
        

class RetencionDR(ScalarMap):
    """
    Nodo requerido para registrar la información detallada de una retención de impuesto específico conforme al monto del pago recibido.

    :param base_dr: Atributo requerido para señalar la base para el cálculo de la retención conforme al monto del pago, aplicable al documento relacionado, la determinación de la base se realiza de acuerdo con las disposiciones fiscales vigentes. No se permiten valores negativos.
    :param impuesto_dr: Atributo requerido para señalar la clave del tipo de impuesto retenido conforme al monto del pago, aplicable al documento relacionado.
    :param tipo_factor_dr: Atributo requerido para señalar la clave del tipo de factor que se aplica a la base del impuesto.
    :param tasa_o_cuota_dr: Atributo requerido para señalar el valor de la tasa o cuota del impuesto que se retiene.
    :param importe_dr: Atributo requerido para señalar el importe del impuesto retenido conforme al monto del pago, aplicable al documento relacionado. No se permiten valores negativos.
    """

    def __init__(
            self,
            base_dr: Decimal | int,
            impuesto_dr: str,
            tipo_factor_dr: str,
            tasa_o_cuota_dr: Decimal | int,
            importe_dr: Decimal | int,
    ):
        super().__init__({
            'BaseDR': base_dr,
            'ImpuestoDR': impuesto_dr,
            'TipoFactorDR': tipo_factor_dr,
            'TasaOCuotaDR': tasa_o_cuota_dr,
            'ImporteDR': importe_dr,
        })
        

class ImpuestosDR(ScalarMap):
    """
    Nodo condicional para registrar los impuestos aplicables conforme al monto del pago recibido, expresados a la moneda del documento relacionado.

    :param retenciones_dr: Nodo opcional para capturar los impuestos retenidos aplicables conforme al monto del pago recibido.
    :param traslados_dr: Nodo opcional para capturar los impuestos trasladados aplicables conforme al monto del pago recibido.
    """

    def __init__(
            self,
            retenciones_dr: Sequence[RetencionDR | dict] = None,
            traslados_dr: Sequence[TrasladoDR | dict] = None,
    ):
        super().__init__({
            'RetencionesDR': retenciones_dr,
            'TrasladosDR': traslados_dr,
        })
        

class DoctoRelacionado(ScalarMap):
    """
    Nodo requerido para expresar la lista de documentos relacionados con los pagos. Por cada documento que se relacione se debe generar un nodo DoctoRelacionado.

    :param id_documento: Atributo requerido para expresar el identificador del documento relacionado con el pago. Este dato puede ser un Folio Fiscal de la Factura Electrónica o bien el número de operación de un documento digital.
    :param moneda_dr: Atributo requerido para identificar la clave de la moneda utilizada en los importes del documento relacionado, cuando se usa moneda nacional o el documento relacionado no especifica la moneda se registra MXN. Los importes registrados en los atributos “ImpSaldoAnt”, “ImpPagado” e “ImpSaldoInsoluto” de éste nodo, deben corresponder a esta moneda. Conforme con la especificación ISO 4217.
    :param num_parcialidad: Atributo requerido para expresar el número de parcialidad que corresponde al pago.
    :param imp_saldo_ant: Atributo requerido para expresar el monto del saldo insoluto de la parcialidad anterior. En el caso de que sea la primer parcialidad este atributo debe contener el importe total del documento relacionado.
    :param imp_pagado: Atributo requerido para expresar el importe pagado para el documento relacionado.
    :param objeto_imp_dr: Atributo requerido para expresar si el pago del documento relacionado es objeto o no de impuesto.
    :param serie: Atributo opcional para precisar la serie del comprobante para control interno del contribuyente, acepta una cadena de caracteres.
    :param folio: Atributo opcional para precisar el folio del comprobante para control interno del contribuyente, acepta una cadena de caracteres.
    :param equivalencia_dr: Atributo condicional para expresar el tipo de cambio conforme con la moneda registrada en el documento relacionado. Es requerido cuando la moneda del documento relacionado es distinta de la moneda de pago. Se debe registrar el número de unidades de la moneda señalada en el documento relacionado que equivalen a una unidad de la moneda del pago. Por ejemplo: El documento relacionado se registra en USD. El pago se realiza por 100 EUR. Este atributo se registra como 1.114700 USD/EUR. El importe pagado equivale a 100 EUR * 1.114700 USD/EUR = 111.47 USD.
    :param impuestos_dr: Nodo condicional para registrar los impuestos aplicables conforme al monto del pago recibido, expresados a la moneda del documento relacionado.
    """

    def __init__(
            self,
            id_documento: str,
            moneda_dr: str,
            num_parcialidad: int,
            imp_saldo_ant: Decimal | int,
            imp_pagado: Decimal | int,
            objeto_imp_dr: str,
            serie: str = None,
            folio: str = None,
            equivalencia_dr: Decimal | int = None,
            impuestos_dr: ImpuestosDR | dict = None,
    ):
        super().__init__({
            'IdDocumento': id_documento,
            'MonedaDR': moneda_dr,
            'NumParcialidad': num_parcialidad,
            'ImpSaldoAnt': imp_saldo_ant,
            'ImpPagado': imp_pagado,
            'ObjetoImpDR': objeto_imp_dr,
            'Serie': serie,
            'Folio': folio,
            'EquivalenciaDR': equivalencia_dr,
            'ImpuestosDR': impuestos_dr,
        })
        

class Pago(ScalarMap):
    """
    Elemento requerido para incorporar la información de la recepción de pagos.

    :param fecha_pago: Atributo requerido para expresar la fecha y hora en la que el beneficiario recibe el pago. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.En caso de no contar con la hora se debe registrar 12:00:00.
    :param forma_de_pago_p: Atributo requerido para expresar la clave de la forma en que se realiza el pago.
    :param moneda_p: Atributo requerido para identificar la clave de la moneda utilizada para realizar el pago conforme a la especificación ISO 4217. Cuando se usa moneda nacional se registra MXN. El atributo Pagos:Pago:Monto debe ser expresado en la moneda registrada en este atributo.
    :param monto: Atributo requerido para expresar el importe del pago.
    :param docto_relacionado: Nodo requerido para expresar la lista de documentos relacionados con los pagos. Por cada documento que se relacione se debe generar un nodo DoctoRelacionado.
    :param tipo_cambio_p: Atributo condicional para expresar el tipo de cambio de la moneda a la fecha en que se realizó el pago. El valor debe reflejar el número de pesos mexicanos que equivalen a una unidad de la divisa señalada en el atributo MonedaP. Es requerido cuando el atributo MonedaP es diferente a MXN.
    :param num_operacion: Atributo condicional para expresar el número de cheque, número de autorización, número de referencia, clave de rastreo en caso de ser SPEI, línea de captura o algún número de referencia análogo que identifique la operación que ampara el pago efectuado.
    :param rfc_emisor_cta_ord: Atributo condicional para expresar la clave RFC de la entidad emisora de la cuenta origen, es decir, la operadora, el banco, la institución financiera, emisor de monedero electrónico, etc., en caso de ser extranjero colocar XEXX010101000, considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param nom_banco_ord_ext: Atributo condicional para expresar el nombre del banco ordenante, es requerido en caso de ser extranjero. Considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param cta_ordenante: Atributo condicional para incorporar el número de la cuenta con la que se realizó el pago. Considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param rfc_emisor_cta_ben: Atributo condicional para expresar la clave RFC de la entidad operadora de la cuenta destino, es decir, la operadora, el banco, la institución financiera, emisor de monedero electrónico, etc. Considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param cta_beneficiario: Atributo condicional para incorporar el número de cuenta en donde se recibió el pago. Considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param tipo_cad_pago: Atributo condicional para identificar la clave del tipo de cadena de pago que genera la entidad receptora del pago. Considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param cert_pago: Atributo condicional que sirve para incorporar el certificado que ampara al pago, como una cadena de texto en formato base 64. Es requerido en caso de que el atributo TipoCadPago contenga información.
    :param cad_pago: Atributo condicional para expresar la cadena original del comprobante de pago generado por la entidad emisora de la cuenta beneficiaria. Es requerido en caso de que el atributo TipoCadPago contenga información.
    :param sello_pago: Atributo condicional para integrar el sello digital que se asocie al pago. La entidad que emite el comprobante de pago, ingresa una cadena original y el sello digital en una sección de dicho comprobante, este sello digital es el que se debe registrar en este atributo. Debe ser expresado como una cadena de texto en formato base 64. Es requerido en caso de que el atributo TipoCadPago contenga información.
    :param impuestos_p: Nodo condicional para registrar el resumen de los impuestos aplicables conforme al monto del pago recibido, expresados a la moneda de pago.
    """

    def __init__(
            self,
            fecha_pago: datetime,
            forma_de_pago_p: str,
            moneda_p: str,
            docto_relacionado: Sequence[DoctoRelacionado | dict],
            monto: Decimal | int = None,
            tipo_cambio_p: Decimal | int = None,
            num_operacion: str = None,
            rfc_emisor_cta_ord: str = None,
            nom_banco_ord_ext: str = None,
            cta_ordenante: str = None,
            rfc_emisor_cta_ben: str = None,
            cta_beneficiario: str = None,
            tipo_cad_pago: str = None,
            cert_pago: str = None,
            cad_pago: str = None,
            sello_pago: str = None,
    ):
        super().__init__({
            'FechaPago': fecha_pago,
            'FormaDePagoP': forma_de_pago_p,
            'MonedaP': moneda_p,
            'Monto': monto,
            'TipoCambioP': tipo_cambio_p,
            'NumOperacion': num_operacion,
            'RfcEmisorCtaOrd': rfc_emisor_cta_ord,
            'NomBancoOrdExt': nom_banco_ord_ext,
            'CtaOrdenante': cta_ordenante,
            'RfcEmisorCtaBen': rfc_emisor_cta_ben,
            'CtaBeneficiario': cta_beneficiario,
            'TipoCadPago': tipo_cad_pago,
            'CertPago': cert_pago,
            'CadPago': cad_pago,
            'SelloPago': sello_pago,
            'DoctoRelacionado': docto_relacionado,
        })


# MAIN #
class Pagos(CFDI):
    """
    Complemento para el Comprobante Fiscal Digital por Internet (CFDI) para registrar información sobre la recepción de pagos. El emisor de este complemento para recepción de pagos debe ser quien las leyes le obligue a expedir comprobantes por los actos o actividades que realicen, por los ingresos que se perciban o por las retenciones de contribuciones que efectúen.

    :param pago: Elemento requerido para incorporar la información de la recepción de pagos.
    :return: objeto CFDI
    """

    tag = '{http://www.sat.gob.mx/Pagos20}Pagos'
    version = '2.0'

    def __init__(
            self,
            pago: Sequence[Pago | dict],
    ):
        for p in iterate(pago):
            docto_relacionado = p['DoctoRelacionado']
            for d in iterate(docto_relacionado):
                d['ImpSaldoInsoluto'] = d['ImpSaldoAnt'] - d['ImpPagado']

            p['Monto'] = sum(c["ImpPagado"] / (c.get('EquivalenciaDR') or 1) for c in iterate(docto_relacionado))
            p['ImpuestosP'] = make_impuestos_p(docto_relacionado)

        totales = make_pago_totales(pago)

        super().__init__({
            'Version': self.version,
            'Totales': totales,
            'Pago': pago,
        })
