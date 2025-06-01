"""cfdi http://www.sat.gob.mx/cfd/4"""
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from satcfdi.create.cfd.catalogos import Impuesto as CatImpuesto
from . import pago20
from ..compute import make_impuestos, rounder, make_impuesto, \
    make_impuestos_dr_parcial
from ...cfdi import CFDI
from ...transform import get_timezone
from ...utils import ScalarMap
from ...utils import iterate


class CfdiRelacionados(ScalarMap):
    """
    Nodo opcional para precisar la información de los comprobantes relacionados.

    :param tipo_relacion: Atributo requerido para indicar la clave de la relación que existe entre éste que se está generando y el o los CFDI previos.
    :param cfdi_relacionado: Nodo requerido para precisar la información de los comprobantes relacionados.
    """

    def __init__(
            self,
            tipo_relacion: str,
            cfdi_relacionado: str | Sequence[str],
    ):
        super().__init__({
            'TipoRelacion': tipo_relacion,
            'CfdiRelacionado': cfdi_relacionado,
        })


class InformacionGlobal(ScalarMap):
    """
    Nodo condicional para precisar la información relacionada con el comprobante global.

    :param periodicidad: Atributo requerido para expresar el período al que corresponde la información del comprobante global.
    :param meses: Atributo requerido para expresar el mes o los meses al que corresponde la información del comprobante global.
    :param ano: Atributo requerido para expresar el año al que corresponde la información del comprobante global.
    """

    def __init__(
            self,
            periodicidad: str,
            meses: str,
            ano: int,
    ):
        super().__init__({
            'Periodicidad': periodicidad,
            'Meses': meses,
            'Año': ano,
        })


class Parte(ScalarMap):
    """
    Nodo opcional para expresar las partes o componentes que integran la totalidad del concepto expresado en el comprobante fiscal digital por Internet.

    :param clave_prod_serv: Atributo requerido para expresar la clave del producto o del servicio amparado por la presente parte. Es requerido y deben utilizar las claves del catálogo de productos y servicios, cuando los conceptos que registren por sus actividades correspondan con dichos conceptos.
    :param cantidad: Atributo requerido para precisar la cantidad de bienes o servicios del tipo particular definido por la presente parte.
    :param descripcion: Atributo requerido para precisar la descripción del bien o servicio cubierto por la presente parte.
    :param no_identificacion: Atributo opcional para expresar el número de serie, número de parte del bien o identificador del producto o del servicio amparado por la presente parte. Opcionalmente se puede utilizar claves del estándar GTIN.
    :param unidad: Atributo opcional para precisar la unidad de medida propia de la operación del emisor, aplicable para la cantidad expresada en la parte. La unidad debe corresponder con la descripción de la parte.
    :param valor_unitario: Atributo opcional para precisar el valor o precio unitario del bien o servicio cubierto por la presente parte. No se permiten valores negativos.
    :param importe: Atributo opcional para precisar el importe total de los bienes o servicios de la presente parte. Debe ser equivalente al resultado de multiplicar la cantidad por el valor unitario expresado en la parte. No se permiten valores negativos.
    :param informacion_aduanera: Nodo opcional para introducir la información aduanera aplicable cuando se trate de ventas de primera mano de mercancías importadas o se trate de operaciones de comercio exterior con bienes o servicios.
    """

    def __init__(
            self,
            clave_prod_serv: str,
            cantidad: Decimal | int,
            descripcion: str,
            no_identificacion: str = None,
            unidad: str = None,
            valor_unitario: Decimal | int = None,
            importe: Decimal | int = None,
            informacion_aduanera: str | Sequence[str] = None,
    ):
        super().__init__({
            'ClaveProdServ': clave_prod_serv,
            'Cantidad': cantidad,
            'Descripcion': descripcion,
            'NoIdentificacion': no_identificacion,
            'Unidad': unidad,
            'ValorUnitario': valor_unitario,
            'Importe': importe,
            'InformacionAduanera': informacion_aduanera,
        })


