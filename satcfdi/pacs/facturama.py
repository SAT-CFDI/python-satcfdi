"""
Facturama Multiemisor PAC adapter.

Facturama seals and stamps from a JSON payload (CSD must already be uploaded).
Pre-signed XML stamp is not supported by their public Multiemisor API.

Supported TipoDeComprobante: I, E, T, P (Pagos 2.0), N (Nómina 1.2).

Docs: https://apisandbox.facturama.mx/guias
"""
from __future__ import annotations

import base64
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from . import (
    PAC,
    Accept,
    CancelReason,
    CancelationAcknowledgment,
    Document,
    Environment,
)
from .. import __version__
from ..cfdi import CFDI
from ..exceptions import DocumentNotFoundError, ResponseError
from ..models import Signer
from ..utils import iterate

_TAX_NAME = {
    "001": "ISR",
    "002": "IVA",
    "003": "IEPS",
}

_ITEM_TIPOS = {"I", "E", "T"}
_SUPPORTED_TIPOS = _ITEM_TIPOS | {"P", "N"}


def _enum_value(val):
    if isinstance(val, Enum):
        return val.value
    return val


def _num(val) -> float | None:
    if val is None:
        return None
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, (int, float)):
        return float(val)
    return float(Decimal(str(val)))


def _format_date(fecha, *, date_only: bool = False) -> str | None:
    if fecha is None:
        return None
    if isinstance(fecha, datetime):
        if date_only:
            return fecha.strftime("%Y-%m-%d")
        return fecha.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(fecha, date):
        return fecha.strftime("%Y-%m-%d")
    text = str(fecha)
    if date_only:
        return text[:10]
    if "T" in text:
        return text.replace("T", " ")[:19]
    return text


def _as_bool(val) -> bool | None:
    if val is None:
        return None
    if isinstance(val, bool):
        return val
    text = str(_enum_value(val)).strip().lower()
    if text in {"si", "sí", "yes", "true", "1"}:
        return True
    if text in {"no", "false", "0"}:
        return False
    return bool(val)


def _tax_entry(
    tax: dict,
    *,
    is_retention: bool,
    base_key="Base",
    impuesto_key="Impuesto",
    tipo_factor_key="TipoFactor",
    tasa_key="TasaOCuota",
    importe_key="Importe",
) -> dict:
    impuesto = str(_enum_value(tax.get(impuesto_key)))
    name = _TAX_NAME.get(impuesto)
    if not name:
        raise NotImplementedError(f"Unsupported tax code: {impuesto}")

    tipo_factor = str(_enum_value(tax.get(tipo_factor_key) or ""))
    entry = {
        "Name": name,
        "IsRetention": is_retention,
        "Base": _num(tax.get(base_key)),
        "Total": _num(tax.get(importe_key)) or 0.0,
    }
    if tipo_factor.lower() == "exento":
        entry["Rate"] = 0.0
        entry["IsQuota"] = False
    else:
        rate = tax.get(tasa_key)
        entry["Rate"] = _num(rate) if rate is not None else 0.0
        entry["IsQuota"] = tipo_factor.lower() == "cuota"
    return entry


def _complement_node(cfdi: CFDI, name: str):
    """
    Return a complement node whether Complemento is a dict of complements
    (after XML parse) or the complement CFDI itself (after create()).
    """
    complemento = cfdi.get("Complemento")
    if not complemento:
        return None
    if name in complemento:
        node = complemento[name]
        # Avoid treating Pagos body keys as a nested "Pago" complement name clash
        if node is not None and not (
            name == "Pago" and isinstance(node, list) and "Version" in complemento
        ):
            return node
    tag = getattr(complemento, "tag", "") or ""
    if name == "Pagos" and (
        "Pagos" in tag
        or ("Pago" in complemento and "Version" in complemento)
    ):
        return complemento
    if name == "Nomina" and (
        "nomina" in tag.lower()
        or "TipoNomina" in complemento
    ):
        return complemento
    return None


def _uuid_from_relacionado(uuid_node) -> str:
    if isinstance(uuid_node, str):
        return uuid_node
    return str(uuid_node["UUID"])


