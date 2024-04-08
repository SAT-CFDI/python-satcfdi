import os
from typing import Sequence

from satcfdi.create.contabilidad.AuxiliarCtas13 import AuxiliarCtas, Cuenta, DetalleAux
from satcfdi.create.contabilidad.BCE13 import Balanza
from satcfdi.create.contabilidad.PLZ13 import Polizas, CompNal, Poliza
from satcfdi.create.contabilidad.RepAux13 import RepAuxFol, DetAuxFol
from satcfdi.create.contabilidad.catalogocuentas13 import Catalogo, Ctas
from .contabilidad_print import imprimir_contablidad

from .. import render

from ..models import DatePeriod


def filename(file):
    if file.tag == '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/BalanzaComprobacion}Balanza':
        return file["RFC"] + str(file["Anio"]) + file["Mes"] + "B" + file["TipoEnvio"] + ".xml"
    if file.tag == '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/CatalogoCuentas}Catalogo':
        return file["RFC"] + str(file["Anio"]) + file["Mes"] + "CT.xml"
    if file.tag == '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarCtas}AuxiliarCtas':
        return file["RFC"] + str(file["Anio"]) + file["Mes"] + "XC.xml"
    if file.tag == '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}Polizas':
        return file["RFC"] + str(file["Anio"]) + file["Mes"] + "PL.xml"
    if file.tag == '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios}RepAuxFol':
        return file["RFC"] + str(file["Anio"]) + file["Mes"] + "XF.xml"
    raise ValueError(f"Unknown file type: {file.tag}")


def output_file(file, folder, fiel=None, generate_pdf=False):
    if fiel:
        file.sign(fiel)

    output_file = os.path.join(folder, filename(file))
    file.xml_write(
        output_file,
        pretty_print=True,
        xml_declaration=True
    )
    if generate_pdf:
        # render.html_write(file, output_file[:-4] + ".html")
        render.pdf_write(file, output_file[:-4] + ".pdf")
    else:
        # delete file
        try:
            os.remove(output_file[:-4] + ".pdf")
        except FileNotFoundError:
            pass

    return output_file


def calcular_saldos(cuentas, polizas):
    for c in cuentas.values():
        # c['SaldoIni'] = 0
        c['Debe'] = 0
        c['Haber'] = 0
        c['SaldoFin'] = 0

    for p in polizas:
        for t in p["Transaccion"]:
            num_cta = t["NumCta"]
            cuenta = cuentas[num_cta]
            cuenta["Debe"] += t["Debe"]
            cuenta["Haber"] += t["Haber"]

    # Fill Parents
    for level in range(4, 1, -1):
        for k, v in cuentas.items():
            if v['Nivel'] == level:
                parent = v['SubCtaDe']
                if parent:
                    p_cuenta = cuentas[parent]
                    p_cuenta['Debe'] += v['Debe']
                    p_cuenta['Haber'] += v['Haber']

    # Fill SaldoFin
    for c in cuentas.values():
        if c["Natur"] == "D":
            c["SaldoFin"] += c["SaldoIni"] + c["Debe"] - c["Haber"]
        else:
            c["SaldoFin"] += c["SaldoIni"] + c["Haber"] - c["Debe"]


