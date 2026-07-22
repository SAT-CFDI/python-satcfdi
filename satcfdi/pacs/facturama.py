"""
Facturama PAC adapters (Multiemisor and API Web).

Facturama seals and stamps from a JSON payload. Pre-signed XML stamp is not
supported by their public Multiemisor/Web JSON APIs.

Supported TipoDeComprobante: I, E, T, P (Pagos 2.0), N (Nómina 1.2).

Item CFDIs may include:
- Carta Porte 3.1 (NameId ``36``) — Multiemisor and Web
- Donativos (NameId ``9``) — Multiemisor and Web
- Leyendas fiscales (TaxLegends)
- Impuestos locales (via item Taxes with ``IsFederalTax: false``)
- Comercio exterior 2.0 (NameId ``26``) — **API Web only** (:class:`FacturamaWeb`)

Docs: https://apisandbox.facturama.mx/guias
"""
from __future__ import annotations

import base64
from collections.abc import Mapping
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
from ..models import Code, Signer
from ..utils import iterate

_TAX_NAME = {
    "001": "ISR",
    "002": "IVA",
    "003": "IEPS",
}

_ITEM_TIPOS = {"I", "E", "T"}
_SUPPORTED_TIPOS = _ITEM_TIPOS | {"P", "N"}
_ITEM_COMPLEMENT_KEYS = {
    "TimbreFiscalDigital",
    "Pagos",
    "Nomina",
    "Pago",
    "CartaPorte",
    "Donatarias",
    "LeyendasFiscales",
    "ImpuestosLocales",
    "ComercioExterior",
}
_CARTA_PORTE_NAME_ID = "36"
_DONATION_NAME_ID = "9"
_FOREIGN_TRADE_NAME_ID = "26"


def _enum_value(val):
    if isinstance(val, Enum):
        return val.value
    return val


def _code_str(val) -> str | None:
    if val is None:
        return None
    if isinstance(val, Code):
        return str(val.code)
    if hasattr(val, "code") and not isinstance(val, type):
        code = getattr(val, "code", None)
        if code is not None and not callable(code):
            return str(code)
    return str(_enum_value(val))


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


def _set_opt(target: dict, key: str, value) -> None:
    if value is not None and value != "":
        target[key] = value


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
        "IsFederalTax": True,
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
    if name == "CartaPorte" and (
        "CartaPorte" in tag
        or (
            "TranspInternac" in complemento
            and ("Ubicaciones" in complemento or "Mercancias" in complemento)
        )
    ):
        return complemento
    if name == "Donatarias" and (
        "donat" in tag.lower()
        or "NoAutorizacion" in complemento
    ):
        return complemento
    if name == "LeyendasFiscales" and (
        "leyendasFiscales" in tag
        or (
            "Leyenda" in complemento
            and "NoAutorizacion" not in complemento
            and not isinstance(complemento.get("Leyenda"), str)
        )
    ):
        return complemento
    if name == "ImpuestosLocales" and (
        "implocal" in tag.lower()
        or "TotaldeTraslados" in complemento
        or "TotaldeRetenciones" in complemento
    ):
        return complemento
    if name == "ComercioExterior" and (
        "ComercioExterior" in tag
        or "ClaveDePedimento" in complemento
        or "TotalUSD" in complemento
    ):
        return complemento
    return None


def _is_carta_porte_body(complemento) -> bool:
    if not complemento or not isinstance(complemento, Mapping):
        return False
    tag = getattr(complemento, "tag", "") or ""
    if "CartaPorte" in tag:
        return True
    return "TranspInternac" in complemento and (
        "Ubicaciones" in complemento or "Mercancias" in complemento
    )


def _is_known_item_complement_body(complemento) -> bool:
    if not complemento or not isinstance(complemento, Mapping):
        return False
    return (
        _is_carta_porte_body(complemento)
        or "NoAutorizacion" in complemento
        or ("Leyenda" in complemento and "Version" in complemento)
        or "TotaldeTraslados" in complemento
        or "TotaldeRetenciones" in complemento
        or "ClaveDePedimento" in complemento
    )


def _map_domicilio(domicilio) -> dict | None:
    if not domicilio:
        return None
    mapped: dict[str, Any] = {}
    _set_opt(mapped, "Calle", domicilio.get("Calle") and str(domicilio["Calle"]))
    _set_opt(
        mapped,
        "NumeroExterior",
        domicilio.get("NumeroExterior") and str(domicilio["NumeroExterior"]),
    )
    _set_opt(
        mapped,
        "NumeroInterior",
        domicilio.get("NumeroInterior") and str(domicilio["NumeroInterior"]),
    )
    _set_opt(mapped, "Colonia", _code_str(domicilio.get("Colonia")))
    _set_opt(mapped, "Localidad", _code_str(domicilio.get("Localidad")))
    _set_opt(
        mapped,
        "Referencia",
        domicilio.get("Referencia") and str(domicilio["Referencia"]),
    )
    _set_opt(mapped, "Municipio", _code_str(domicilio.get("Municipio")))
    _set_opt(mapped, "Estado", _code_str(domicilio.get("Estado")))
    _set_opt(mapped, "Pais", _code_str(domicilio.get("Pais")))
    _set_opt(
        mapped,
        "CodigoPostal",
        domicilio.get("CodigoPostal") and str(domicilio["CodigoPostal"]),
    )
    return mapped or None


