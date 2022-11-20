import logging

from .models import Payment, PaymentsDetails, SatCFDI

logger = logging.getLogger(__name__)


def format_head(cfdi):
    return str(cfdi["TipoDeComprobante"]) + " " + cfdi["Version"] + "\n" + \
           str(cfdi.uuid) + "\n- " + cfdi.name


def format_head_pre(cfdi):
    return str(cfdi["TipoDeComprobante"]) + " " + cfdi["Version"] + "\n" + \
           "*" + cfdi["Serie"] + cfdi["Folio"]


def format_fecha(cfdi):
    return str(cfdi["Fecha"]) + "\n" + cfdi["LugarExpedicion"].code + "\n" + str(cfdi["Receptor"]["UsoCFDI"])


def format_emisor(cfdi):
    emisor = cfdi["Emisor"]
    return emisor["Nombre"] + "\n" + emisor["Rfc"] + "\n" + str(emisor["RegimenFiscal"])


def format_receptor(cfdi):
    receptor = cfdi["Receptor"]
    return receptor.get("Nombre", "") + "\n" + receptor["Rfc"] + " - " + receptor.get("DomicilioFiscalReceptor", "") + "\n" + str(receptor.get("RegimenFiscalReceptor", ""))


def format_forma_pago(cfdi):
    return str(cfdi.get("FormaPago")) + "\n" + \
           str(cfdi.get("MetodoPago")) + "\n" + \
           str(cfdi["Moneda"])


def format_forma_pago_dr(payment: Payment):
    if payment.pago is None:
        return format_forma_pago(payment.comprobante)

    return str(payment.pago["FormaDePagoP"]) + "\n" + \
           str(payment.docto_relacionado.get("MetodoDePagoDR")) + "\n" + \
           str(payment.docto_relacionado["MonedaDR"])


def format_fecha_pago(payment: PaymentsDetails):
    if payment.pago:
        return payment.pago["FechaPago"]

    def_pagado = payment.comprobante.saldo_pendiente == 0
    if def_pagado:
        return payment.comprobante["Fecha"]
    else:
        return "Pendiente"


def format_estado_cfdi(cfdi: SatCFDI):
    estatus = cfdi.consulta_estado()
    if not estatus:
        return ""

    return (
            (estatus["Estado"] or "") + "\n" +
            (estatus["EsCancelable"] or "") + "\n" +
            (estatus["EstatusCancelacion"] or "")
    )


def format_pagos(cfdi: SatCFDI):
    if cfdi["TipoDeComprobante"] == "P":
        for pago in cfdi["Complemento"]["Pagos"]["Pago"]:
            response = ""
            for doc_rel in pago.get("DoctoRelacionado", []):
                response += doc_rel["IdDocumento"] + '\n' + \
                            '- ' + doc_rel.get("Serie", "") + doc_rel.get("Folio", "") + '\n'
            return response[:-1]

    if cfdi["TipoDeComprobante"] == "I":
        payment_complements = cfdi.payments
        if payment_complements:
            response = ""
            for p in payment_complements:
                response += str(p.comprobante.uuid) + '\n' + \
                            '- ' + p.comprobante.name + '\n'
            return response[:-1]


def format_relaciones(cfdi: SatCFDI):
    response = ""
    rel = cfdi.get("CfdiRelacionados")
    if rel:
        response += str(rel["TipoRelacion"]) + '\n'
        for uuid in rel["CfdiRelacionado"]:
            response += str(uuid) + '\n'

    for c in cfdi.relations:
        response += str(c.cfdi_relacionados["TipoRelacion"]) + '\n' + \
                    str(c.comprobante.uuid) + '\n' + \
                    "- " + c.comprobante.name + '\n'
    return response[:-1]


def format_conceptos(cfdi):
    return "\n".join([str(c["ClaveProdServ"]) + "\n- " + c['Descripcion'] for c in cfdi["Conceptos"]])