def generar_contabilidad(
        dp: DatePeriod,
        rfc_emisor: str,
        cuentas: dict,
        polizas: Sequence[Poliza],
        tipo_envio='N',
        fecha_mod_bal=None,
        tipo_solicitud='',
        numero_orden=None,
        numero_tramite=None,
        folder=None,
        fiel=None,
        generate_pdf=False):
    calcular_saldos(cuentas, polizas)

    plz = Polizas(
        rfc=rfc_emisor,
        mes=str(dp.month).zfill(2),
        anio=dp.year,
        tipo_solicitud=tipo_solicitud,
        num_orden=numero_orden,
        num_tramite=numero_tramite,
        poliza=polizas
    )
    output_file(plz, folder, fiel, generate_pdf=generate_pdf)

    cat = Catalogo(
        rfc=rfc_emisor,
        mes=str(dp.month).zfill(2),
        anio=dp.year,
        ctas=[
            Ctas(
                cod_agrup=v["CodAgrup"].split("_")[0],
                num_cta=k,
                desc=v["Desc"],
                nivel=v["Nivel"],
                natur=v["Natur"],
                sub_cta_de=v['SubCtaDe'],
            ) for k, v in cuentas.items()
        ]
    )
    output_file(cat, folder, fiel)

    ban = Balanza(
        rfc=rfc_emisor,
        mes=str(dp.month).zfill(2),
        anio=dp.year,
        tipo_envio=tipo_envio,
        fecha_mod_bal=fecha_mod_bal,
        ctas=[{
            "NumCta": k,
            **v,
        } for k, v in cuentas.items() if v["SaldoIni"] or v["Debe"] or v["Haber"] or v["SaldoFin"]],
    )
    output_file(ban, folder, fiel)

    aux_detalles = group_aux_cuentas(polizas)
    aux = AuxiliarCtas(
        rfc=rfc_emisor,
        mes=str(dp.month).zfill(2),
        anio=dp.year,
        tipo_solicitud=tipo_solicitud,
        num_orden=numero_orden,
        num_tramite=numero_tramite,
        cuenta=[
            Cuenta(
                num_cta=k,
                des_cta=v["Desc"],
                saldo_ini=v["SaldoIni"],
                saldo_fin=v["SaldoFin"],
                detalle_aux=aux_detalles[k]
            ) for k, v in cuentas.items() if k in aux_detalles
        ]
    )
    output_file(aux, folder, fiel, generate_pdf=generate_pdf)

    auxf = RepAuxFol(
        rfc=rfc_emisor,
        mes=str(dp.month).zfill(2),
        anio=dp.year,
        tipo_solicitud=tipo_solicitud,
        num_orden=numero_orden,
        num_tramite=numero_tramite,
        det_aux_fol=list(group_aux_folios(polizas))
    )
    output_file(auxf, folder, fiel, generate_pdf=generate_pdf)

    imprimir_contablidad(
        catalogo_cuentas=cat,
        balanza_comprobacion=ban,
        archivo_excel=os.path.join(folder, filename(ban)[:-4] + ".xlsx")
    )

    validate_saldos(cuentas)


def group_aux_cuentas(polizas):
    cta_polizas = {}
    for p in polizas:
        for t in p["Transaccion"]:
            detalles = cta_polizas.setdefault(t["NumCta"], [])
            detalles.append(
                DetalleAux(
                    fecha=p["Fecha"],
                    num_un_iden_pol=p["NumUnIdenPol"],
                    concepto=t["Concepto"],
                    debe=t["Debe"],
                    haber=t["Haber"],
                )
            )
    return cta_polizas


def group_aux_folios(polizas):
    for p in polizas:
        yield DetAuxFol(
            num_un_iden_pol=p["NumUnIdenPol"],
            fecha=p["Fecha"],
            compr_nal=p.comp_nal,
        )


def validate_saldos(cuentas):
    total = 0
    totales = {}
    for k, v in cuentas.items():
        if v['Nivel'] == 1:
            if v['Natur'] == 'D':
                total += v['SaldoFin']
            else:
                total -= v['SaldoFin']
        else:
            totales.setdefault(v['SubCtaDe'], 0)
            if v['Natur'] == 'D':
                totales[v['SubCtaDe']] += v['SaldoFin']
            else:
                totales[v['SubCtaDe']] -= v['SaldoFin']

    assert total == 0
    for k, v in totales.items():
        if cuentas[k]['Natur'] == 'D':
            assert v == cuentas[k]['SaldoFin']
        else:
            assert v == -cuentas[k]['SaldoFin']