def _map_relations(cfdi: CFDI) -> dict | None:
    relacionados = cfdi.get("CfdiRelacionados")
    if not relacionados:
        return None
    groups = list(iterate(relacionados))
    if not groups:
        return None
    tipo = str(_enum_value(groups[0]["TipoRelacion"]))
    uuids = []
    for group in groups:
        group_tipo = str(_enum_value(group["TipoRelacion"]))
        if group_tipo != tipo:
            raise NotImplementedError(
                "Facturama Relations supports a single TipoRelacion; "
                f"got both {tipo!r} and {group_tipo!r}"
            )
        for uuid_node in iterate(group.get("CfdiRelacionado")):
            uuids.append({"Uuid": _uuid_from_relacionado(uuid_node)})
    return {"Type": tipo, "Cfdis": uuids}


def _map_items(cfdi: CFDI) -> list[dict]:
    items = []
    for concepto in iterate(cfdi["Conceptos"]):
        item: dict[str, Any] = {
            "ProductCode": str(concepto["ClaveProdServ"]),
            "Description": str(concepto["Descripcion"]),
            "UnitCode": str(concepto["ClaveUnidad"]),
            "Quantity": _num(concepto["Cantidad"]),
            "UnitPrice": _num(concepto["ValorUnitario"]),
            "Subtotal": _num(concepto["Importe"]),
            "TaxObject": str(_enum_value(concepto.get("ObjetoImp") or "01")),
        }
        if no_id := concepto.get("NoIdentificacion"):
            item["IdentificationNumber"] = str(no_id)
        if unidad := concepto.get("Unidad"):
            item["Unit"] = str(unidad)
        if desc := concepto.get("Descuento"):
            item["Discount"] = _num(desc)

        if terceros := concepto.get("ACuentaTerceros"):
            item["ThirdPartyAccount"] = {
                "Rfc": terceros["RfcACuentaTerceros"],
                "Name": terceros["NombreACuentaTerceros"],
                "FiscalRegime": str(_enum_value(terceros["RegimenFiscalACuentaTerceros"])),
                "TaxZipCode": str(terceros["DomicilioFiscalACuentaTerceros"]),
            }

        taxes = []
        impuestos = concepto.get("Impuestos") or {}
        for traslado in iterate(impuestos.get("Traslados")):
            taxes.append(_tax_entry(traslado, is_retention=False))
        for retencion in iterate(impuestos.get("Retenciones")):
            taxes.append(_tax_entry(retencion, is_retention=True))
        if taxes:
            item["Taxes"] = taxes

        line_total = _num(concepto["Importe"]) or 0.0
        if desc := item.get("Discount"):
            line_total -= desc
        for tax in taxes:
            if tax["IsRetention"]:
                line_total -= tax["Total"] or 0.0
            else:
                line_total += tax["Total"] or 0.0
        item["Total"] = line_total
        items.append(item)
    return items


def _map_payments(pagos) -> list[dict]:
    payments = []
    for pago in iterate(pagos.get("Pago")):
        payment: dict[str, Any] = {
            "Date": _format_date(pago["FechaPago"]),
            "PaymentForm": str(_enum_value(pago["FormaDePagoP"])),
            "Amount": _num(pago["Monto"]),
        }
        if moneda := pago.get("MonedaP"):
            payment["Currency"] = str(_enum_value(moneda))
        if tipo_cambio := pago.get("TipoCambioP"):
            payment["ExchangeRate"] = _num(tipo_cambio)
        if num_op := pago.get("NumOperacion"):
            payment["OperationNumber"] = str(num_op)
        if rfc_ord := pago.get("RfcEmisorCtaOrd"):
            payment["AccountOrderRfc"] = str(rfc_ord)
        if banco := pago.get("NomBancoOrdExt"):
            payment["AccountOrderBankName"] = str(banco)
        if cta_ord := pago.get("CtaOrdenante"):
            payment["AccountOrderNumber"] = str(cta_ord)
        if rfc_ben := pago.get("RfcEmisorCtaBen"):
            payment["AccountBeneficiaryRfc"] = str(rfc_ben)
        if cta_ben := pago.get("CtaBeneficiario"):
            payment["AccountBeneficiaryNumber"] = str(cta_ben)

        related = []
        for docto in iterate(pago.get("DoctoRelacionado")):
            doc: dict[str, Any] = {
                "Uuid": str(docto["IdDocumento"]),
                "PaymentMethod": str(
                    _enum_value(
                        docto.get("MetodoDePagoDR")
                        or docto.get("MetodoPagoDR")
                        or "PPD"
                    )
                ),
                "PartialityNumber": str(docto["NumParcialidad"]),
                "PreviousBalanceAmount": _num(docto["ImpSaldoAnt"]),
                "AmountPaid": _num(docto["ImpPagado"]),
                "ImpSaldoInsoluto": _num(
                    docto.get("ImpSaldoInsoluto")
                    if docto.get("ImpSaldoInsoluto") is not None
                    else (docto["ImpSaldoAnt"] - docto["ImpPagado"])
                ),
                "TaxObject": str(_enum_value(docto.get("ObjetoImpDR") or "01")),
            }
            if serie := docto.get("Serie"):
                doc["Serie"] = str(serie)
            if folio := docto.get("Folio"):
                doc["Folio"] = str(folio)
            if moneda := docto.get("MonedaDR"):
                doc["Currency"] = str(_enum_value(moneda))
            if equiv := docto.get("EquivalenciaDR"):
                doc["EquivalenceDocRel"] = _num(equiv)

            taxes = []
            impuestos = docto.get("ImpuestosDR") or {}
            for traslado in iterate(impuestos.get("TrasladosDR")):
                taxes.append(
                    _tax_entry(
                        traslado,
                        is_retention=False,
                        base_key="BaseDR",
                        impuesto_key="ImpuestoDR",
                        tipo_factor_key="TipoFactorDR",
                        tasa_key="TasaOCuotaDR",
                        importe_key="ImporteDR",
                    )
                )
            for retencion in iterate(impuestos.get("RetencionesDR")):
                taxes.append(
                    _tax_entry(
                        retencion,
                        is_retention=True,
                        base_key="BaseDR",
                        impuesto_key="ImpuestoDR",
                        tipo_factor_key="TipoFactorDR",
                        tasa_key="TasaOCuotaDR",
                        importe_key="ImporteDR",
                    )
                )
            if taxes:
                doc["Taxes"] = taxes
            related.append(doc)
        payment["RelatedDocuments"] = related
        payments.append(payment)
    return payments