def _map_regimenes_aduaneros(regimenes) -> list[dict]:
    result = []
    for regimen in iterate(regimenes):
        if isinstance(regimen, Mapping) and "RegimenAduanero" in regimen:
            code = _code_str(regimen["RegimenAduanero"])
        else:
            code = _code_str(regimen)
        if code:
            result.append({"RegimenAduanero": code})
    return result


def _map_partes_transporte(partes) -> list[dict]:
    result = []
    for parte in iterate(partes):
        if isinstance(parte, Mapping) and "ParteTransporte" in parte:
            code = _code_str(parte["ParteTransporte"])
        else:
            code = _code_str(parte)
        if code:
            result.append({"ParteTransporte": code})
    return result


def _map_ubicacion(ubicacion) -> dict:
    mapped: dict[str, Any] = {
        "TipoUbicacion": str(ubicacion["TipoUbicacion"]),
        "RFCRemitenteDestinatario": str(ubicacion["RFCRemitenteDestinatario"]),
        "FechaHoraSalidaLlegada": _format_date(ubicacion["FechaHoraSalidaLlegada"]),
    }
    _set_opt(mapped, "IDUbicacion", ubicacion.get("IDUbicacion") and str(ubicacion["IDUbicacion"]))
    _set_opt(
        mapped,
        "NombreRemitenteDestinatario",
        ubicacion.get("NombreRemitenteDestinatario")
        and str(ubicacion["NombreRemitenteDestinatario"]),
    )
    _set_opt(mapped, "NumRegIdTrib", ubicacion.get("NumRegIdTrib") and str(ubicacion["NumRegIdTrib"]))
    _set_opt(mapped, "ResidenciaFiscal", _code_str(ubicacion.get("ResidenciaFiscal")))
    _set_opt(mapped, "NumEstacion", _code_str(ubicacion.get("NumEstacion")))
    _set_opt(
        mapped,
        "NombreEstacion",
        ubicacion.get("NombreEstacion") and str(ubicacion["NombreEstacion"]),
    )
    _set_opt(mapped, "NavegacionTrafico", _code_str(ubicacion.get("NavegacionTrafico")))
    _set_opt(mapped, "TipoEstacion", _code_str(ubicacion.get("TipoEstacion")))
    if ubicacion.get("DistanciaRecorrida") is not None:
        mapped["DistanciaRecorrida"] = _num(ubicacion["DistanciaRecorrida"])
    if domicilio := _map_domicilio(ubicacion.get("Domicilio")):
        mapped["Domicilio"] = domicilio
    return mapped


def _map_cantidad_transporta(items) -> list[dict]:
    result = []
    for item in iterate(items):
        entry: dict[str, Any] = {
            "Cantidad": _num(item["Cantidad"]),
            "IDOrigen": str(item["IDOrigen"]),
            "IDDestino": str(item["IDDestino"]),
        }
        _set_opt(entry, "CvesTransporte", _code_str(item.get("CvesTransporte")))
        result.append(entry)
    return result


def _map_documentacion_aduanera(items) -> list[dict]:
    result = []
    for item in iterate(items):
        entry: dict[str, Any] = {
            "TipoDocumento": _code_str(item["TipoDocumento"]),
        }
        _set_opt(entry, "NumPedimento", item.get("NumPedimento") and str(item["NumPedimento"]))
        _set_opt(
            entry,
            "IdentDocAduanero",
            item.get("IdentDocAduanero") and str(item["IdentDocAduanero"]),
        )
        _set_opt(entry, "RFCImpo", item.get("RFCImpo") and str(item["RFCImpo"]))
        result.append(entry)
    return result


def _map_guias_identificacion(items) -> list[dict]:
    result = []
    for item in iterate(items):
        result.append(
            {
                "NumeroGuiaIdentificacion": str(item["NumeroGuiaIdentificacion"]),
                "DescripGuiaIdentificacion": str(item["DescripGuiaIdentificacion"]),
                "PesoGuiaIdentificacion": _num(item["PesoGuiaIdentificacion"]),
            }
        )
    return result


def _map_detalle_mercancia(detalle) -> dict | None:
    if not detalle:
        return None
    mapped: dict[str, Any] = {
        "UnidadPesoMerc": _code_str(detalle["UnidadPesoMerc"]),
        "PesoBruto": _num(detalle["PesoBruto"]),
        "PesoNeto": _num(detalle["PesoNeto"]),
        "PesoTara": _num(detalle["PesoTara"]),
    }
    if detalle.get("NumPiezas") is not None:
        mapped["NumPiezas"] = int(detalle["NumPiezas"])
    return mapped


