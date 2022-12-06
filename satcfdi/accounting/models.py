from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .. import CFDI, XElement, CFDIError
from ..create.compute import make_impuestos_dr_parcial, rounder, group_impuestos, encode_impuesto, calculate_partial
from ..pacs.sat import SAT
from ..transform.helpers import fmt_decimal, strcode

PPD = "PPD"
PUE = "PUE"

sat = SAT()


class SatCFDI(CFDI):
    relations = None  # type: list[Relation]
    payments = None  # type: list[Payment]
    """
    SatCFDI is an extension of a CFDI to represent a CFDI that has been sent to SAT
    """

    @property
    def uuid(self):
        return UUID(self["Complemento"]["TimbreFiscalDigital"]["UUID"])

    @property
    def name(self):
        return self.get("Serie", "") + self.get("Folio", "")

    @property
    def saldo_pendiente(self) -> Decimal:
        if self["TipoDeComprobante"] == "I":
            # Nota de crédito de los documentos relacionados
            credit_notes = sum(
                c.comprobante["Total"]
                for c in self.relations
                if c.cfdi_relacionados["TipoRelacion"] == "01" and c.comprobante['TipoDeComprobante'] == "E" and c.comprobante.estatus != '0'
            )
            insoluto = min(
                (c.docto_relacionado['ImpSaldoInsoluto']
                 for c in self.payments
                 if c.comprobante.estatus != '0'),
                default=None
            )
            if insoluto is not None:
                return insoluto - credit_notes

            insoluto = self["Total"] - credit_notes
            if self["MetodoPago"] == PPD:
                return insoluto
            if self["MetodoPago"] == PUE:
                return Decimal(0)

        return None

    @property
    def ultima_num_parcialidad(self) -> int:
        return max((c.docto_relacionado['NumParcialidad'] for c in self.payments), default=0)

    def consulta_estado(self):
        raise NotImplementedError()

    @property
    def metadata(self) -> str:
        match self.tag:
            case '{http://www.sat.gob.mx/cfd/3}Comprobante' | '{http://www.sat.gob.mx/cfd/4}Comprobante':
                # Uuid~RfcEmisor~NombreEmisor~RfcReceptor~NombreReceptor~RfcPac~FechaEmision~FechaCertificacionSat~Monto~EfectoComprobante~Estatus~FechaCancelacion
                return "{uuid}~{rfc_emisor}~{nombre_emisor}~{rfc_receptor}~{nombre_receptor}~{rfc_pac}~{fecha_emision}~{fecha_certificacion_sat}~{monto}~{efecto_comprobante}~{estatus}~{fecha_cancelacion}".format(
                    uuid=self["Complemento"]["TimbreFiscalDigital"]["UUID"],
                    rfc_emisor=self['Emisor']["Rfc"],
                    nombre_emisor=self['Emisor']['Nombre'],
                    rfc_receptor=self['Receptor']['Rfc'],
                    nombre_receptor=self['Receptor'].get('Nombre', ''),
                    rfc_pac=self["Complemento"]["TimbreFiscalDigital"]["RfcProvCertif"],
                    fecha_emision=self["Fecha"],
                    fecha_certificacion_sat=self["Complemento"]["TimbreFiscalDigital"]["FechaTimbrado"],
                    monto=fmt_decimal(self["Total"]),
                    efecto_comprobante=strcode(self["TipoDeComprobante"]),
                    estatus=self.estatus,
                    fecha_cancelacion=self.fecha_cancelacion or ''
                )

            case '{http://www.sat.gob.mx/esquemas/retencionpago/1}Retenciones':
                # Uuid~RfcEmisor~NombreEmisor~RfcReceptor~NombreReceptor~RfcPac~FechaEmision~FechaCertificacionSat~MontoOp~MontoRet~Estatus~FechaCancelacion
                cert_sat = sat.recover_certificate(
                    no_certificado=self["Complemento"]["TimbreFiscalDigital"]["NoCertificadoSAT"]
                )
                return "{uuid}~{rfc_emisor}~{nombre_emisor}~{rfc_receptor}~{nombre_receptor}~{rfc_pac}~{fecha_emision}~{fecha_certificacion_sat}~{monto_op}~{monto_ret}~{estatus}~{fecha_cancelacion}".format(
                    uuid=self["Complemento"]["TimbreFiscalDigital"]["UUID"],
                    rfc_emisor=self["Emisor"]["RFCEmisor"],
                    nombre_emisor=self['Emisor']['NomDenRazSocE'],
                    rfc_receptor=self['Receptor']['Nacional']['RFCRecep'],
                    nombre_receptor=self['Receptor']['Nacional']['NomDenRazSocR'],
                    rfc_pac=cert_sat.rfc_pac,
                    fecha_emision=self["FechaExp"],
                    fecha_certificacion_sat=self["Complemento"]["TimbreFiscalDigital"]["FechaTimbrado"],
                    monto_op=fmt_decimal(self["Totales"]["MontoTotOperacion"]),
                    monto_ret=fmt_decimal(self["Totales"]["MontoTotRet"]),
                    estatus=self.estatus,
                    fecha_cancelacion=self.fecha_cancelacion or ''
                )

            case '{http://www.sat.gob.mx/esquemas/retencionpago/2}Retenciones':
                # Uuid~RfcEmisor~NombreEmisor~RfcReceptor~NombreReceptor~RfcPac~FechaEmision~FechaCertificacionSat~MontoOp~MontoRet~Estatus~FechaCancelacion
                return "{uuid}~{rfc_emisor}~{nombre_emisor}~{rfc_receptor}~{nombre_receptor}~{rfc_pac}~{fecha_emision}~{fecha_certificacion_sat}~{monto_op}~{monto_ret}~{estatus}~{fecha_cancelacion}".format(
                    uuid=self["Complemento"]["TimbreFiscalDigital"]["UUID"],
                    rfc_emisor=self["Emisor"]["RfcE"],
                    nombre_emisor=self['Emisor']['NomDenRazSocE'],
                    rfc_receptor=self['Receptor']['Nacional']['RfcR'],
                    nombre_receptor=self['Receptor']['Nacional']['NomDenRazSocR'],
                    rfc_pac=self["Complemento"]["TimbreFiscalDigital"]["RfcProvCertif"],
                    fecha_emision=self["FechaExp"],
                    fecha_certificacion_sat=self["Complemento"]["TimbreFiscalDigital"]["FechaTimbrado"],
                    monto_op=fmt_decimal(self["Totales"]["MontoTotOperacion"]),
                    monto_ret=fmt_decimal(self["Totales"]["MontoTotRet"]),
                    estatus=self.estatus,
                    fecha_cancelacion=self.fecha_cancelacion or ''
                )
            case _:
                raise CFDIError("No metadata")

    @property
    def estatus(self) -> str:
        """
        '0' = 'Cancelado'
        '1' = 'Vigente'
        :return:
        """
        raise NotImplementedError()

    @property
    def fecha_cancelacion(self) -> datetime | None:
        raise NotImplementedError()