def _map_payroll(nomina) -> dict:
    payroll: dict[str, Any] = {
        "Type": str(_enum_value(nomina["TipoNomina"])),
        "PaymentDate": _format_date(nomina["FechaPago"], date_only=True),
        "InitialPaymentDate": _format_date(nomina["FechaInicialPago"], date_only=True),
        "FinalPaymentDate": _format_date(nomina["FechaFinalPago"], date_only=True),
        "DaysPaid": _num(nomina["NumDiasPagados"]),
    }

    if emisor := nomina.get("Emisor"):
        issuer: dict[str, Any] = {}
        if registro := emisor.get("RegistroPatronal"):
            issuer["EmployerRegistration"] = str(registro)
        if rfc_origen := emisor.get("RfcPatronOrigen"):
            issuer["FromEmployerRfc"] = str(rfc_origen)
        if issuer:
            payroll["Issuer"] = issuer

    receptor = nomina["Receptor"]
    employee: dict[str, Any] = {
        "Curp": str(receptor["Curp"]),
        "ContractType": str(_enum_value(receptor["TipoContrato"])),
        "RegimeType": str(_enum_value(receptor["TipoRegimen"])),
        "EmployeeNumber": str(receptor["NumEmpleado"]),
        "FrequencyPayment": str(_enum_value(receptor["PeriodicidadPago"])),
        "FederalEntityKey": str(_enum_value(receptor["ClaveEntFed"])),
    }
    if nss := receptor.get("NumSeguridadSocial"):
        employee["SocialSecurityNumber"] = str(nss)
    if inicio := receptor.get("FechaInicioRelLaboral"):
        employee["StartDateLaborRelations"] = _format_date(inicio, date_only=True)
    if receptor.get("Sindicalizado") is not None:
        employee["Unionized"] = bool(_as_bool(receptor.get("Sindicalizado")))
    if jornada := receptor.get("TipoJornada"):
        employee["TypeOfJourney"] = str(_enum_value(jornada))
    if depto := receptor.get("Departamento"):
        employee["Department"] = str(depto)
    if puesto := receptor.get("Puesto"):
        employee["Position"] = str(puesto)
    if riesgo := receptor.get("RiesgoPuesto"):
        employee["PositionRisk"] = str(_enum_value(riesgo))
    if banco := receptor.get("Banco"):
        employee["Bank"] = str(_enum_value(banco))
    if cuenta := receptor.get("CuentaBancaria"):
        employee["BankAccount"] = str(cuenta)
    if sbc := receptor.get("SalarioBaseCotApor"):
        employee["BaseSalary"] = _num(sbc)
    if sdi := receptor.get("SalarioDiarioIntegrado"):
        employee["DailySalary"] = _num(sdi)
    payroll["Employee"] = employee

    if percepciones := nomina.get("Percepciones"):
        details = []
        for p in iterate(percepciones.get("Percepcion")):
            details.append(
                {
                    "PerceptionType": str(_enum_value(p["TipoPercepcion"])),
                    "Code": str(p["Clave"]),
                    "Description": str(p["Concepto"]),
                    "TaxedAmount": _num(p["ImporteGravado"]),
                    "ExemptAmount": _num(p["ImporteExento"]),
                }
            )
        payroll["Perceptions"] = {"Details": details}

    if deducciones := nomina.get("Deducciones"):
        details = []
        for d in iterate(deducciones.get("Deduccion")):
            details.append(
                {
                    "DeduccionType": str(_enum_value(d["TipoDeduccion"])),
                    "Code": str(d["Clave"]),
                    "Description": str(d["Concepto"]),
                    "Amount": _num(d["Importe"]),
                }
            )
        payroll["Deductions"] = {"Details": details}

    if otros := nomina.get("OtrosPagos"):
        other_payments = []
        for o in iterate(otros):
            entry: dict[str, Any] = {
                "OtherPaymentType": str(_enum_value(o["TipoOtroPago"])),
                "Code": str(o["Clave"]),
                "Description": str(o["Concepto"]),
                "Amount": _num(o["Importe"]),
            }
            subsidio = o.get("SubsidioAlEmpleo")
            if subsidio is not None:
                if isinstance(subsidio, dict):
                    amount = subsidio.get("SubsidioCausado") or subsidio.get("Amount")
                else:
                    amount = subsidio
                entry["EmploymentSubsidy"] = {"Amount": _num(amount)}
            other_payments.append(entry)
        payroll["OtherPayments"] = other_payments

    if incapacidades := nomina.get("Incapacidades"):
        incapacity = []
        for i in iterate(incapacidades):
            entry = {
                "Days": i["DiasIncapacidad"],
                "IncapacityType": str(_enum_value(i["TipoIncapacidad"])),
            }
            if importe := i.get("ImporteMonetario"):
                entry["Amount"] = _num(importe)
            incapacity.append(entry)
        payroll["Incapacities"] = incapacity

    return payroll