def _map_mercancia(mercancia) -> dict:
    mapped: dict[str, Any] = {
        "BienesTransp": _code_str(mercancia["BienesTransp"]),
        "Descripcion": str(mercancia["Descripcion"]),
        "Cantidad": _num(mercancia["Cantidad"]),
        "ClaveUnidad": _code_str(mercancia["ClaveUnidad"]),
        "PesoEnKg": _num(mercancia["PesoEnKg"]),
    }
    optional_str = (
        ("ClaveSTCC", "ClaveSTCC"),
        ("Unidad", "Unidad"),
        ("Dimensiones", "Dimensiones"),
        ("DescripEmbalaje", "DescripEmbalaje"),
        ("NombreIngredienteActivo", "NombreIngredienteActivo"),
        ("NomQuimico", "NomQuimico"),
        ("DenominacionGenericaProd", "DenominacionGenericaProd"),
        ("DenominacionDistintivaProd", "DenominacionDistintivaProd"),
        ("Fabricante", "Fabricante"),
        ("LoteMedicamento", "LoteMedicamento"),
        ("RegistroSanitarioFolioAutorizacion", "RegistroSanitarioFolioAutorizacion"),
        ("PermisoImportacion", "PermisoImportacion"),
        ("FolioImpoVUCEM", "FolioImpoVUCEM"),
        ("NumCAS", "NumCAS"),
        ("RazonSocialEmpImp", "RazonSocialEmpImp"),
        ("NumRegSanPlagCOFEPRIS", "NumRegSanPlagCOFEPRIS"),
        ("DatosFabricante", "DatosFabricante"),
        ("DatosFormulador", "DatosFormulador"),
        ("DatosMaquilador", "DatosMaquilador"),
        ("UsoAutorizado", "UsoAutorizado"),
        ("DescripcionMateria", "DescripcionMateria"),
        ("UUIDComercioExt", "UUIDComercioExt"),
    )
    for src, dst in optional_str:
        if mercancia.get(src) is not None:
            mapped[dst] = str(mercancia[src])

    optional_code = (
        "MaterialPeligroso",
        "CveMaterialPeligroso",
        "Embalaje",
        "SectorCOFEPRIS",
        "FormaFarmaceutica",
        "CondicionesEspTransp",
        "Moneda",
        "FraccionArancelaria",
        "TipoMateria",
    )
    for key in optional_code:
        _set_opt(mapped, key, _code_str(mercancia.get(key)))

    if mercancia.get("FechaCaducidad") is not None:
        mapped["FechaCaducidad"] = _format_date(mercancia["FechaCaducidad"], date_only=True)
    if mercancia.get("ValorMercancia") is not None:
        mapped["ValorMercancia"] = _num(mercancia["ValorMercancia"])
    if docs := mercancia.get("DocumentacionAduanera"):
        mapped["DocumentacionAduanera"] = _map_documentacion_aduanera(docs)
    if guias := mercancia.get("GuiasIdentificacion"):
        mapped["GuiasIdentificacion"] = _map_guias_identificacion(guias)
    if cantidad := mercancia.get("CantidadTransporta"):
        mapped["CantidadTransporta"] = _map_cantidad_transporta(cantidad)
    if detalle := _map_detalle_mercancia(mercancia.get("DetalleMercancia")):
        mapped["DetalleMercancia"] = detalle
    return mapped


def _map_remolques(remolques) -> list[dict]:
    return [
        {
            "SubTipoRem": _code_str(remolque["SubTipoRem"]),
            "Placa": str(remolque["Placa"]),
        }
        for remolque in iterate(remolques)
    ]


def _map_seguros(seguros) -> dict:
    mapped: dict[str, Any] = {
        "AseguraRespCivil": str(seguros["AseguraRespCivil"]),
        "PolizaRespCivil": str(seguros["PolizaRespCivil"]),
    }
    _set_opt(
        mapped,
        "AseguraMedAmbiente",
        seguros.get("AseguraMedAmbiente") and str(seguros["AseguraMedAmbiente"]),
    )
    _set_opt(
        mapped,
        "PolizaMedAmbiente",
        seguros.get("PolizaMedAmbiente") and str(seguros["PolizaMedAmbiente"]),
    )
    _set_opt(
        mapped,
        "AseguraCarga",
        seguros.get("AseguraCarga") and str(seguros["AseguraCarga"]),
    )
    _set_opt(
        mapped,
        "PolizaCarga",
        seguros.get("PolizaCarga") and str(seguros["PolizaCarga"]),
    )
    if seguros.get("PrimaSeguro") is not None:
        mapped["PrimaSeguro"] = _num(seguros["PrimaSeguro"])
    return mapped


def _map_identificacion_vehicular(ident) -> dict:
    return {
        "ConfigVehicular": _code_str(ident["ConfigVehicular"]),
        "PesoBrutoVehicular": _num(ident["PesoBrutoVehicular"]),
        "PlacaVM": str(ident["PlacaVM"]),
        "AnioModeloVM": int(ident["AnioModeloVM"]),
    }


