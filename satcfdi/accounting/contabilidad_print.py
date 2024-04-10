import xlsxwriter
from satcfdi.accounting.process import excel_export
from satcfdi.cfdi import CFDI

EXCEL_COLUMNS = {
    'NumCta': (12, False, lambda i: i['NumCta']),
    'Desc': (62, False, lambda i: '    ' * (i['Nivel'] - 1) + i['Desc']),
    'Natur': (5, False, lambda i: i['Natur']),

    'SaldoIni': (12, False, lambda i: i.get('SaldoIni')),
    'Debe': (12, False, lambda i: i.get('Debe')),
    'Haber': (12, False, lambda i: i.get('Haber')),
    'SaldoFin': (12, False, lambda i: i.get('SaldoFin')),

    'CodAgrup': (12, False, lambda i: i['CodAgrup'].code),
    'CodDesc': (120, False, lambda i: i['CodAgrup'].description),
}


def imprimir_contablidad(
        catalogo_cuentas,
        balanza_comprobacion,
        archivo_excel
):
    ct = catalogo_cuentas
    bc = balanza_comprobacion

    ctas = {
        c['NumCta']: {
            'Desc': c['Desc'],
            'Natur': c['Natur'],
            'CodAgrup': c['CodAgrup'],
            'Nivel': c['Nivel'],
        }
        for c in ct['Ctas']
    }
    for r in bc['Ctas']:
        ctv = ctas[r['NumCta']]
        r.update(ctv)

    workbook = xlsxwriter.Workbook(archivo_excel)
    excel_export(
        workbook=workbook,
        name=bc['RFC'] + str(bc['Anio']) + str(bc['Mes']),
        invoices=bc['Ctas'],
        columns=EXCEL_COLUMNS,
        row_height=1
    )
    workbook.close()