def _base_payload(cfdi: CFDI, tipo: str) -> dict:
    emisor = cfdi["Emisor"]
    receptor = cfdi["Receptor"]
    payload: dict[str, Any] = {
        "CfdiType": tipo,
        "ExpeditionPlace": str(cfdi["LugarExpedicion"]),
        "Issuer": {
            "Rfc": emisor["Rfc"],
            "Name": emisor["Nombre"],
            "FiscalRegime": str(_enum_value(emisor["RegimenFiscal"])),
        },
        "Receiver": {
            "Rfc": receptor["Rfc"],
            "Name": receptor["Nombre"],
            "CfdiUse": str(_enum_value(receptor["UsoCFDI"])),
            "FiscalRegime": str(_enum_value(receptor["RegimenFiscalReceptor"])),
            "TaxZipCode": str(receptor["DomicilioFiscalReceptor"]),
        },
    }
    if fecha := _format_date(cfdi.get("Fecha")):
        payload["Date"] = fecha
    if serie := cfdi.get("Serie"):
        payload["Serie"] = str(serie)
    if folio := cfdi.get("Folio"):
        payload["Folio"] = str(folio)
    if confirmacion := cfdi.get("Confirmacion"):
        payload["Confirmation"] = str(confirmacion)
    if exportacion := cfdi.get("Exportacion"):
        payload["Exportation"] = str(_enum_value(exportacion))
    if relations := _map_relations(cfdi):
        payload["Relations"] = relations
    if info_global := cfdi.get("InformacionGlobal"):
        payload["GlobalInformation"] = {
            "Periodicity": str(_enum_value(info_global["Periodicidad"])),
            "Months": str(_enum_value(info_global["Meses"])),
            "Year": str(info_global["Año"]),
        }
    return payload


