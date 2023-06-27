"""pago10 http://www.sat.gob.mx/Pagos"""
from collections.abc import *
from datetime import datetime
from decimal import Decimal

from ...cfdi import CFDI
from ...utils import ScalarMap
from ...utils import iterate


class Traslado(ScalarMap):
    """
    Nodo requerido para la información detallada de un traslado de impuesto específico.

    :param impuesto: Atributo requerido para señalar la clave del tipo de impuesto trasladado.
    :param tipo_factor: Atributo requerido para señalar la clave del tipo de factor que se aplica a la base del impuesto.
    :param tasa_o_cuota: Atributo requerido para señalar el valor de la tasa o cuota del impuesto que se traslada.
    :param importe: Atributo requerido para señalar el importe del impuesto trasladado. No se permiten valores negativos.
    """

    def __init__(
            self,
            impuesto: str,
            tipo_factor: str,
            tasa_o_cuota: Decimal | int,
            importe: Decimal | int,
    ):
        super().__init__({
            'Impuesto': impuesto,
            'TipoFactor': tipo_factor,
            'TasaOCuota': tasa_o_cuota,
            'Importe': importe,
        })


class Retencion(ScalarMap):
    """
    Nodo requerido para registrar la información detallada de una retención de impuesto específico.

    :param impuesto: Atributo requerido para señalar la clave del tipo de impuesto retenido.
    :param importe: Atributo requerido para señalar el importe o monto del impuesto retenido. No se permiten valores negativos.
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
    Nodo condicional para expresar el resumen de los impuestos aplicables cuando este documento sea un anticipo.

    :param total_impuestos_retenidos: Atributo condicional para expresar el total de los impuestos retenidos que se desprenden del pago. No se permiten valores negativos.
    :param total_impuestos_trasladados: Atributo condicional para expresar el total de los impuestos trasladados que se desprenden del pago. No se permiten valores negativos.
    :param retenciones: Nodo condicional para capturar los impuestos retenidos aplicables.
    :param traslados: Nodo condicional para capturar los impuestos trasladados aplicables.
    """

    def __init__(
            self,
            total_impuestos_retenidos: Decimal | int = None,
            total_impuestos_trasladados: Decimal | int = None,
            retenciones: Sequence[Retencion | dict] = None,
            traslados: Sequence[Traslado | dict] = None,
    ):
        super().__init__({
            'TotalImpuestosRetenidos': total_impuestos_retenidos,
            'TotalImpuestosTrasladados': total_impuestos_trasladados,
            'Retenciones': retenciones,
            'Traslados': traslados,
        })


class DoctoRelacionado(ScalarMap):
    """
    Nodo condicional para expresar la lista de documentos relacionados con los pagos diferentes de anticipos. Por cada documento que se relacione se debe generar un nodo DoctoRelacionado.

    :param id_documento: Atributo requerido para expresar el identificador del documento relacionado con el pago. Este dato puede ser un Folio Fiscal de la Factura Electrónica o bien el número de operación de un documento digital.
    :param moneda_dr: Atributo requerido para identificar la clave de la moneda utilizada en los importes del documento relacionado, cuando se usa moneda nacional o el documento relacionado no especifica la moneda se registra MXN. Los importes registrados en los atributos “ImpSaldoAnt”, “ImpPagado” e “ImpSaldoInsoluto” de éste nodo, deben corresponder a esta moneda. Conforme con la especificación ISO 4217.
    :param metodo_de_pago_dr: Atributo requerido para expresar la clave del método de pago que se registró en el documento relacionado.
    :param serie: Atributo opcional para precisar la serie del comprobante para control interno del contribuyente, acepta una cadena de caracteres.
    :param folio: Atributo opcional para precisar el folio del comprobante para control interno del contribuyente, acepta una cadena de caracteres.
    :param tipo_cambio_dr: Atributo condicional para expresar el tipo de cambio conforme con la moneda registrada en el documento relacionado. Es requerido cuando la moneda del documento relacionado es distinta de la moneda de pago. Se debe registrar el número de unidades de la moneda señalada en el documento relacionado que equivalen a una unidad de la moneda del pago. Por ejemplo: El documento relacionado se registra en USD El pago se realiza por 100 EUR. Este atributo se registra como 1.114700 USD/EUR. El importe pagado equivale a 100 EUR * 1.114700 USD/EUR = 111.47 USD.
    :param num_parcialidad: Atributo condicional para expresar el número de parcialidad que corresponde al pago. Es requerido cuando MetodoDePagoDR contiene: “PPD” Pago en parcialidades o diferido.
    :param imp_saldo_ant: Atributo condicional para expresar el monto del saldo insoluto de la parcialidad anterior. Es requerido cuando MetodoDePagoDR contiene: “PPD” Pago en parcialidades o diferido.En el caso de que sea la primer parcialidad este campo debe contener el importe total del documento relacionado.
    :param imp_pagado: Atributo condicional para expresar el importe pagado para el documento relacionado. Es obligatorio cuando exista más de un documento relacionado o cuando existe un documento relacionado y el TipoCambioDR tiene un valor.
    """

    def __init__(
            self,
            id_documento: str,
            moneda_dr: str,
            metodo_de_pago_dr: str,
            serie: str = None,
            folio: str = None,
            tipo_cambio_dr: Decimal | int = None,
            num_parcialidad: int = None,
            imp_saldo_ant: Decimal | int = None,
            imp_pagado: Decimal | int = None,
    ):
        super().__init__({
            'IdDocumento': id_documento,
            'MonedaDR': moneda_dr,
            'MetodoDePagoDR': metodo_de_pago_dr,
            'Serie': serie,
            'Folio': folio,
            'TipoCambioDR': tipo_cambio_dr,
            'NumParcialidad': num_parcialidad,
            'ImpSaldoAnt': imp_saldo_ant,
            'ImpPagado': imp_pagado
        })


