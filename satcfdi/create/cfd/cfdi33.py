from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import *

from . import cfdi40, pago10
from .. import Issuer
from ... import CFDI, XElement, ScalarMap

_a = Issuer


class Impuesto(cfdi40.Impuesto):
    """
    http://www.sat.gob.mx/cfd/4
    Nodo requerido para la información detallada de un traslado de impuesto específico.
    """


class CfdiRelacionados(ScalarMap):
    """
    http://www.sat.gob.mx/cfd/3
    Nodo opcional para precisar la información de los comprobantes relacionados.
    """

    def __init__(
            self,
            tipo_relacion: str,
            cfdi_relacionado: str | Sequence[str],
    ):
        """
        Nodo opcional para precisar la información de los comprobantes relacionados.

        :param tipo_relacion: Atributo requerido para indicar la clave de la relación que existe entre éste que se esta generando y el o los CFDI previos.
        :param cfdi_relacionado: Nodo requerido para precisar la información de los comprobantes relacionados.
        """

        super().__init__({
            'TipoRelacion': tipo_relacion,
            'CfdiRelacionado': cfdi_relacionado,
        })


class Parte(ScalarMap):
    """
    http://www.sat.gob.mx/cfd/3
    Nodo opcional para expresar las partes o componentes que integran la totalidad del concepto expresado en el comprobante fiscal digital por Internet.
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


class Concepto(ScalarMap):
    """
    http://www.sat.gob.mx/cfd/3
    Nodo requerido para registrar la información detallada de un bien o servicio amparado en el comprobante.
    """

    def __init__(
            self,
            clave_prod_serv: str,
            cantidad: Decimal | int,
            clave_unidad: str,
            descripcion: str,
            valor_unitario: Decimal | int,
            no_identificacion: str = None,
            unidad: str = None,
            descuento: Decimal | int = None,
            informacion_aduanera: str | Sequence[str] = None,
            cuenta_predial: str = None,
            complemento_concepto: Sequence[CFDI] = None,
            parte: Sequence[Parte | dict] = None,
            traslados: Impuesto | str | Sequence[Impuesto | str | dict] = None,
            retenciones: Impuesto | str | Sequence[Impuesto | str | dict] = None,
            _traslados_incluidos: bool = False
    ):
        """
        Nodo requerido para registrar la información detallada de un bien o servicio amparado en el comprobante.
        
        :param clave_prod_serv: Atributo requerido para expresar la clave del producto o del servicio amparado por el presente concepto. Es requerido y deben utilizar las claves del catálogo de productos y servicios, cuando los conceptos que registren por sus actividades correspondan con dichos conceptos.
        :param cantidad: Atributo requerido para precisar la cantidad de bienes o servicios del tipo particular definido por el presente concepto.
        :param clave_unidad: Atributo requerido para precisar la clave de unidad de medida estandarizada aplicable para la cantidad expresada en el concepto. La unidad debe corresponder con la descripción del concepto.
        :param descripcion: Atributo requerido para precisar la descripción del bien o servicio cubierto por el presente concepto.
        :param valor_unitario: Atributo requerido para precisar el valor o precio unitario del bien o servicio cubierto por el presente concepto.
        :param no_identificacion: Atributo opcional para expresar el número de parte, identificador del producto o del servicio, la clave de producto o servicio, SKU o equivalente, propia de la operación del emisor, amparado por el presente concepto. Opcionalmente se puede utilizar claves del estándar GTIN.
        :param unidad: Atributo opcional para precisar la unidad de medida propia de la operación del emisor, aplicable para la cantidad expresada en el concepto. La unidad debe corresponder con la descripción del concepto.
        :param descuento: Atributo opcional para representar el importe de los descuentos aplicables al concepto. No se permiten valores negativos.
        :param informacion_aduanera: Nodo opcional para introducir la información aduanera aplicable cuando se trate de ventas de primera mano de mercancías importadas o se trate de operaciones de comercio exterior con bienes o servicios.
        :param cuenta_predial: Nodo opcional para asentar el número de cuenta predial con el que fue registrado el inmueble, en el sistema catastral de la entidad federativa de que trate, o bien para incorporar los datos de identificación del certificado de participación inmobiliaria no amortizable.
        :param complemento_concepto: Nodo opcional donde se incluyen los nodos complementarios de extensión al concepto definidos por el SAT, de acuerdo con las disposiciones particulares para un sector o actividad específica.
        :param parte: Nodo opcional para expresar las partes o componentes que integran la totalidad del concepto expresado en el comprobante fiscal digital por Internet.
        :param traslados: Traslados a aplicar.
        :param retenciones: Retenciones a aplicar.
        :param _traslados_incluidos: si el valor valor_unitario ya incluye traslados.
        """

        super().__init__({
            'ClaveProdServ': clave_prod_serv,
            'Cantidad': cantidad,
            'ClaveUnidad': clave_unidad,
            'Descripcion': descripcion,
            'ValorUnitario': valor_unitario,
            'NoIdentificacion': no_identificacion,
            'Unidad': unidad,
            'Descuento': descuento,
            'InformacionAduanera': informacion_aduanera,
            'CuentaPredial': cuenta_predial,
            'ComplementoConcepto': complemento_concepto,
            'Parte': parte,
            'Impuestos': {
                'Traslados': traslados,
                'Retenciones': retenciones
            },
            '_traslados_incluidos': _traslados_incluidos
        })


class Receptor(ScalarMap):
    """
    http://www.sat.gob.mx/cfd/3
    Nodo requerido para precisar la información del contribuyente receptor del comprobante.
    """

    def __init__(
            self,
            rfc: str,
            uso_cfdi: str,
            nombre: str = None,
            residencia_fiscal: str = None,
            num_reg_id_trib: str = None,
    ):
        """
        Nodo requerido para precisar la información del contribuyente receptor del comprobante.
        
        :param rfc: Atributo requerido para precisar la Clave del Registro Federal de Contribuyentes correspondiente al contribuyente receptor del comprobante.
        :param uso_cfdi: Atributo requerido para expresar la clave del uso que dará a esta factura el receptor del CFDI.
        :param nombre: Atributo opcional para precisar el nombre, denominación o razón social del contribuyente receptor del comprobante.
        :param residencia_fiscal: Atributo condicional para registrar la clave del país de residencia para efectos fiscales del receptor del comprobante, cuando se trate de un extranjero, y que es conforme con la especificación ISO 3166-1 alpha-3. Es requerido cuando se incluya el complemento de comercio exterior o se registre el atributo NumRegIdTrib.
        :param num_reg_id_trib: Atributo condicional para expresar el número de registro de identidad fiscal del receptor cuando sea residente en el extranjero. Es requerido cuando se incluya el complemento de comercio exterior.
        """

        super().__init__({
            'Rfc': rfc,
            'UsoCFDI': uso_cfdi,
            'Nombre': nombre,
            'ResidenciaFiscal': residencia_fiscal,
            'NumRegIdTrib': num_reg_id_trib,
        })


class Comprobante(cfdi40.Comprobante):
    """
    Estándar de Comprobante Fiscal Digital por Internet.
    """
    tag = '{http://www.sat.gob.mx/cfd/3}Comprobante'
    version = '3.3'
    complemento_pago = pago10.Pagos