def cfdi_to_facturama_payload(cfdi: CFDI) -> dict:
    """Map a satcfdi CFDI (typically unsigned) to Facturama Multiemisor JSON."""
    if not isinstance(cfdi, CFDI):
        raise TypeError("cfdi must be a CFDI object")

    tipo = str(_enum_value(cfdi.get("TipoDeComprobante")))
    if tipo not in _SUPPORTED_TIPOS:
        raise NotImplementedError(
            f"Facturama Multiemisor adapter supports TipoDeComprobante "
            f"{sorted(_SUPPORTED_TIPOS)}, got {tipo!r}"
        )

    payload = _base_payload(cfdi, tipo)

    if tipo in _ITEM_TIPOS:
        if forma := cfdi.get("FormaPago"):
            payload["PaymentForm"] = str(_enum_value(forma))
        if metodo := cfdi.get("MetodoPago"):
            payload["PaymentMethod"] = str(_enum_value(metodo))
        if moneda := cfdi.get("Moneda"):
            payload["Currency"] = str(_enum_value(moneda))
        if tipo_cambio := cfdi.get("TipoCambio"):
            payload["ExchangeRate"] = _num(tipo_cambio)
        if descuento := cfdi.get("Descuento"):
            payload["Discount"] = _num(descuento)
        if condiciones := cfdi.get("CondicionesDePago"):
            payload["PaymentConditions"] = str(condiciones)
        payload["Items"] = _map_items(cfdi)

        unsupported = set()
        complemento = cfdi.get("Complemento") or {}
        if isinstance(complemento, dict):
            unsupported = {
                k for k in complemento
                if k not in {"TimbreFiscalDigital", "Pagos", "Nomina", "Pago"}
            }
        if unsupported:
            raise NotImplementedError(
                f"Unsupported Complemento nodes for item CFDI mapper: {sorted(unsupported)}"
            )
        return payload

    if tipo == "P":
        pagos = _complement_node(cfdi, "Pagos")
        if not pagos:
            raise ValueError("CFDI tipo P requires Complemento Pagos 2.0")
        payload["Complemento"] = {"Payments": _map_payments(pagos)}
        # Facturama forbids root PaymentForm/Method/Currency/Items on payment CFDI
        return payload

    # tipo == "N"
    if metodo := cfdi.get("MetodoPago"):
        payload["PaymentMethod"] = str(_enum_value(metodo))
    if forma := cfdi.get("FormaPago"):
        payload["PaymentForm"] = str(_enum_value(forma))
    if moneda := cfdi.get("Moneda"):
        currency = str(_enum_value(moneda))
        if currency != "MXN":
            payload["Currency"] = currency
            if tipo_cambio := cfdi.get("TipoCambio"):
                payload["ExchangeRate"] = _num(tipo_cambio)
    nomina = _complement_node(cfdi, "Nomina")
    if not nomina:
        raise ValueError("CFDI tipo N requires Complemento Nomina 1.2")
    payload["NameId"] = "16"
    payload["Complemento"] = {"Payroll": _map_payroll(nomina)}
    return payload


