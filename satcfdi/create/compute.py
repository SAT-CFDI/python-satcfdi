from collections import defaultdict
from decimal import Decimal

from ..catalogs import moneda_decimales
from ..transform.helpers import strcode
from ..utils import iterate


def rounder(moneda):
    decimals = moneda_decimales(strcode(moneda))
    return lambda v: round(v, decimals)


def aggregate(sequence, keys: tuple, values: tuple, project=None) -> list:
    _res = defaultdict(lambda: tuple(None for _ in values))

    _keys = lambda obj: tuple(obj.get(i) for i in keys)
    _values = lambda obj: tuple(obj.get(i) for i in values)
    if callable(project):
        _project = tuple(project(i) for i in keys + values)
    else:
        _project = project or keys + values

    def add(t):
        a, b = t
        if a is None:
            return b
        if b is None:
            return a
        return a + b

    for dic in sequence:
        k = _keys(dic)
        _res[k] = tuple(add(t) for t in zip(_res[k], _values(dic)))

    return [
        dict(zip(_project, k + v))
        for k, v in _res.items()
    ]


def encode_impuesto(impuesto, tipo_factor, tasa_cuota: Decimal = None):
    impuesto = strcode(impuesto)
    if tipo_factor:
        impuesto += "|" + strcode(tipo_factor)
        if tasa_cuota is not None:
            impuesto += "|" + tasa_cuota.__format__(".6f")
    return impuesto


def make_impuesto(impuesto: dict, base, rnd_fn):
    _impuesto = impuesto["Impuesto"]
    tipo_factor = impuesto['TipoFactor']
    tasa_cuota = impuesto['TasaOCuota']
    if impuesto.get('Base') is not None:
        base = impuesto['Base']

    if impuesto.get('Importe') is not None:
        importe = impuesto['Importe']
    else:
        match tipo_factor:
            case "Tasa":
                importe = rnd_fn(base * tasa_cuota)
            case "Cuota":
                importe = tasa_cuota
            case "Exento":
                importe = None
            case _:
                raise ValueError("Invalid TipoFactor", tipo_factor)

    return {
        'Base': rnd_fn(base),
        'Impuesto': _impuesto,
        'TipoFactor': tipo_factor,
        'TasaOCuota': tasa_cuota,
        'Importe': importe
    }


def group_impuestos(elements, pfx="", ofx=""):
    retenciones = aggregate(
        (t for c in iterate(elements) for t in iterate((c[f"Impuestos{pfx}"] or {}).get(f"Retenciones{pfx}"))),
        keys=(f"Impuesto{pfx}",),
        values=(f"Importe{pfx}",),
        project=lambda i: i[:len(i) - len(pfx)] + ofx,
    )
    traslados = aggregate(
        (t for c in iterate(elements) for t in iterate((c[f"Impuestos{pfx}"] or {}).get(f"Traslados{pfx}"))),
        keys=(f"Impuesto{pfx}", f"TipoFactor{pfx}", f"TasaOCuota{pfx}"),
        values=(f"Base{pfx}", f"Importe{pfx}"),
        project=lambda i: i[:len(i) - len(pfx)] + ofx,
    )

    impuestos = {}
    if retenciones:
        impuestos[f"Retenciones{ofx}"] = retenciones

    if traslados:
        impuestos[f"Traslados{ofx}"] = traslados

    return impuestos


def make_impuestos(conceptos):
    impuestos = group_impuestos(conceptos)

    if retenciones := impuestos.get('Retenciones'):
        impuestos['Retenciones'] = retenciones
        imp = list(i["Importe"] for i in retenciones if i["Importe"] is not None)
        if imp:
            impuestos['TotalImpuestosRetenidos'] = sum(imp)

    if traslados := impuestos.get('Traslados'):
        impuestos['Traslados'] = traslados
        imp = list(i["Importe"] for i in traslados if i["Importe"] is not None)
        if imp:
            impuestos['TotalImpuestosTrasladados'] = sum(imp)

    return impuestos or None