class ACuentaTerceros(ScalarMap):
    """
    Nodo opcional para registrar información del contribuyente Tercero, a cuenta del que se realiza la operación.

    :param rfc_a_cuenta_terceros: Atributo requerido para registrar la Clave del Registro Federal de Contribuyentes del contribuyente Tercero, a cuenta del que se realiza la operación.
    :param nombre_a_cuenta_terceros: Atributo requerido para registrar el nombre, denominación o razón social del contribuyente Tercero correspondiente con el Rfc, a cuenta del que se realiza la operación.
    :param regimen_fiscal_a_cuenta_terceros: Atributo requerido para incorporar la clave del régimen del contribuyente Tercero, a cuenta del que se realiza la operación.
    :param domicilio_fiscal_a_cuenta_terceros: Atributo requerido para incorporar el código postal del domicilio fiscal del Tercero, a cuenta del que se realiza la operación.
    """

    def __init__(
            self,
            rfc_a_cuenta_terceros: str,
            nombre_a_cuenta_terceros: str,
            regimen_fiscal_a_cuenta_terceros: str,
            domicilio_fiscal_a_cuenta_terceros: str,
    ):
        super().__init__({
            'RfcACuentaTerceros': rfc_a_cuenta_terceros,
            'NombreACuentaTerceros': nombre_a_cuenta_terceros,
            'RegimenFiscalACuentaTerceros': regimen_fiscal_a_cuenta_terceros,
            'DomicilioFiscalACuentaTerceros': domicilio_fiscal_a_cuenta_terceros,
        })


def _find_impuesto(impuesto):
    try:
        return CatImpuesto[impuesto]
    except KeyError:
        return impuesto


class Traslado(ScalarMap):
    """
    Nodo requerido para la información detallada de un traslado de impuesto específico.

    :param base: Atributo requerido para señalar la suma de los atributos Base de los conceptos del impuesto trasladado. No se permiten valores negativos.
    :param impuesto: Atributo requerido para señalar la clave del tipo de impuesto retencion.
    :param tipo_factor: Atributo requerido para señalar la clave del tipo de factor que se aplica a la base del impuesto.
    :param tasa_o_cuota: Atributo condicional para señalar el valor de la tasa o cuota del impuesto que se traslada por los conceptos amparados en el comprobante.
    :param importe: Atributo condicional para señalar la suma del importe del impuesto trasladado, agrupado por impuesto, TipoFactor y TasaOCuota. No se permiten valores negativos.
    """

    def __init__(
            self,
            impuesto: str,
            tipo_factor: str,
            tasa_o_cuota: Decimal | int = None,
            importe: Decimal | int = None,
            base: Decimal | int = None,
    ):
        super().__init__({
            'Base': base,
            'Impuesto': _find_impuesto(impuesto),
            'TipoFactor': tipo_factor,
            'TasaOCuota': tasa_o_cuota,
            'Importe': importe,
        })


class Retencion(ScalarMap):
    """
    Nodo requerido para la información detallada de un traslado de impuesto específico.

    :param base: Atributo requerido para señalar la suma de los atributos Base de los conceptos del impuesto trasladado. No se permiten valores negativos.
    :param impuesto: Atributo requerido para señalar la clave del tipo de impuesto retencion.
    :param tipo_factor: Atributo requerido para señalar la clave del tipo de factor que se aplica a la base del impuesto.
    :param tasa_o_cuota: Atributo condicional para señalar el valor de la tasa o cuota del impuesto que se traslada por los conceptos amparados en el comprobante.
    :param importe: Atributo condicional para señalar la suma del importe del impuesto trasladado, agrupado por impuesto, TipoFactor y TasaOCuota. No se permiten valores negativos.
    """

    def __init__(
            self,
            impuesto: str,
            tipo_factor: str,
            tasa_o_cuota: Decimal | int = None,
            importe: Decimal | int = None,
            base: Decimal | int = None,
    ):
        super().__init__({
            'Base': base,
            'Impuesto': _find_impuesto(impuesto),
            'TipoFactor': tipo_factor,
            'TasaOCuota': tasa_o_cuota,
            'Importe': importe,
        })


class Impuestos(ScalarMap):
    """
    Nodo condicional para expresar el resumen de los impuestos aplicables.

    :param retenciones: Nodo condicional para capturar los impuestos retenidos aplicables. Es requerido cuando en los conceptos se registre algún impuesto retenido.
    :param traslados: Nodo condicional para capturar los impuestos trasladados aplicables. Es requerido cuando en los conceptos se registre un impuesto trasladado.
    """

    def __init__(
            self,
            retenciones: Retencion | dict | str | Sequence[Retencion | dict | str] = None,
            traslados: Traslado | dict | str | Sequence[Traslado | dict | str] = None,
    ):
        super().__init__({
            'Retenciones': retenciones,
            'Traslados': traslados,
        })