class Facturama(PAC):
    """
    Facturama Multiemisor API adapter.

    Facturama is a billing platform that seals+stamps via Multiemisor; CSD files
    must be uploaded first (see :meth:`upload_csd`).

    Documentation: https://apisandbox.facturama.mx/guias/api-multi/proceso-facturacion
    """

    # Facturama aggregates multiple PACs; no single PAC RFC applies.
    RFC = None

    def __init__(self, username: str, password: str, environment=Environment.PRODUCTION):
        super().__init__(environment=environment)
        self.auth = HTTPBasicAuth(username, password)

    @property
    def host(self) -> str:
        match self.environment:
            case Environment.PRODUCTION:
                return "https://api.facturama.mx"
            case Environment.TEST:
                return "https://apisandbox.facturama.mx"
            case _:
                raise NotImplementedError("Environment not supported")

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict | None = None,
        params: dict | None = None,
    ):
        r = requests.request(
            method=method,
            url=f"{self.host}/{path.lstrip('/')}",
            headers={
                "User-Agent": __version__.__user_agent__,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            auth=self.auth,
            json=json,
            params=params,
        )
        if r.ok:
            if not r.content:
                return None
            content_type = (r.headers.get("Content-Type") or "").lower()
            if "application/json" in content_type:
                return r.json()
            return r.content
        raise ResponseError(r)

    def _download_file(self, document_id: str, fmt: str) -> bytes:
        res = self._request(
            "get",
            f"api/Cfdi/{fmt}/issuedLite/{document_id}",
        )
        if isinstance(res, dict) and "Content" in res:
            return base64.urlsafe_b64decode(res["Content"].encode("utf-8"))
        if isinstance(res, (bytes, bytearray)):
            return bytes(res)
        raise ResponseError(res)

    def upload_csd(
        self,
        rfc: str,
        certificate: bytes,
        key: bytes,
        password: str | bytes,
    ) -> dict:
        """Upload issuer CSD required before Multiemisor issue()."""
        if isinstance(password, bytes):
            password = password.decode()
        return self._request(
            "post",
            "api-lite/csds",
            json={
                "Rfc": rfc.upper(),
                "Certificate": base64.b64encode(certificate).decode("ascii"),
                "PrivateKey": base64.b64encode(key).decode("ascii"),
                "PrivateKeyPassword": password,
            },
        )

    def delete_csd(self, rfc: str) -> None:
        self._request("delete", f"api-lite/csds/{rfc.upper()}")

    def get_csd(self, rfc: str) -> dict:
        return self._request("get", f"api-lite/csds/{rfc.upper()}")

    def list_cfdis(self, *, keyword: str | None = None, status: str = "all") -> list[dict]:
        """List Multiemisor CFDIs (optionally filtered by keyword / UUID)."""
        params = {"status": status}
        if keyword:
            params["keyword"] = keyword
        results = self._request("get", "api-lite/cfdis", params=params)
        if results is None:
            return []
        if isinstance(results, list):
            return results
        for key in ("data", "Data", "Cfdis", "items"):
            if isinstance(results.get(key), list):
                return results[key]
        return []

    def find_id_by_uuid(self, uuid: str) -> str:
        """Resolve Facturama document Id from a stamped CFDI UUID."""
        uuid_u = str(uuid).upper()
        for item in self.list_cfdis(keyword=uuid):
            item_uuid = str(item.get("Uuid") or item.get("UUID") or "").upper()
            item_id = str(item.get("Id") or "")
            if item_uuid == uuid_u or item_id.upper() == uuid_u:
                return item["Id"]
        raise DocumentNotFoundError(f"Facturama document not found for UUID {uuid}")

    def issue(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        """
        Seal and stamp via Facturama Multiemisor.

        The local CFDI does not need to be signed; Facturama seals with the
        uploaded CSD for the issuer RFC.
        """
        payload = cfdi_to_facturama_payload(cfdi)
        created = self._request("post", "api-lite/3/cfdis", json=payload)
        document_id = created["Id"]

        xml = None
        pdf = None
        if accept & Accept.XML:
            xml = self._download_file(document_id, "xml")
        if accept & Accept.PDF:
            pdf = self._download_file(document_id, "pdf")

        return Document(document_id=document_id, xml=xml, pdf=pdf)

    def stamp(self, cfdi: CFDI, accept: Accept = Accept.XML) -> Document:
        raise NotImplementedError(
            "Facturama Multiemisor does not stamp pre-signed XML; use issue() "
            "(Facturama seals and stamps from the mapped JSON payload)."
        )

    def recover(self, document_id: str, accept: Accept = Accept.XML) -> Document:
        xml = self._download_file(document_id, "xml") if accept & Accept.XML else None
        pdf = self._download_file(document_id, "pdf") if accept & Accept.PDF else None
        return Document(document_id=document_id, xml=xml, pdf=pdf)

    def recover_by_uuid(self, uuid: str, accept: Accept = Accept.XML) -> Document:
        return self.recover(self.find_id_by_uuid(uuid), accept=accept)

    def cancel(
        self,
        cfdi: CFDI,
        reason: CancelReason,
        substitution_id: str = None,
        signer: Signer = None,
        document_id: str = None,
    ) -> CancelationAcknowledgment:
        """
        Cancel a Multiemisor CFDI.

        Resolves Facturama Id from ``document_id`` or from the CFDI UUID
        (``Complemento.TimbreFiscalDigital.UUID``) via :meth:`find_id_by_uuid`.
        """
        del signer  # Facturama cancels with account credentials, not local FIEL
        if document_id:
            facturama_id = document_id
        else:
            uuid = cfdi["Complemento"]["TimbreFiscalDigital"]["UUID"]
            facturama_id = self.find_id_by_uuid(uuid)

        params = {"motive": reason.value}
        if substitution_id:
            params["uuidReplacement"] = substitution_id

        res = self._request(
            "delete",
            f"api-lite/cfdis/{facturama_id}",
            params=params,
        )
        status = None
        acuse = None
        if isinstance(res, dict):
            status = res.get("Status") or res.get("Message") or res
            if content := res.get("AcuseXmlBase64") or res.get("Acuse"):
                if isinstance(content, str):
                    try:
                        acuse = base64.b64decode(content)
                    except Exception:
                        acuse = content.encode() if content else None
        return CancelationAcknowledgment(code=status or "cancelled", acuse=acuse)