def _map_autotransporte(auto) -> dict:
    mapped: dict[str, Any] = {
        "PermSCT": _code_str(auto["PermSCT"]),
        "NumPermisoSCT": str(auto["NumPermisoSCT"]),
        "IdentificacionVehicular": _map_identificacion_vehicular(
            auto["IdentificacionVehicular"]
        ),
        "Seguros": _map_seguros(auto["Seguros"]),
    }
    if remolques := auto.get("Remolques"):
        mapped["Remolques"] = _map_remolques(remolques)
    return mapped


def _map_transporte_aereo(aereo) -> dict:
    mapped: dict[str, Any] = {
        "PermSCT": _code_str(aereo["PermSCT"]),
        "NumPermisoSCT": str(aereo["NumPermisoSCT"]),
        "NumeroGuia": str(aereo["NumeroGuia"]),
        "CodigoTransportista": _code_str(aereo["CodigoTransportista"]),
    }
    for key in (
        "MatriculaAeronave",
        "NombreAseg",
        "NumPolizaSeguro",
        "LugarContrato",
        "RFCEmbarcador",
        "NumRegIdTribEmbarc",
        "NombreEmbarcador",
    ):
        if aereo.get(key) is not None:
            mapped[key] = str(aereo[key])
    _set_opt(mapped, "ResidenciaFiscalEmbarc", _code_str(aereo.get("ResidenciaFiscalEmbarc")))
    return mapped


def _map_transporte_maritimo(maritimo) -> dict:
    mapped: dict[str, Any] = {
        "TipoEmbarcacion": _code_str(maritimo["TipoEmbarcacion"]),
        "Matricula": str(maritimo["Matricula"]),
        "NumeroOMI": str(maritimo["NumeroOMI"]),
        "NacionalidadEmbarc": _code_str(maritimo["NacionalidadEmbarc"]),
        "UnidadesDeArqBruto": _num(maritimo["UnidadesDeArqBruto"]),
        "TipoCarga": _code_str(maritimo["TipoCarga"]),
        "NombreAgenteNaviero": str(maritimo["NombreAgenteNaviero"]),
        "NumAutorizacionNaviero": str(maritimo["NumAutorizacionNaviero"]),
    }
    for key in (
        "PermSCT",
        "NumPermisoSCT",
        "NombreAseg",
        "NumPolizaSeguro",
        "NombreEmbarc",
        "LineaNaviera",
        "NumViaje",
        "NumConocEmbarc",
        "PermisoTempNavegacion",
    ):
        if maritimo.get(key) is not None:
            if key == "PermSCT":
                mapped[key] = _code_str(maritimo[key])
            else:
                mapped[key] = str(maritimo[key])
    for key in ("AnioEmbarcacion",):
        if maritimo.get(key) is not None:
            mapped[key] = int(maritimo[key])
    for key in ("Eslora", "Manga", "Calado", "Puntal"):
        if maritimo.get(key) is not None:
            mapped[key] = _num(maritimo[key])
    if contenedores := maritimo.get("Contenedor"):
        mapped["Contenedor"] = [
            {
                k: (_num(v) if k.startswith("Peso") else _code_str(v) if k == "TipoContenedor" else str(v))
                for k, v in cont.items()
                if v is not None
            }
            for cont in iterate(contenedores)
        ]
    return mapped


def _map_transporte_ferroviario(ferro) -> dict:
    mapped: dict[str, Any] = {
        "TipoDeServicio": _code_str(ferro["TipoDeServicio"]),
        "TipoDeTrafico": _code_str(ferro["TipoDeTrafico"]),
        "Carro": [
            {
                "TipoCarro": _code_str(carro["TipoCarro"]),
                "MatriculaCarro": str(carro["MatriculaCarro"]),
                "GuiaCarro": str(carro["GuiaCarro"]),
                "ToneladasNetasCarro": _num(carro["ToneladasNetasCarro"]),
                **(
                    {
                        "Contenedor": [
                            {
                                "TipoContenedor": _code_str(c["TipoContenedor"]),
                                "PesoContenedorVacio": _num(c["PesoContenedorVacio"]),
                                "PesoNetoMercancia": _num(c["PesoNetoMercancia"]),
                            }
                            for c in iterate(carro["Contenedor"])
                        ]
                    }
                    if carro.get("Contenedor")
                    else {}
                ),
            }
            for carro in iterate(ferro["Carro"])
        ],
    }
    _set_opt(mapped, "NombreAseg", ferro.get("NombreAseg") and str(ferro["NombreAseg"]))
    _set_opt(
        mapped,
        "NumPolizaSeguro",
        ferro.get("NumPolizaSeguro") and str(ferro["NumPolizaSeguro"]),
    )
    if derechos := ferro.get("DerechosDePaso"):
        mapped["DerechosDePaso"] = [
            {
                "TipoDerechoDePaso": _code_str(d["TipoDerechoDePaso"]),
                "KilometrajePagado": _num(d["KilometrajePagado"]),
            }
            for d in iterate(derechos)
        ]
    return mapped


