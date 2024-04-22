import os
from typing import Sequence

from satcfdi.zip import zip_create, ZipData, zip_file

from satcfdi.catalogs import select, catalog_code

from satcfdi.utils import iterate

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


def output_file(file, folder, fiel=None, generate_pdf=False, zip_xml=False):
    if fiel:
        file.sign(fiel)

    output_file = os.path.join(folder, filename(file))
    if zip_xml:
        zip_file(output_file[:-4] + '.zip', [
            ZipData(
                filename(file),
                file.xml_bytes()
            )
        ])
    else:
        file.xml_write(
            output_file,
            pretty_print=True
        )

    if generate_pdf:
        render.pdf_write(file, output_file[:-4] + ".pdf")
    else:
        try:
            os.remove(output_file[:-4] + ".pdf")
        except FileNotFoundError:
            pass

    return output_file


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
        generate_pdf=False,
        zip_xml=False
):
    validate_cuentas(cuentas)
    validate_polizas(polizas)
    calcular_saldos(cuentas, polizas)

    plz = Polizas(
        rfc=rfc_emisor,
        mes="{:02d}".format(dp.month),
        anio=dp.year,
        tipo_solicitud=tipo_solicitud,
        num_orden=numero_orden,
        num_tramite=numero_tramite,
        poliza=polizas
    )
    output_file(plz, folder, fiel, generate_pdf=generate_pdf, zip_xml=zip_xml)

    cat = Catalogo(
        rfc=rfc_emisor,
        mes="{:02d}".format(dp.month),
        anio=dp.year,
        ctas=[
            Ctas(
                cod_agrup=v["CodAgrup"],
                num_cta=k,
                desc=v["Desc"],
                nivel=v["Nivel"],
                natur=v["Natur"],
                sub_cta_de=v['SubCtaDe'],
            ) for k, v in cuentas.items()
        ]
    )
    output_file(cat, folder, fiel, zip_xml=zip_xml)

    ban = Balanza(
        rfc=rfc_emisor,
        mes="{:02d}".format(dp.month),
        anio=dp.year,
        tipo_envio=tipo_envio,
        fecha_mod_bal=fecha_mod_bal,
        ctas=[{
            "NumCta": k,
            **v,
        } for k, v in cuentas.items() if v["SaldoIni"] or v["Debe"] or v["Haber"] or v["SaldoFin"]],
    )
    output_file(ban, folder, fiel, zip_xml=zip_xml)

    aux_detalles = group_aux_cuentas(polizas)
    aux = AuxiliarCtas(
        rfc=rfc_emisor,
        mes="{:02d}".format(dp.month),
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
    output_file(aux, folder, fiel, generate_pdf=generate_pdf, zip_xml=zip_xml)

    auxf = RepAuxFol(
        rfc=rfc_emisor,
        mes="{:02d}".format(dp.month),
        anio=dp.year,
        tipo_solicitud=tipo_solicitud,
        num_orden=numero_orden,
        num_tramite=numero_tramite,
        det_aux_fol=list(group_aux_folios(polizas))
    )
    output_file(auxf, folder, fiel, generate_pdf=generate_pdf, zip_xml=zip_xml)

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
                    concepto=p["Concepto"] + " " + t["Concepto"],
                    debe=t["Debe"],
                    haber=t["Haber"],
                )
            )
    return cta_polizas


def group_aux_folios(polizas):
    for p in polizas:
        compr_nal = []
        compr_nal_otr = []
        compr_ext = []

        for t in p["Transaccion"]:
            if c := t.get('CompNal'):
                for c in iterate(c):
                    if c not in compr_nal:
                        compr_nal.append(c)
            if c := t.get('CompNalOtr'):
                for c in iterate(c):
                    if c not in compr_nal_otr:
                        compr_nal_otr.append(c)
            if c := t.get('CompExt'):
                for c in iterate(c):
                    if c not in compr_ext:
                        compr_ext.append(c)

        yield DetAuxFol(
            num_un_iden_pol=p["NumUnIdenPol"],
            fecha=p["Fecha"],
            compr_nal=compr_nal,
            compr_nal_otr=compr_nal_otr,
            compr_ext=compr_ext,
        )


def validate_cuentas(cuentas):
    # validar cuentas
    for k, v in cuentas.items():
        assert k
        v['_Lowest'] = True
        assert v['Natur'] in ['A', 'D']
        if v['SubCtaDe']:
            assert v['SubCtaDe'] in cuentas, f"Parent account {v['SubCtaDe']} not found for {k}"
            v['Nivel'] = cuentas[v['SubCtaDe']]['Nivel'] + 1
        else:
            v['Nivel'] = 1

        if isinstance(v['CodAgrup'], str):
            v['CodAgrup'] = catalog_code('Cb9f_c_CodAgrup', v['CodAgrup'])
            assert v['CodAgrup'].description, f"Unknown CodAgrup: {v['CodAgrup']}"

    for k, v in cuentas.items():
        if v['SubCtaDe']:
            cuentas[v['SubCtaDe']]['_Lowest'] = False


def sign(cta):
    if cta['Natur'] == 'D':
        return 1
    return -1


def validate_saldos(cuentas):
    totales = {}
    for k, v in cuentas.items():
        sub_cta = v.get('SubCtaDe')
        totales.setdefault(sub_cta, 0)
        totales[sub_cta] += v['SaldoFin'] * sign(v)

    for k, v in totales.items():
        if k:
            if v != cuentas[k]['SaldoFin'] * sign(cuentas[k]):
                raise ValueError(f"Error in {k}: {v} != {cuentas[k]['SaldoFin']}")
        else:
            assert v == 0


def validate_polizas(polizas):
    num_un = set()
    for p in polizas:
        u = p['NumUnIdenPol']
        if u in num_un:
            raise ValueError(f"Repeated NumUnIdenPol: {u}")
        num_un.add(u)


def calcular_saldos(cuentas, polizas):
    max_level = 1
    for c in cuentas.values():
        # c['SaldoIni'] = 0
        c['Debe'] = 0
        c['Haber'] = 0
        c['SaldoFin'] = 0
        max_level = max(max_level, c['Nivel'])

    for p in polizas:
        for t in p["Transaccion"]:
            num_cta = t["NumCta"]
            cuenta = cuentas[num_cta]
            t['DesCta'] = cuenta['Desc']
            assert cuenta["_Lowest"], f"Account {num_cta} is not a lowest level account"
            cuenta["Debe"] += t["Debe"]
            cuenta["Haber"] += t["Haber"]

    # Fill Parents
    for level in range(max_level, 1, -1):
        for k, v in cuentas.items():
            if v['Nivel'] == level:
                parent = v['SubCtaDe']
                if parent:
                    p_cuenta = cuentas[parent]
                    p_cuenta['Debe'] += v['Debe']
                    p_cuenta['Haber'] += v['Haber']

    # Fill SaldoFin
    for c in cuentas.values():
        s = sign(c)
        c["SaldoFin"] += c["SaldoIni"] + c["Debe"] * s - c["Haber"] * s