def make_impuestos_dr(conceptos):
    impuestos = {}
    for imp_t in ("Retenciones", "Traslados"):
        imp = aggregate(
            (t for c in conceptos for t in iterate((c["Impuestos"] or {}).get(imp_t))),
            keys=("Impuesto", 'TipoFactor', "TasaOCuota"),
            values=("Base", "Importe"),
            project=lambda i: i + "DR",
        )

        if imp:
            impuestos[imp_t + 'DR'] = imp

    return impuestos or None


def calculate_partial(value, imp_saldo_ant, imp_pagado, total, rnd_fn):
    if value is None:
        return None

    p_tot_pagado = (total - imp_saldo_ant + imp_pagado) / total
    p_anterior = (total - imp_saldo_ant) / total

    return rnd_fn(value * p_tot_pagado) - rnd_fn(value * p_anterior)


def make_impuestos_dr_parcial(conceptos, imp_saldo_ant: Decimal, imp_pagado: Decimal, total: Decimal, rnd_fn):
    p_tot_pagado = (total - imp_saldo_ant + imp_pagado) / total
    p_anterior = (total - imp_saldo_ant) / total

    impuestos = make_impuestos_dr(conceptos)
    for imp_t in ("RetencionesDR", "TrasladosDR"):
        for t in impuestos.get(imp_t, []):
            if t["ImporteDR"] is not None:
                t["ImporteDR"] = rnd_fn(t["ImporteDR"] * p_tot_pagado) - rnd_fn(t["ImporteDR"] * p_anterior)
            t["BaseDR"] = rnd_fn(t["BaseDR"] * p_tot_pagado) - rnd_fn(t["BaseDR"] * p_anterior)

    return impuestos


def make_impuestos_p(documentos):
    impuestos = group_impuestos(documentos, pfx="DR", ofx="P")
    return impuestos or None


RETENCIONES_MAP = {
    '001': 'TotalRetencionesISR',
    "002": 'TotalRetencionesIVA',
    '003': 'TotalRetencionesIEPS'
}


def make_pago_totales(pagos):
    impuestos = defaultdict(lambda: 0)

    for p in iterate(pagos):
        tipo_cambio = p.get('TipoCambioP', 1)
        impuestos['MontoTotalPagos'] += p['Monto'] * tipo_cambio

        for retencion in iterate((p["ImpuestosP"] or {}).get("RetencionesP")):
            impuestos[RETENCIONES_MAP[retencion["ImpuestoP"]]] += retencion["ImporteP"] * tipo_cambio

        for traslado in iterate((p["ImpuestosP"] or {}).get("TrasladosP")):
            match (traslado["ImpuestoP"], traslado["TipoFactorP"], "{:.6f}".format(traslado["TasaOCuotaP"] or -1)):
                case ("002", "Tasa", "0.160000"):
                    impuestos['TotalTrasladosBaseIVA16'] += traslado["BaseP"] * tipo_cambio
                    impuestos['TotalTrasladosImpuestoIVA16'] += traslado["ImporteP"] * tipo_cambio
                case ("002", "Tasa", "0.080000"):
                    impuestos['TotalTrasladosBaseIVA8'] += traslado["BaseP"] * tipo_cambio
                    impuestos['TotalTrasladosImpuestoIVA8'] += traslado["ImporteP"] * tipo_cambio
                case ("002", "Tasa", "0.000000"):
                    impuestos['TotalTrasladosBaseIVA0'] += traslado["BaseP"] * tipo_cambio
                    impuestos['TotalTrasladosImpuestoIVA0'] += traslado["ImporteP"] * tipo_cambio
                case ("002", "Tasa", _):
                    raise ValueError("Unknown Impuesto")
                case ("002", "Exento", _):
                    impuestos['TotalTrasladosBaseIVAExento'] += traslado["BaseP"] * tipo_cambio

    return impuestos