def _map_mercancias(mercancias) -> dict:
    mapped: dict[str, Any] = {
        "PesoBrutoTotal": _num(mercancias["PesoBrutoTotal"]),
        "UnidadPeso": _code_str(mercancias["UnidadPeso"]),
        "NumTotalMercancias": int(mercancias["NumTotalMercancias"]),
        "Mercancia": [_map_mercancia(m) for m in iterate(mercancias["Mercancia"])],
    }
    if mercancias.get("PesoNetoTotal") is not None:
        mapped["PesoNetoTotal"] = _num(mercancias["PesoNetoTotal"])
    if mercancias.get("CargoPorTasacion") is not None:
        mapped["CargoPorTasacion"] = _num(mercancias["CargoPorTasacion"])
    if mercancias.get("LogisticaInversaRecoleccionDevolucion") is not None:
        mapped["LogisticaInversaRecoleccionDevolucion"] = str(
            _enum_value(mercancias["LogisticaInversaRecoleccionDevolucion"])
        )
    if auto := mercancias.get("Autotransporte"):
        mapped["Autotransporte"] = _map_autotransporte(auto)
    if maritimo := mercancias.get("TransporteMaritimo"):
        mapped["TransporteMaritimo"] = _map_transporte_maritimo(maritimo)
    if aereo := mercancias.get("TransporteAereo"):
        mapped["TransporteAereo"] = _map_transporte_aereo(aereo)
    if ferro := mercancias.get("TransporteFerroviario"):
        mapped["TransporteFerroviario"] = _map_transporte_ferroviario(ferro)
    return mapped


def _map_figura_transporte(figura) -> dict:
    mapped: dict[str, Any] = {
        "TipoFigura": _code_str(figura["TipoFigura"]),
        "NombreFigura": str(figura["NombreFigura"]),
    }
    _set_opt(mapped, "RFCFigura", figura.get("RFCFigura") and str(figura["RFCFigura"]))
    _set_opt(mapped, "NumLicencia", figura.get("NumLicencia") and str(figura["NumLicencia"]))
    _set_opt(
        mapped,
        "NumRegIdTribFigura",
        figura.get("NumRegIdTribFigura") and str(figura["NumRegIdTribFigura"]),
    )
    _set_opt(
        mapped,
        "ResidenciaFiscalFigura",
        _code_str(figura.get("ResidenciaFiscalFigura")),
    )
    if partes := figura.get("PartesTransporte"):
        mapped["PartesTransporte"] = _map_partes_transporte(partes)
    if domicilio := _map_domicilio(figura.get("Domicilio")):
        mapped["Domicilio"] = domicilio
    return mapped


def _map_carta_porte(carta) -> dict:
    """Map satcfdi Carta Porte 3.1 to Facturama ``CartaPorte31`` JSON."""
    version = str(carta.get("Version") or "3.1")
    if version != "3.1":
        raise NotImplementedError(
            f"Facturama Multiemisor adapter supports Carta Porte 3.1 only, got {version!r}"
        )

    mapped: dict[str, Any] = {
        "TranspInternac": str(_enum_value(carta["TranspInternac"])),
        "Ubicaciones": [_map_ubicacion(u) for u in iterate(carta["Ubicaciones"])],
        "Mercancias": _map_mercancias(carta["Mercancias"]),
    }
    if carta.get("IdCCP") is not None:
        mapped["IdCCP"] = str(carta["IdCCP"])
    if carta.get("EntradaSalidaMerc") is not None:
        mapped["EntradaSalidaMerc"] = str(_enum_value(carta["EntradaSalidaMerc"]))
    _set_opt(mapped, "PaisOrigenDestino", _code_str(carta.get("PaisOrigenDestino")))
    _set_opt(mapped, "ViaEntradaSalida", _code_str(carta.get("ViaEntradaSalida")))
    if carta.get("TotalDistRec") is not None:
        mapped["TotalDistRec"] = _num(carta["TotalDistRec"])
    if carta.get("RegistroISTMO") is not None:
        mapped["RegistroISTMO"] = str(_enum_value(carta["RegistroISTMO"]))
    _set_opt(mapped, "UbicacionPoloOrigen", _code_str(carta.get("UbicacionPoloOrigen")))
    _set_opt(mapped, "UbicacionPoloDestino", _code_str(carta.get("UbicacionPoloDestino")))
    if regimenes := carta.get("RegimenesAduaneros"):
        mapped["RegimenesAduaneros"] = _map_regimenes_aduaneros(regimenes)
    if figuras := carta.get("FiguraTransporte"):
        mapped["FiguraTransporte"] = [
            _map_figura_transporte(f) for f in iterate(figuras)
        ]
    return mapped


def _format_donation_date(fecha) -> str:
    """Facturama Donation uses DD/MM/YYYY."""
    if isinstance(fecha, datetime):
        return fecha.strftime("%d/%m/%Y")
    if isinstance(fecha, date):
        return fecha.strftime("%d/%m/%Y")
    text = str(fecha)
    if len(text) >= 10 and text[4] == "-":
        # YYYY-MM-DD -> DD/MM/YYYY
        return f"{text[8:10]}/{text[5:7]}/{text[0:4]}"
    return text