class Concepto(ScalarMap):
    """
    Nodo requerido para registrar la información detallada de un bien o servicio amparado en el comprobante.

    :param clave_prod_serv: Atributo requerido para expresar la clave del producto o del servicio amparado por el presente concepto. Es requerido y deben utilizar las claves del catálogo de productos y servicios, cuando los conceptos que registren por sus actividades correspondan con dichos conceptos.
    :param cantidad: Atributo requerido para precisar la cantidad de bienes o servicios del tipo particular definido por el presente concepto.
    :param clave_unidad: Atributo requerido para precisar la clave de unidad de medida estandarizada aplicable para la cantidad expresada en el concepto. La unidad debe corresponder con la descripción del concepto.
    :param descripcion: Atributo requerido para precisar la descripción del bien o servicio cubierto por el presente concepto.
    :param valor_unitario: Atributo requerido para precisar el valor o precio unitario del bien o servicio cubierto por el presente concepto.
    :param objeto_imp: Atributo requerido para expresar si la operación comercial es objeto o no de impuesto.
    :param no_identificacion: Atributo opcional para expresar el número de parte, identificador del producto o del servicio, la clave de producto o servicio, SKU o equivalente, propia de la operación del emisor, amparado por el presente concepto. Opcionalmente se puede utilizar claves del estándar GTIN.
    :param unidad: Atributo opcional para precisar la unidad de medida propia de la operación del emisor, aplicable para la cantidad expresada en el concepto. La unidad debe corresponder con la descripción del concepto.
    :param descuento: Atributo opcional para representar el importe de los descuentos aplicables al concepto. No se permiten valores negativos.
    :param a_cuenta_terceros: Nodo opcional para registrar información del contribuyente Tercero, a cuenta del que se realiza la operación.
    :param informacion_aduanera: Nodo opcional para introducir la información aduanera aplicable cuando se trate de ventas de primera mano de mercancías importadas o se trate de operaciones de comercio exterior con bienes o servicios.
    :param cuenta_predial: Nodo opcional para asentar el número de cuenta predial con el que fue registrado el inmueble, en el sistema catastral de la entidad federativa de que trate, o bien para incorporar los datos de identificación del certificado de participación inmobiliaria no amortizable.
    :param complemento_concepto: Nodo opcional donde se incluyen los nodos complementarios de extensión al concepto definidos por el SAT, de acuerdo con las disposiciones particulares para un sector o actividad específica.
    :param parte: Nodo opcional para expresar las partes o componentes que integran la totalidad del concepto expresado en el comprobante fiscal digital por Internet.
    :param _traslados_incluidos: si el valor valor_unitario ya incluye traslados.
    """

    def __init__(
            self,
            clave_prod_serv: str,
            cantidad: Decimal | int,
            clave_unidad: str,
            descripcion: str,
            valor_unitario: Decimal | int,
            objeto_imp: str = None,
            no_identificacion: str = None,
            unidad: str = None,
            descuento: Decimal | int = None,
            impuestos: Impuestos | dict = None,
            a_cuenta_terceros: ACuentaTerceros | dict = None,
            informacion_aduanera: str | Sequence[str] = None,
            cuenta_predial: str | Sequence[str] = None,
            complemento_concepto: CFDI | Sequence[CFDI] = None,
            parte: Parte | Sequence[Parte | dict] = None,
            _traslados_incluidos: bool = False
    ):
        super().__init__({
            'ClaveProdServ': clave_prod_serv,
            'Cantidad': cantidad,
            'ClaveUnidad': clave_unidad,
            'Descripcion': descripcion,
            'ValorUnitario': valor_unitario,
            'ObjetoImp': objeto_imp,
            'NoIdentificacion': no_identificacion,
            'Unidad': unidad,
            'Descuento': descuento,
            'Impuestos': impuestos,
            'ACuentaTerceros': a_cuenta_terceros,
            'InformacionAduanera': informacion_aduanera,
            'CuentaPredial': cuenta_predial,
            'ComplementoConcepto': complemento_concepto,
            'Parte': parte,
            '_traslados_incluidos': _traslados_incluidos
        })


class Receptor(ScalarMap):
    """
    Nodo requerido para precisar la información del contribuyente receptor del comprobante.

    :param rfc: Atributo requerido para registrar la Clave del Registro Federal de Contribuyentes correspondiente al contribuyente receptor del comprobante.
    :param nombre: Atributo requerido para registrar el nombre(s), primer apellido, segundo apellido, según corresponda, denominación o razón social del contribuyente, inscrito en el RFC, del receptor del comprobante.
    :param domicilio_fiscal_receptor: Atributo requerido para registrar el código postal del domicilio fiscal del receptor del comprobante.
    :param regimen_fiscal_receptor: Atributo requerido para incorporar la clave del régimen fiscal del contribuyente receptor al que aplicará el efecto fiscal de este comprobante.
    :param uso_cfdi: Atributo requerido para expresar la clave del uso que dará a esta factura el receptor del CFDI.
    :param residencia_fiscal: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del receptor del comprobante, cuando se trate de un extranjero, y que es conforme con la especificación ISO 3166-1 alpha-3. Es requerido cuando se incluya el complemento de comercio exterior o se registre el atributo NumRegIdTrib.
    :param num_reg_id_trib: Atributo condicional para expresar el número de registro de identidad fiscal del receptor cuando sea residente en el extranjero. Es requerido cuando se incluya el complemento de comercio exterior.
    """

    def __init__(
            self,
            rfc: str,
            nombre: str,
            domicilio_fiscal_receptor: str,
            regimen_fiscal_receptor: str,
            uso_cfdi: str,
            residencia_fiscal: str = None,
            num_reg_id_trib: str = None,
    ):
        super().__init__({
            'Rfc': rfc,
            'Nombre': nombre,
            'DomicilioFiscalReceptor': domicilio_fiscal_receptor,
            'RegimenFiscalReceptor': regimen_fiscal_receptor,
            'UsoCFDI': uso_cfdi,
            'ResidenciaFiscal': residencia_fiscal,
            'NumRegIdTrib': num_reg_id_trib,
        })