class Pago(ScalarMap):
    """
    Elemento requerido para incorporar la información de la recepción de pagos.

    :param fecha_pago: Atributo requerido para expresar la fecha y hora en la que el beneficiario recibe el pago. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.En caso de no contar con la hora se debe registrar 12:00:00.
    :param forma_de_pago_p: Atributo requerido para expresar la clave de la forma en que se realiza el pago.
    :param moneda_p: Atributo requerido para identificar la clave de la moneda utilizada para realizar el pago, cuando se usa moneda nacional se registra MXN. El atributo Pagos:Pago:Monto y los atributos TotalImpuestosRetenidos, TotalImpuestosTrasladados, Traslados:Traslado:Importe y Retenciones:Retencion:Importe del nodo Pago:Impuestos deben ser expresados en esta moneda. Conforme con la especificación ISO 4217.
    :param tipo_cambio_p: Atributo condicional para expresar el tipo de cambio de la moneda a la fecha en que se realizó el pago. El valor debe reflejar el número de pesos mexicanos que equivalen a una unidad de la divisa señalada en el atributo MonedaP. Es requerido cuando el atributo MonedaP es diferente a MXN.
    :param num_operacion: Atributo condicional para expresar el número de cheque, número de autorización, número de referencia, clave de rastreo en caso de ser SPEI, línea de captura o algún número de referencia análogo que identifique la operación que ampara el pago efectuado
    :param rfc_emisor_cta_ord: Atributo condicional para expresar la clave RFC de la entidad emisora de la cuenta origen, es decir, la operadora, el banco, la institución financiera, emisor de monedero electrónico, etc., en caso de ser extranjero colocar XEXX010101000, considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param nom_banco_ord_ext: Atributo condicional para expresar el nombre del banco ordenante, es requerido en caso de ser extranjero. Considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param cta_ordenante: Atributo condicional para incorporar el número de la cuenta con la que se realizó el pago. Considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago
    :param rfc_emisor_cta_ben: Atributo condicional para expresar la clave RFC de la entidad operadora de la cuenta destino, es decir, la operadora, el banco, la institución financiera, emisor de monedero electrónico, etc. Considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param cta_beneficiario: Atributo condicional para incorporar el número de cuenta en donde se recibió el pago. Considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param tipo_cad_pago: Atributo condicional para identificar la clave del tipo de cadena de pago que genera la entidad receptora del pago. Considerar las reglas de obligatoriedad publicadas en la página del SAT para éste atributo de acuerdo con el catálogo catCFDI:c_FormaPago.
    :param cert_pago: Atributo condicional que sirve para incorporar el certificado que ampara al pago, como una cadena de texto en formato base 64. Es requerido en caso de que el atributo TipoCadPago contenga información.
    :param cad_pago: Atributo condicional para expresar la cadena original del comprobante de pago generado por la entidad emisora de la cuenta beneficiaria. Es requerido en caso de que el atributo TipoCadPago contenga información.
    :param sello_pago: Atributo condicional para integrar el sello digital que se asocie al pago. La entidad que emite el comprobante de pago, ingresa una cadena original y el sello digital en una sección de dicho comprobante, este sello digital es el que se debe registrar en este campo. Debe ser expresado como una cadena de texto en formato base 64. Es requerido en caso de que el atributo TipoCadPago contenga información.
    :param docto_relacionado: Nodo condicional para expresar la lista de documentos relacionados con los pagos diferentes de anticipos. Por cada documento que se relacione se debe generar un nodo DoctoRelacionado.
    :param impuestos: Nodo condicional para expresar el resumen de los impuestos aplicables cuando este documento sea un anticipo.
    """

    def __init__(
            self,
            fecha_pago: datetime,
            forma_de_pago_p: str,
            moneda_p: str,
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
            docto_relacionado: Sequence[DoctoRelacionado | dict] = None,
            impuestos: Sequence[Impuestos | dict] = None,
    ):
        super().__init__({
            'FechaPago': fecha_pago,
            'FormaDePagoP': forma_de_pago_p,
            'MonedaP': moneda_p,
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
            'Impuestos': impuestos,
        })


class Pagos(CFDI):
    """
    Complemento para el Comprobante Fiscal Digital por Internet (CFDI) para registrar información sobre la recepción de pagos. El emisor de este complemento para recepción de pagos debe ser quien las leyes le obligue a expedir comprobantes por los actos o actividades que realicen, por los ingresos que se perciban o por las retenciones de contribuciones que efectúen.

    :param pago: Elemento requerido para incorporar la información de la recepción de pagos.
    """

    tag = '{http://www.sat.gob.mx/Pagos}Pagos'
    version = '1.0'

    def __init__(
            self,
            pago: Pago | Sequence[Pago | dict],
    ):
        for p in iterate(pago):
            docto_relacionado = p['DoctoRelacionado']
            for d in iterate(docto_relacionado):
                d['ImpSaldoInsoluto'] = d['ImpSaldoAnt'] - d['ImpPagado']

            p['Monto'] = sum(c["ImpPagado"] for c in docto_relacionado)

        super().__init__({
            'Version': self.version,
            'Pago': pago,
        })