def _map_donation(donat) -> dict:
    return {
        "AuthorizationDate": _format_donation_date(donat["FechaAutorizacion"]),
        "AuthorizationNumber": str(donat["NoAutorizacion"]),
        "Legend": str(donat["Leyenda"]),
    }


def _map_tax_legends(leyendas) -> dict:
    legends = []
    for leyenda in iterate(leyendas.get("Leyenda")):
        entry: dict[str, Any] = {"Text": str(leyenda["TextoLeyenda"])}
        _set_opt(
            entry,
            "TaxProvision",
            leyenda.get("DisposicionFiscal") and str(leyenda["DisposicionFiscal"]),
        )
        _set_opt(entry, "Norm", leyenda.get("Norma") and str(leyenda["Norma"]))
        legends.append(entry)
    return {"Legends": legends}


def _local_tax_entries(implocal) -> list[dict]:
    """
    Facturama has no ImpuestosLocales complement node; local taxes go on item
    Taxes with IsFederalTax=false (see API Web factura guide).
    """
    taxes = []
    for ret in iterate(implocal.get("RetencionesLocales")):
        taxes.append(
            {
                "Name": str(ret["ImpLocRetenido"]),
                "Rate": _num(ret["TasadeRetencion"]),
                "Total": _num(ret["Importe"]) or 0.0,
                "Base": 0.0,
                "IsRetention": True,
                "IsQuota": False,
                "IsFederalTax": False,
            }
        )
    for tras in iterate(implocal.get("TrasladosLocales")):
        taxes.append(
            {
                "Name": str(tras["ImpLocTrasladado"]),
                "Rate": _num(tras["TasadeTraslado"]),
                "Total": _num(tras["Importe"]) or 0.0,
                "Base": 0.0,
                "IsRetention": False,
                "IsQuota": False,
                "IsFederalTax": False,
            }
        )
    return taxes


def _apply_local_taxes_to_items(items: list[dict], implocal) -> None:
    local_taxes = _local_tax_entries(implocal)
    if not local_taxes or not items:
        return
    # Facturama models local taxes at item level; attach to the first concept.
    first = items[0]
    taxes = list(first.get("Taxes") or [])
    taxes.extend(local_taxes)
    first["Taxes"] = taxes
    line_total = first.get("Total") or 0.0
    for tax in local_taxes:
        if tax["IsRetention"]:
            line_total -= tax["Total"] or 0.0
        else:
            line_total += tax["Total"] or 0.0
    first["Total"] = line_total


def _map_foreign_trade_address(domicilio) -> dict | None:
    if not domicilio:
        return None
    mapped: dict[str, Any] = {}
    _set_opt(mapped, "Street", domicilio.get("Calle") and str(domicilio["Calle"]))
    _set_opt(
        mapped,
        "ExteriorNumber",
        domicilio.get("NumeroExterior") and str(domicilio["NumeroExterior"]),
    )
    _set_opt(
        mapped,
        "InteriorNumber",
        domicilio.get("NumeroInterior") and str(domicilio["NumeroInterior"]),
    )
    _set_opt(mapped, "Neighborhood", _code_str(domicilio.get("Colonia")))
    _set_opt(
        mapped,
        "Reference",
        domicilio.get("Referencia") and str(domicilio["Referencia"]),
    )
    _set_opt(mapped, "Locality", _code_str(domicilio.get("Localidad")))
    _set_opt(mapped, "Municipality", _code_str(domicilio.get("Municipio")))
    _set_opt(mapped, "State", _code_str(domicilio.get("Estado")))
    _set_opt(mapped, "Country", _code_str(domicilio.get("Pais")))
    _set_opt(
        mapped,
        "ZipCode",
        domicilio.get("CodigoPostal") and str(domicilio["CodigoPostal"]),
    )
    return mapped or None