class Emisor(ScalarMap):
    """
    Nodo requerido para expresar la información del contribuyente emisor del comprobante.

    :param rfc: Atributo requerido para registrar la Clave del Registro Federal de Contribuyentes correspondiente al contribuyente emisor del comprobante.
    :param nombre: Atributo requerido para registrar el nombre, denominación o razón social del contribuyente inscrito en el RFC, del emisor del comprobante.
    :param regimen_fiscal: Atributo requerido para incorporar la clave del régimen del contribuyente emisor al que aplicará el efecto fiscal de este comprobante.
    :param fac_atr_adquirente: Atributo condicional para expresar el número de operación proporcionado por el SAT cuando se trate de un comprobante a través de un PCECFDI o un PCGCFDISP.
    """

    def __init__(
            self,
            rfc: str,
            nombre: str,
            regimen_fiscal: str,
            fac_atr_adquirente: str = None,
    ):
        super().__init__({
            'Rfc': rfc,
            'Nombre': nombre,
            'RegimenFiscal': regimen_fiscal,
            'FacAtrAdquirente': fac_atr_adquirente,
        })


@dataclass
class PagoComprobante:
    comprobante: CFDI
    num_parcialidad: int = None
    imp_saldo_ant: Decimal | int = None
    imp_pagado: Decimal | int = None

    def __post_init__(self):
        if self.num_parcialidad is None and self.imp_saldo_ant is None and self.imp_pagado is None:
            self.num_parcialidad = 1
            self.imp_saldo_ant = self.comprobante['Total']
            self.imp_pagado = self.comprobante['Total']

        if self.imp_pagado > self.imp_saldo_ant:
            raise ValueError('Importe Pagado debe de ser menor o igual al Importe Saldo Anterior')


def _make_conceptos(conceptos, rnd_fn):
    def make_concepto(concepto):
        impuestos = concepto.get("Impuestos") or {}
        trasladados = [x if isinstance(x, dict) else Traslado.parse(x) for x in iterate(impuestos.get("Traslados"))]
        retenciones = [x if isinstance(x, dict) else Retencion.parse(x) for x in iterate(impuestos.get("Retenciones"))]

        if concepto.get('_traslados_incluidos'):
            s_tasa = sum(c["TasaOCuota"] for c in trasladados if c["TipoFactor"] == "Tasa")
            s_cuota = sum(c["TasaOCuota"] for c in trasladados if c["TipoFactor"] == "Cuota")
            if any(c for c in trasladados if c["TipoFactor"] in ('Tasa', 'Cuota') and (c.get('Base') is not None or c.get('Importe') is not None)):
                raise ValueError("Not possible to compute '_traslados_incluidos' if any 'trasladados' contains 'Base' or 'Importe'")

            valor_unitario = concepto['ValorUnitario']
            valor_unitario = (valor_unitario - s_cuota) / (s_tasa + 1)
            concepto['ValorUnitario'] = rnd_fn(valor_unitario)
        else:
            valor_unitario = concepto['ValorUnitario']

        importe = concepto["Cantidad"] * valor_unitario
        concepto["Importe"] = rnd_fn(importe)

        if concepto.get("ObjetoImp") in ("01", "03"):
            concepto['Impuestos'] = None
        else:
            base = importe - (concepto.get("Descuento") or 0)
            impuestos = {
                imp_t: [
                    make_impuesto(i, base=base, rnd_fn=rnd_fn) for i in imp
                ]
                for imp_t, imp in [('Traslados', trasladados), ('Retenciones', retenciones)] if imp
            }
            concepto['Impuestos'] = impuestos or None
            concepto["ObjetoImp"] = "02" if impuestos else "01"

        return concepto

    return [make_concepto(c) for c in iterate(conceptos)]