@dataclass(slots=True, init=True)
class Relation:
    cfdi_relacionados: XElement
    comprobante: SatCFDI


@dataclass(slots=True, init=True)
class Payment:
    comprobante: SatCFDI
    pago: XElement = None
    docto_relacionado: XElement = None


@dataclass
class PaymentsDetails(Payment):
    comprobante_pagado: SatCFDI = None

    def __post_init__(self):
        if self.pago:
            self.impuestos = self.docto_relacionado.get('ImpuestosDR')
            if self.impuestos is None:
                self.impuestos = make_impuestos_dr_parcial(
                    conceptos=self.comprobante_pagado['Conceptos'],
                    imp_saldo_ant=self.docto_relacionado['ImpSaldoAnt'],
                    imp_pagado=self.docto_relacionado['ImpPagado'],
                    total=self.comprobante_pagado['Total'],
                    rnd_fn=rounder(self.comprobante_pagado['Moneda'])
                )

            self.impuestos = group_impuestos([{
                "ImpuestosDR": self.impuestos
            }], pfx="DR", ofx="")

            for imp in ('Traslados', 'Retenciones'):
                if imps := self.impuestos.get(imp):
                    self.impuestos[imp] = {
                        encode_impuesto(
                            impuesto=v['Impuesto'],
                            tipo_factor=v.get("TipoFactor"),
                            tasa_cuota=v.get('TasaOCuota')
                        ): v
                        for v in imps
                    }

            def calc_parcial(field):
                return calculate_partial(
                    value=self.comprobante_pagado.get(field),
                    imp_saldo_ant=self.docto_relacionado['ImpSaldoAnt'],
                    imp_pagado=self.docto_relacionado["ImpPagado"],
                    total=self.comprobante_pagado["Total"],
                    rnd_fn=rounder(self.comprobante_pagado['Moneda'])
                )

            self.sub_total = calc_parcial("SubTotal")
            self.descuento = calc_parcial("Descuento")

        else:
            self.impuestos = self.comprobante.get("Impuestos", {})
            self.sub_total = self.comprobante["SubTotal"]
            self.descuento = self.comprobante.get("Descuento")