def _map_foreign_trade(cce) -> dict:
    version = str(cce.get("Version") or "2.0")
    if not version.startswith("2"):
        raise NotImplementedError(
            f"Facturama ForeignTrade mapper supports ComercioExterior 2.x, got {version!r}"
        )

    mapped: dict[str, Any] = {
        "RequestCode": _code_str(cce["ClaveDePedimento"]),
        "ExchangeRateUSD": _num(cce["TipoCambioUSD"]),
        "TotalUSD": _num(cce["TotalUSD"]),
    }
    cert = cce.get("CertificadoOrigen")
    if cert is not None:
        mapped["OriginCertificate"] = bool(int(cert)) if not isinstance(cert, bool) else cert
    _set_opt(mapped, "OriginCertificateNumber", cce.get("NumCertificadoOrigen") and str(cce["NumCertificadoOrigen"]))
    _set_opt(
        mapped,
        "ReliableExporterNumber",
        cce.get("NumeroExportadorConfiable") and str(cce["NumeroExportadorConfiable"]),
    )
    _set_opt(mapped, "Incoterm", _code_str(cce.get("Incoterm")))
    _set_opt(mapped, "Observations", cce.get("Observaciones") and str(cce["Observaciones"]))
    _set_opt(mapped, "ReasonForTrasnfer", _code_str(cce.get("MotivoTraslado")))

    if emisor := cce.get("Emisor"):
        issuer: dict[str, Any] = {}
        if addr := _map_foreign_trade_address(emisor.get("Domicilio")):
            issuer["Address"] = addr
        _set_opt(issuer, "Curp", emisor.get("Curp") and str(emisor["Curp"]))
        if issuer:
            mapped["Issuer"] = issuer

    if receptor := cce.get("Receptor"):
        receiver: dict[str, Any] = {}
        if addr := _map_foreign_trade_address(receptor.get("Domicilio")):
            receiver["Address"] = addr
        _set_opt(
            receiver,
            "NumRegIdTrib",
            receptor.get("NumRegIdTrib") and str(receptor["NumRegIdTrib"]),
        )
        if receiver:
            mapped["Receiver"] = receiver

    if propietarios := cce.get("Propietario"):
        mapped["Owner"] = [
            {
                "NumRegIdTrib": str(p["NumRegIdTrib"]),
                "TaxResidence": _code_str(p["ResidenciaFiscal"]),
            }
            for p in iterate(propietarios)
        ]

    if destinatarios := cce.get("Destinatario"):
        recipients = []
        for dest in iterate(destinatarios):
            entry: dict[str, Any] = {}
            _set_opt(entry, "NumRegIdTrib", dest.get("NumRegIdTrib") and str(dest["NumRegIdTrib"]))
            _set_opt(entry, "Name", dest.get("Nombre") and str(dest["Nombre"]))
            addresses = [
                addr
                for d in iterate(dest.get("Domicilio"))
                if (addr := _map_foreign_trade_address(d))
            ]
            if addresses:
                entry["Address"] = addresses
            recipients.append(entry)
        mapped["Recipient"] = recipients

    commodities = []
    for merc in iterate(cce.get("Mercancias") or cce.get("Mercancia")):
        # after create(): Mercancias may be list; key is Mercancias holding Sequence
        commodity: dict[str, Any] = {
            "IdentificationNumber": str(merc["NoIdentificacion"]),
            "ValueInDolar": _num(merc["ValorDolares"]),
        }
        _set_opt(commodity, "TariffFraction", _code_str(merc.get("FraccionArancelaria")))
        if merc.get("CantidadAduana") is not None:
            commodity["CustomsQuantity"] = str(_num(merc["CantidadAduana"]))
        _set_opt(commodity, "CustomsUnit", _code_str(merc.get("UnidadAduana")))
        if merc.get("ValorUnitarioAduana") is not None:
            commodity["CustomsUnitValue"] = _num(merc["ValorUnitarioAduana"])
        if specs := merc.get("DescripcionesEspecificas"):
            commodity["SpecificDescriptions"] = [
                {
                    "Brand": str(s["Marca"]),
                    **(
                        {"Model": str(s["Modelo"])}
                        if s.get("Modelo") is not None
                        else {}
                    ),
                    **(
                        {"SubModel": str(s["SubModelo"])}
                        if s.get("SubModelo") is not None
                        else {}
                    ),
                    **(
                        {"SerialNumber": str(s["NumeroSerie"])}
                        if s.get("NumeroSerie") is not None
                        else {}
                    ),
                }
                for s in iterate(specs)
            ]
        commodities.append(commodity)
    if commodities:
        mapped["Commodity"] = commodities
    return mapped


def _apply_item_complements(
    cfdi: CFDI,
    payload: dict,
    *,
    allow_foreign_trade: bool = False,
) -> None:
    complemento_out: dict[str, Any] = {}

    if carta := _complement_node(cfdi, "CartaPorte"):
        payload["NameId"] = _CARTA_PORTE_NAME_ID
        complemento_out["CartaPorte31"] = _map_carta_porte(carta)

    if donat := _complement_node(cfdi, "Donatarias"):
        payload["NameId"] = _DONATION_NAME_ID
        complemento_out["Donation"] = _map_donation(donat)

    if leyendas := _complement_node(cfdi, "LeyendasFiscales"):
        complemento_out["TaxLegends"] = _map_tax_legends(leyendas)

    if implocal := _complement_node(cfdi, "ImpuestosLocales"):
        _apply_local_taxes_to_items(payload["Items"], implocal)

    if cce := _complement_node(cfdi, "ComercioExterior"):
        if not allow_foreign_trade:
            raise NotImplementedError(
                "Facturama Multiemisor does not support Comercio Exterior; "
                "use FacturamaWeb (API Web)."
            )
        payload["NameId"] = _FOREIGN_TRADE_NAME_ID
        complemento_out["ForeignTrade"] = _map_foreign_trade(cce)

    if complemento_out:
        payload["Complemento"] = complemento_out

    complemento = cfdi.get("Complemento") or {}
    if isinstance(complemento, Mapping) and not _is_known_item_complement_body(complemento):
        unsupported = {k for k in complemento if k not in _ITEM_COMPLEMENT_KEYS}
        if unsupported:
            raise NotImplementedError(
                f"Unsupported Complemento nodes for item CFDI mapper: {sorted(unsupported)}"
            )


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
    if num_reg := receptor.get("NumRegIdTrib"):
        payload["Receiver"]["TaxRegistrationNumber"] = str(num_reg)
    if residencia := receptor.get("ResidenciaFiscal"):
        payload["Receiver"]["TaxResidence"] = _code_str(residencia)
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