# MAIN #
class Comprobante(CFDI):
    """
    Estándar de Comprobante Fiscal Digital por Internet.

    :param emisor: Nodo requerido para expresar la información del contribuyente emisor del comprobante.
    :param lugar_expedicion: Atributo requerido para incorporar el código postal del lugar de expedición del comprobante (domicilio de la matriz o de la sucursal).
    :param receptor: Nodo requerido para precisar la información del contribuyente receptor del comprobante.
    :param conceptos: Nodo requerido para listar los conceptos cubiertos por el comprobante.
    :param moneda: Atributo requerido para identificar la clave de la moneda utilizada para expresar los montos, cuando se usa moneda nacional se registra MXN. Conforme con la especificación ISO 4217.
    :param tipo_de_comprobante: Atributo requerido para expresar la clave del efecto del comprobante fiscal para el contribuyente emisor.
    :param exportacion: Atributo requerido para expresar si el comprobante ampara una operación de exportación.
    :param serie: Atributo opcional para precisar la serie para control interno del contribuyente. Este atributo acepta una cadena de caracteres.
    :param folio: Atributo opcional para control interno del contribuyente que expresa el folio del comprobante, acepta una cadena de caracteres.
    :param forma_pago: Atributo condicional para expresar la clave de la forma de pago de los bienes o servicios amparados por el comprobante.
    :param condiciones_de_pago: Atributo condicional para expresar las condiciones comerciales aplicables para el pago del comprobante fiscal digital por Internet. Este atributo puede ser condicionado mediante atributos o complementos.
    :param tipo_cambio: Atributo condicional para representar el tipo de cambio FIX conforme con la moneda usada. Es requerido cuando la clave de moneda es distinta de MXN y de XXX. El valor debe reflejar el número de pesos mexicanos que equivalen a una unidad de la divisa señalada en el atributo moneda. Si el valor está fuera del porcentaje aplicable a la moneda tomado del catálogo c_Moneda, el emisor debe obtener del PAC que vaya a timbrar el CFDI, de manera no automática, una clave de confirmación para ratificar que el valor es correcto e integrar dicha clave en el atributo Confirmacion.
    :param metodo_pago: Atributo condicional para precisar la clave del método de pago que aplica para este comprobante fiscal digital por Internet, conforme al Artículo 29-A fracción VII incisos a y b del CFF.
    :param confirmacion: Atributo condicional para registrar la clave de confirmación que entregue el PAC para expedir el comprobante con importes grandes, con un tipo de cambio fuera del rango establecido o con ambos casos. Es requerido cuando se registra un tipo de cambio o un total fuera del rango establecido.
    :param informacion_global: Nodo condicional para precisar la información relacionada con el comprobante global.
    :param cfdi_relacionados: Nodo opcional para precisar la información de los comprobantes relacionados.
    :param complemento: Nodo opcional donde se incluye el complemento Timbre Fiscal Digital de manera obligatoria y los nodos complementarios determinados por el SAT, de acuerdo con las disposiciones particulares para un sector o actividad específica.
    :param addenda: Nodo opcional para recibir las extensiones al presente formato que sean de utilidad al contribuyente. Para las reglas de uso del mismo, referirse al formato origen.
    :param fecha: Atributo requerido para la expresión de la fecha y hora de expedición del Comprobante Fiscal Digital por Internet. Se expresa en la forma AAAA-MM-DDThh:mm:ss y debe corresponder con la hora local donde se expide el comprobante.
    """

    tag = '{http://www.sat.gob.mx/cfd/4}Comprobante'
    version = '4.0'
    complemento_pago = pago20.Pagos

    def __init__(
            self,
            emisor: Emisor | dict,
            lugar_expedicion: str,
            receptor: Receptor | dict,
            conceptos: Concepto | Sequence[Concepto | dict],
            moneda: str = "MXN",
            tipo_de_comprobante: str = "I",
            exportacion: str = "01",
            serie: str = None,
            folio: str = None,
            forma_pago: str = None,
            condiciones_de_pago: str = None,
            tipo_cambio: Decimal | int = None,
            metodo_pago: str = None,
            confirmacion: str = None,
            informacion_global: InformacionGlobal | dict = None,
            cfdi_relacionados: CfdiRelacionados | Sequence[CfdiRelacionados | dict] = None,
            complemento: CFDI | Sequence[CFDI] = None,
            addenda: CFDI | Sequence[CFDI] = None,
            fecha: datetime = None,
    ):
        super().__init__({
            'Version': self.version,
            'Fecha': fecha or datetime.now(tz=get_timezone(lugar_expedicion)).replace(tzinfo=None),
            'Sello': '',
            'SubTotal': None,
            'Moneda': moneda,
            'Total': None,
            'TipoDeComprobante': tipo_de_comprobante,
            'Exportacion': exportacion,
            'LugarExpedicion': lugar_expedicion,
            'Serie': serie,
            'Folio': folio,
            'FormaPago': forma_pago,
            'CondicionesDePago': condiciones_de_pago,
            'Descuento': None,
            'TipoCambio': tipo_cambio,
            'MetodoPago': metodo_pago,
            'Confirmacion': confirmacion,
            'InformacionGlobal': informacion_global,
            'CfdiRelacionados': cfdi_relacionados,
            'Emisor': emisor,
            'Receptor': receptor,
            'Conceptos': conceptos,
            'Impuestos': None,
            'Complemento': complemento,
            'Addenda': addenda,
            'NoCertificado': '',
            'Certificado': '',
        })
        self.compute()

    def compute(self):
        self["Conceptos"] = conceptos = _make_conceptos(self["Conceptos"], rnd_fn=rounder(self["Moneda"]))
        self["SubTotal"] = sub_total = sum(c['Importe'] for c in conceptos)
        descuento = sum(c.get('Descuento') or 0 for c in conceptos)
        self['Descuento'] = descuento or None
        self['Impuestos'] = impuestos = make_impuestos(conceptos)
        total = sub_total - descuento
        if impuestos:
            total += impuestos.get('TotalImpuestosTrasladados') or 0
            total -= impuestos.get('TotalImpuestosRetenidos') or 0
        self['Total'] = total

    @classmethod
    def pago(
            cls,
            emisor: Emisor | dict,
            lugar_expedicion: str,
            receptor: Receptor | dict,
            complemento_pago: CFDI,
            cfdi_relacionados: CfdiRelacionados | Sequence[CfdiRelacionados | dict] = None,
            confirmacion: str = None,
            serie: str = None,
            folio: str = None,
            addenda: CFDI | Sequence[CFDI] = None,
            fecha: datetime = None) -> 'Comprobante':
        """
        Estándar de Comprobante Fiscal Digital por Internet de Tipo Pago.

        :param emisor: Nodo requerido para expresar la información del contribuyente emisor del comprobante.
        :param lugar_expedicion: Atributo requerido para incorporar el código postal del lugar de expedición del comprobante (domicilio de la matriz o de la sucursal).
        :param receptor: Nodo requerido para precisar la información del contribuyente receptor del comprobante.
        :param complemento_pago: Pago
        :param serie: Atributo opcional para precisar la serie para control interno del contribuyente. Este atributo acepta una cadena de caracteres.
        :param folio: Atributo opcional para control interno del contribuyente que expresa el folio del comprobante, acepta una cadena de caracteres.
        :param confirmacion: Atributo condicional para registrar la clave de confirmación que entregue el PAC para expedir el comprobante con importes grandes, con un tipo de cambio fuera del rango establecido o con ambos casos. Es requerido cuando se registra un tipo de cambio o un total fuera del rango establecido.
        :param cfdi_relacionados: Nodo opcional para precisar la información de los comprobantes relacionados.
        :param addenda: Nodo opcional para recibir las extensiones al presente formato que sean de utilidad al contribuyente. Para las reglas de uso del mismo, referirse al formato origen.
        :param fecha: Atributo requerido para la expresión de la fecha y hora de expedición del Comprobante Fiscal Digital por Internet. Se expresa en la forma AAAA-MM-DDThh:mm:ss y debe corresponder con la hora local donde se expide el comprobante.
        :return: Comprobante
        """
        if cls.version == "3.3":
            receptor["UsoCFDI"] = "P01"
        else:
            receptor["UsoCFDI"] = "CP01"

        return cls(
            emisor=emisor,
            lugar_expedicion=lugar_expedicion,
            receptor=receptor,
            conceptos=Concepto(
                clave_prod_serv='84111506',
                cantidad=1,
                clave_unidad='ACT',
                descripcion='Pago',
                valor_unitario=Decimal(0),
                objeto_imp="01"
            ),
            complemento=complemento_pago,
            serie=serie,
            folio=folio,
            moneda='XXX',
            tipo_de_comprobante='P',
            cfdi_relacionados=cfdi_relacionados,
            confirmacion=confirmacion,
            exportacion="01",
            addenda=addenda,
            fecha=fecha
        )

    @classmethod
    def _pago_tipo_cambio(cls, moneda, tipo_cambio):
        # CRP204: El campo TipoCambioP no debe estar presente cuando el campo Moneda contenga ^MXN$ en el nodo Pago
        if cls.complemento_pago.version == "1.0":
            if moneda == 'MXN' and tipo_cambio == 1:
                tipo_cambio = None
        else:
            if moneda == 'MXN' and tipo_cambio is None:
                tipo_cambio = 1
        return tipo_cambio

    @classmethod
    def pago_comprobantes(
            cls,
            comprobantes: CFDI | PagoComprobante | Sequence[CFDI | PagoComprobante],
            fecha_pago: datetime,
            forma_pago: str,
            emisor: Emisor | dict = None,
            lugar_expedicion: str = None,
            receptor: Receptor | dict = None,
            tipo_cambio: Decimal | int = None,
            cfdi_relacionados: CfdiRelacionados | Sequence[CfdiRelacionados | dict] = None,
            confirmacion: str = None,
            serie: str = None,
            folio: str = None,
            addenda: CFDI | Sequence[CFDI] = None,
            fecha: datetime = None) -> 'Comprobante':
        """
        Estándar de Comprobante Fiscal Digital por Internet de Tipo Pago. Generado a partir de una lista de Comprobantes
        Se asume que los comprobantes se pagan en su totalidad en una sola exhibición

        :param emisor: Nodo requerido para expresar la información del contribuyente emisor del comprobante.
        :param lugar_expedicion: Atributo requerido para incorporar el código postal del lugar de expedición del comprobante (domicilio de la matriz o de la sucursal).
        :param receptor: Nodo requerido para precisar la información del contribuyente receptor del comprobante.
        :param comprobantes: CFDI(s) de Comprobante de Ingreso para generar el pago por su monto total o parcial usando PagoComprobante
        :param fecha_pago: Atributo requerido para expresar la fecha y hora en la que el beneficiario recibe el pago. Se expresa en la forma aaaa-mm-ddThh:mm:ss, de acuerdo con la especificación ISO 8601.En caso de no contar con la hora se debe registrar 12:00:00.
        :param serie: Atributo opcional para precisar la serie para control interno del contribuyente. Este atributo acepta una cadena de caracteres.
        :param folio: Atributo opcional para control interno del contribuyente que expresa el folio del comprobante, acepta una cadena de caracteres.
        :param forma_pago: Atributo condicional para expresar la clave de la forma de pago de los bienes o servicios amparados por el comprobante.
        :param tipo_cambio: Atributo condicional para representar el tipo de cambio FIX conforme con la moneda usada. Es requerido cuando la clave de moneda es distinta de MXN y de XXX. El valor debe reflejar el número de pesos mexicanos que equivalen a una unidad de la divisa señalada en el atributo moneda. Si el valor está fuera del porcentaje aplicable a la moneda tomado del catálogo c_Moneda, el emisor debe obtener del PAC que vaya a timbrar el CFDI, de manera no automática, una clave de confirmación para ratificar que el valor es correcto e integrar dicha clave en el atributo Confirmacion.
        :param confirmacion: Atributo condicional para registrar la clave de confirmación que entregue el PAC para expedir el comprobante con importes grandes, con un tipo de cambio fuera del rango establecido o con ambos casos. Es requerido cuando se registra un tipo de cambio o un total fuera del rango establecido.
        :param cfdi_relacionados: Nodo opcional para precisar la información de los comprobantes relacionados.
        :param addenda: Nodo opcional para recibir las extensiones al presente formato que sean de utilidad al contribuyente. Para las reglas de uso del mismo, referirse al formato origen.
        :param fecha: Atributo requerido para la expresión de la fecha y hora de expedición del Comprobante Fiscal Digital por Internet. Se expresa en la forma AAAA-MM-DDThh:mm:ss y debe corresponder con la hora local donde se expide el comprobante.
        :return: Comprobante
        """
        comprobantes = [c if isinstance(c, PagoComprobante) else PagoComprobante(comprobante=c) for c in iterate(comprobantes)]
        first_cfdi = comprobantes[0].comprobante
        moneda = first_cfdi['Moneda']

        emisor = emisor or first_cfdi['Emisor'].copy()
        lugar_expedicion = lugar_expedicion or first_cfdi['LugarExpedicion']
        receptor = receptor or first_cfdi['Receptor'].copy()

        tipo_cambio = cls._pago_tipo_cambio(moneda, tipo_cambio)

        if not all(
                c.comprobante["Moneda"] == moneda
                and c.comprobante["Emisor"]["Rfc"] == emisor["Rfc"]
                and c.comprobante["Emisor"]["RegimenFiscal"] == emisor["RegimenFiscal"]
                and c.comprobante["Receptor"]["Rfc"] == receptor["Rfc"]
                and c.comprobante["Receptor"].get("RegimenFiscalReceptor") == receptor.get("RegimenFiscalReceptor")
                for c in comprobantes
        ):
            raise ValueError("CFDIS are of different RFC's Emisor/Receptor o Moneda")

        return cls.pago(
            emisor=emisor,
            lugar_expedicion=lugar_expedicion,
            receptor=receptor,
            complemento_pago=cls.complemento_pago(
                pago=[{
                    'DoctoRelacionado': [
                        {
                            'IdDocumento': c.comprobante["Complemento"]["TimbreFiscalDigital"]["UUID"],
                            'Serie': c.comprobante.get("Serie"),
                            'Folio': c.comprobante.get("Folio"),
                            'MonedaDR': c.comprobante["Moneda"],
                            'EquivalenciaDR': 1,
                            'MetodoDePagoDR': c.comprobante["MetodoPago"],
                            'NumParcialidad': c.num_parcialidad,
                            'ImpSaldoAnt': c.imp_saldo_ant,
                            'ImpPagado': c.imp_pagado,
                            'ObjetoImpDR': '02' if 'Impuestos' in c.comprobante else '01',
                            'ImpuestosDR': make_impuestos_dr_parcial(
                                conceptos=c.comprobante['Conceptos'],
                                imp_saldo_ant=c.imp_saldo_ant,
                                imp_pagado=c.imp_pagado,
                                total=c.comprobante["Total"],
                                rnd_fn=rounder(c.comprobante["Moneda"])
                            ) if 'Impuestos' in c.comprobante else None
                        } for c in comprobantes
                    ],
                    'FechaPago': fecha_pago,
                    'FormaDePagoP': forma_pago,
                    'MonedaP': moneda,
                    'TipoCambioP': tipo_cambio
                }]
            ),
            cfdi_relacionados=cfdi_relacionados,
            confirmacion=confirmacion,
            serie=serie,
            folio=folio,
            addenda=addenda,
            fecha=fecha
        )

    @classmethod
    def nomina(
            cls,
            emisor: Emisor | dict,
            lugar_expedicion: str,
            receptor: Receptor | dict,
            complemento_nomina: CFDI,
            cfdi_relacionados: CfdiRelacionados | Sequence[CfdiRelacionados | dict] = None,
            confirmacion: str = None,
            serie: str = None,
            folio: str = None,
            addenda: CFDI | Sequence[CFDI] = None,
            fecha: datetime = None) -> 'Comprobante':
        """
        Estándar de Comprobante Fiscal Digital por Internet de Tipo Pago.

        :param emisor: Nodo requerido para expresar la información del contribuyente emisor del comprobante.
        :param lugar_expedicion: Atributo requerido para incorporar el código postal del lugar de expedición del comprobante (domicilio de la matriz o de la sucursal).
        :param receptor: Nodo requerido para precisar la información del contribuyente receptor del comprobante.
        :param complemento_nomina: Pago
        :param serie: Atributo opcional para precisar la serie para control interno del contribuyente. Este atributo acepta una cadena de caracteres.
        :param folio: Atributo opcional para control interno del contribuyente que expresa el folio del comprobante, acepta una cadena de caracteres.
        :param confirmacion: Atributo condicional para registrar la clave de confirmación que entregue el PAC para expedir el comprobante con importes grandes, con un tipo de cambio fuera del rango establecido o con ambos casos. Es requerido cuando se registra un tipo de cambio o un total fuera del rango establecido.
        :param cfdi_relacionados: Nodo opcional para precisar la información de los comprobantes relacionados.
        :param addenda: Nodo opcional para recibir las extensiones al presente formato que sean de utilidad al contribuyente. Para las reglas de uso del mismo, referirse al formato origen.
        :param fecha: Atributo requerido para la expresión de la fecha y hora de expedición del Comprobante Fiscal Digital por Internet. Se expresa en la forma AAAA-MM-DDThh:mm:ss y debe corresponder con la hora local donde se expide el comprobante.
        :return: Comprobante
        """
        if cls.version == "3.3":
            receptor["UsoCFDI"] = "P01"
        else:
            receptor["UsoCFDI"] = "CN01"

        valor_unitario = (
            complemento_nomina.get('TotalPercepciones') or Decimal(0)
        ) + (
            complemento_nomina.get('TotalOtrosPagos') or Decimal(0)
        )
        
        concepto = Concepto(
            clave_prod_serv='84111505',
            cantidad=1,
            clave_unidad='ACT',
            descripcion='Pago de nómina',
            valor_unitario=valor_unitario,
            descuento=complemento_nomina.get('TotalDeducciones'),
            objeto_imp="03"
        )
        
        return cls(
            emisor=emisor,
            lugar_expedicion=lugar_expedicion,
            receptor=receptor,
            conceptos=concepto,
            complemento=complemento_nomina,
            serie=serie,
            folio=folio,
            moneda='MXN',
            tipo_de_comprobante='N',
            metodo_pago="PUE",
            forma_pago="99",
            cfdi_relacionados=cfdi_relacionados,
            confirmacion=confirmacion,
            exportacion="01",
            addenda=addenda,
            fecha=fecha,
        )