def cfdi_to_facturama_payload(
    cfdi: CFDI,
    *,
    allow_foreign_trade: bool = False,
) -> dict:
    """Map a satcfdi CFDI (typically unsigned) to Facturama JSON.

    :param allow_foreign_trade: Enable Comercio Exterior mapping (API Web only).
    """
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
        _apply_item_complements(
            cfdi,
            payload,
            allow_foreign_trade=allow_foreign_trade,
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

    Comercio exterior is not available on Multiemisor; use :class:`FacturamaWeb`.

    Documentation: https://apisandbox.facturama.mx/guias/api-multi/proceso-facturacion
    """

    # Facturama aggregates multiple PACs; no single PAC RFC applies.
    RFC = None
    _issue_path = "api-lite/3/cfdis"
    _download_type = "issuedLite"
    _cancel_path_prefix = "api-lite/cfdis"
    _list_path = "api-lite/cfdis"
    _allow_foreign_trade = False

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
            f"api/Cfdi/{fmt}/{self._download_type}/{document_id}",
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
        """List CFDIs (optionally filtered by keyword / UUID)."""
        params = {"status": status}
        if keyword:
            params["keyword"] = keyword
        if self._list_path == "api/Cfdi":
            params["type"] = "issued"
        results = self._request("get", self._list_path, params=params)
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
        Seal and stamp via Facturama.

        The local CFDI does not need to be signed; Facturama seals with the
        uploaded CSD (Multiemisor) or account fiscal profile (API Web).
        """
        payload = cfdi_to_facturama_payload(
            cfdi,
            allow_foreign_trade=self._allow_foreign_trade,
        )
        created = self._request("post", self._issue_path, json=payload)
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
            "Facturama does not stamp pre-signed XML; use issue() "
            "(Facturama seals and stamps from the mapped JSON payload)."
        )

    def recover(self, document_id: str, accept: Accept = Accept.XML) -> Document:
        xml = self._download_file(document_id, "xml") if accept & Accept.XML else None
        pdf = self._download_file(document_id, "pdf") if accept & Accept.PDF else None
        return Document(document_id=document_id, xml=xml, pdf=pdf)

    def recover_by_uuid(self, uuid: str, accept: Accept = Accept.XML) -> Document:
        return self.recover(self.find_id_by_uuid(uuid), accept=accept)

    def send_email(self, document_id: str, email: str, *, cfdi_type: str | None = None) -> dict | None:
        """Send a stamped CFDI by email through Facturama."""
        cfdi_type = cfdi_type or (
            "issuedLite" if self._download_type == "issuedLite" else "issued"
        )
        return self._request(
            "post",
            "api/Cfdi",
            params={
                "cfdiType": cfdi_type,
                "cfdiId": document_id,
                "email": email,
            },
        )

    def cancel(
        self,
        cfdi: CFDI,
        reason: CancelReason,
        substitution_id: str = None,
        signer: Signer = None,
        document_id: str = None,
    ) -> CancelationAcknowledgment:
        """
        Cancel a Facturama CFDI.

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
        if self._cancel_path_prefix == "api/Cfdi":
            params["type"] = "issued"

        res = self._request(
            "delete",
            f"{self._cancel_path_prefix}/{facturama_id}",
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


class FacturamaWeb(Facturama):
    """
    Facturama API Web adapter (single-issuer account fiscal profile).

    Unlike Multiemisor, API Web does not require per-RFC CSD upload via
    :meth:`upload_csd` (CSD lives on the Facturama account). It is also the
    only Facturama mode that supports Comercio Exterior.

    Documentation: https://apisandbox.facturama.mx/guias/api-web/cfdi/factura
    """

    _issue_path = "api/3/cfdis"
    _download_type = "issued"
    _cancel_path_prefix = "api/Cfdi"
    _list_path = "api/Cfdi"
    _allow_foreign_trade = True

    def upload_csd(self, rfc: str, certificate: bytes, key: bytes, password: str | bytes) -> dict:
        raise NotImplementedError(
            "FacturamaWeb uses the account fiscal profile CSD; "
            "upload certificates in the Facturama web UI, or use Facturama Multiemisor."
        )

    def delete_csd(self, rfc: str) -> None:
        raise NotImplementedError(
            "FacturamaWeb uses the account fiscal profile CSD; "
            "manage certificates in the Facturama web UI."
        )

    def get_csd(self, rfc: str) -> dict:
        raise NotImplementedError(
            "FacturamaWeb uses the account fiscal profile CSD; "
            "manage certificates in the Facturama web UI."
        )
