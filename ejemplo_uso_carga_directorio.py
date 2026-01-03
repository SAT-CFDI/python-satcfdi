#!/usr/bin/env python3
"""
EJEMPLO DE USO: Cargar CFDIs desde directorio y generar reportes

Este script muestra ejemplos prácticos de cómo usar la función
cargar_cfdis_desde_directorio() para diferentes casos de uso.
"""

from datetime import date, datetime
import xlsxwriter
from cargar_cfdis_desde_directorio import (
    cargar_cfdis_desde_directorio,
    filtrar_por_fecha,
    mostrar_resumen
)
from satcfdi.accounting import (
    complement_invoices_data,
    filter_invoices_iter,
    filter_payments_iter,
    invoices_export,
    payments_export,
    invoices_print
)
from satcfdi.create.cfd.catalogos import TipoDeComprobante


# ==============================================================================
# CASO 1: Cargar todas las facturas de una carpeta
# ==============================================================================

def caso1_cargar_todo():
    """
    Carga todos los CFDIs de una carpeta y subcarpetas.
    """
    print("=" * 80)
    print("CASO 1: Cargar todas las facturas de una carpeta")
    print("=" * 80)

    # Cargar CFDIs
    invoices_dict, stats = cargar_cfdis_desde_directorio(
        directorio_base='/home/usuario/facturas',
        recursivo=True,  # Buscar en subcarpetas
        mostrar_progreso=True
    )

    # Mostrar resumen
    mostrar_resumen(invoices_dict)

    # Complementar datos
    complement_invoices_data(invoices_dict)

    print(f"✓ Cargados {stats['cargados']} CFDIs listos para usar\n")

    return invoices_dict


# ==============================================================================
# CASO 2: Cargar solo facturas de un mes específico
# ==============================================================================

def caso2_cargar_mes_especifico():
    """
    Carga CFDIs y filtra por mes.
    """
    print("=" * 80)
    print("CASO 2: Reportes de un mes específico")
    print("=" * 80)

    # Cargar todos los CFDIs
    invoices_dict, _ = cargar_cfdis_desde_directorio(
        directorio_base='/home/usuario/facturas/2024',
        recursivo=True
    )

    # Filtrar por mes (Enero 2024)
    facturas_enero = filtrar_por_fecha(
        invoices_dict,
        fecha_inicio=date(2024, 1, 1),
        fecha_fin=date(2024, 1, 31)
    )

    print(f"\n✓ Facturas de enero 2024: {len(facturas_enero)}")

    # Complementar datos
    complement_invoices_data(facturas_enero)

    # Generar reporte
    facturas = list(filter_invoices_iter(
        facturas_enero.values(),
        invoice_type=TipoDeComprobante.INGRESO
    ))

    if facturas:
        print(f"  • Facturas de ingreso: {len(facturas)}")
        total = sum(f['Total'] for f in facturas)
        print(f"  • Total facturado: ${total:,.2f}")

    return facturas_enero


# ==============================================================================
# CASO 3: Exportar reporte de cuentas por cobrar
# ==============================================================================

def caso3_reporte_cuentas_por_cobrar():
    """
    Genera reporte de cuentas por cobrar.
    """
    print("=" * 80)
    print("CASO 3: Reporte de cuentas por cobrar")
    print("=" * 80)

    # Cargar CFDIs
    invoices_dict, _ = cargar_cfdis_desde_directorio(
        directorio_base='/home/usuario/facturas',
        recursivo=True
    )

    complement_invoices_data(invoices_dict)

    # Filtrar facturas con saldo pendiente
    facturas_pendientes = list(filter_invoices_iter(
        invoices_dict.values(),
        invoice_type=TipoDeComprobante.INGRESO,
        pending_balance=lambda x: x is not None and x > 0
    ))

    print(f"\n✓ Facturas pendientes de cobro: {len(facturas_pendientes)}")

    if facturas_pendientes:
        # Calcular totales
        total_por_cobrar = sum(f.saldo_pendiente() for f in facturas_pendientes)
        print(f"  • Total por cobrar: ${total_por_cobrar:,.2f}")

        # Agrupar por cliente
        print("\n  Detalle por cliente:")
        clientes = {}
        for f in facturas_pendientes:
            rfc = f['Receptor']['Rfc']
            if rfc not in clientes:
                clientes[rfc] = {
                    'nombre': f['Receptor'].get('Nombre', 'Sin nombre'),
                    'facturas': 0,
                    'saldo': 0
                }
            clientes[rfc]['facturas'] += 1
            clientes[rfc]['saldo'] += f.saldo_pendiente()

        # Mostrar top 5
        top_clientes = sorted(
            clientes.items(),
            key=lambda x: x[1]['saldo'],
            reverse=True
        )[:5]

        for rfc, info in top_clientes:
            print(f"    • {rfc} ({info['nombre']})")
            print(f"      {info['facturas']} facturas - ${info['saldo']:,.2f}")

        # Exportar a Excel
        archivo = f"cuentas_por_cobrar_{datetime.now().strftime('%Y%m%d')}.xlsx"
        workbook = xlsxwriter.Workbook(archivo)
        invoices_export(workbook, 'Pendientes', facturas_pendientes)
        workbook.close()

        print(f"\n✓ Reporte exportado a: {archivo}")

    return facturas_pendientes


# ==============================================================================
# CASO 4: Análisis de pagos recibidos por período
# ==============================================================================

def caso4_analisis_pagos():
    """
    Analiza pagos recibidos en un período.
    """
    print("=" * 80)
    print("CASO 4: Análisis de pagos recibidos")
    print("=" * 80)

    # Cargar CFDIs
    invoices_dict, _ = cargar_cfdis_desde_directorio(
        directorio_base='/home/usuario/facturas',
        recursivo=True
    )

    complement_invoices_data(invoices_dict)

    # Filtrar pagos de un período
    def es_febrero_2024(fecha):
        if isinstance(fecha, datetime):
            return fecha.year == 2024 and fecha.month == 2
        return False

    pagos_febrero = list(filter_payments_iter(
        invoices_dict,
        fecha=es_febrero_2024
    ))

    print(f"\n✓ Pagos recibidos en febrero 2024: {len(pagos_febrero)}")

    if pagos_febrero:
        # Calcular total cobrado
        total_cobrado = sum(p.total for p in pagos_febrero)
        print(f"  • Total cobrado: ${total_cobrado:,.2f}")

        # Contar por forma de pago
        formas_pago = {}
        for p in pagos_febrero:
            if p.pago:
                forma = str(p.pago.get('FormaDePagoP', 'No especificado'))
            else:
                forma = str(p.comprobante.get('FormaPago', 'No especificado'))

            formas_pago[forma] = formas_pago.get(forma, 0) + 1

        print("\n  Distribución por forma de pago:")
        for forma, cantidad in sorted(formas_pago.items()):
            print(f"    • {forma}: {cantidad} pagos")

        # Exportar
        archivo = f"pagos_febrero_2024.xlsx"
        workbook = xlsxwriter.Workbook(archivo)
        payments_export(workbook, 'Pagos Febrero', pagos_febrero)
        workbook.close()

        print(f"\n✓ Reporte exportado a: {archivo}")

    return pagos_febrero


# ==============================================================================
# CASO 5: Cargar solo un tipo de directorio (no recursivo)
# ==============================================================================

def caso5_cargar_no_recursivo():
    """
    Carga CFDIs solo del directorio actual, sin subcarpetas.
    """
    print("=" * 80)
    print("CASO 5: Cargar solo directorio actual (sin subcarpetas)")
    print("=" * 80)

    # Cargar sin recursión
    invoices_dict, stats = cargar_cfdis_desde_directorio(
        directorio_base='/home/usuario/facturas/enero',
        recursivo=False,  # NO buscar en subcarpetas
        mostrar_progreso=False
    )

    print(f"\n✓ Cargados {stats['cargados']} CFDIs del directorio actual")

    return invoices_dict


# ==============================================================================
# CASO 6: Procesamiento por lotes (grandes volúmenes)
# ==============================================================================

def caso6_procesamiento_lotes():
    """
    Procesa grandes volúmenes de CFDIs por lotes.
    """
    print("=" * 80)
    print("CASO 6: Procesamiento por lotes (grandes volúmenes)")
    print("=" * 80)

    import os

    base_dir = '/home/usuario/facturas/2024'

    # Obtener lista de subdirectorios (por mes)
    meses = []
    for item in os.listdir(base_dir):
        ruta = os.path.join(base_dir, item)
        if os.path.isdir(ruta):
            meses.append(ruta)

    print(f"\n✓ Encontrados {len(meses)} subdirectorios (meses)")

    # Procesar cada mes por separado
    reportes = []

    for mes_dir in sorted(meses):
        mes_nombre = os.path.basename(mes_dir)
        print(f"\n  Procesando {mes_nombre}...")

        # Cargar CFDIs del mes
        invoices_mes, stats = cargar_cfdis_desde_directorio(
            directorio_base=mes_dir,
            recursivo=False,
            mostrar_progreso=False
        )

        if stats['cargados'] > 0:
            complement_invoices_data(invoices_mes)

            # Generar estadísticas
            facturas = list(filter_invoices_iter(
                invoices_mes.values(),
                invoice_type=TipoDeComprobante.INGRESO
            ))

            total = sum(f['Total'] for f in facturas) if facturas else 0

            reportes.append({
                'mes': mes_nombre,
                'cantidad': len(facturas),
                'total': total
            })

            print(f"    • Facturas: {len(facturas)}")
            print(f"    • Total: ${total:,.2f}")

    # Resumen consolidado
    print("\n" + "-" * 80)
    print("RESUMEN CONSOLIDADO:")
    total_general = sum(r['total'] for r in reportes)
    total_facturas = sum(r['cantidad'] for r in reportes)

    print(f"  • Total de facturas: {total_facturas}")
    print(f"  • Total facturado: ${total_general:,.2f}")

    return reportes


# ==============================================================================
# CASO 7: Validar integridad de directorio
# ==============================================================================

def caso7_validar_integridad():
    """
    Valida la integridad de los XMLs en un directorio.
    """
    print("=" * 80)
    print("CASO 7: Validar integridad de archivos XML")
    print("=" * 80)

    # Cargar con detalle de errores
    invoices_dict, stats = cargar_cfdis_desde_directorio(
        directorio_base='/home/usuario/facturas',
        recursivo=True,
        detener_en_error=False  # Continuar aunque haya errores
    )

    print("\n✓ RESULTADOS DE VALIDACIÓN:")
    print(f"  • Archivos válidos: {stats['cargados']}")
    print(f"  • Archivos con error: {stats['errores']}")
    print(f"  • Sin timbre fiscal: {stats['sin_timbre']}")
    print(f"  • UUIDs duplicados: {stats['duplicados']}")

    # Mostrar archivos con error
    if stats['archivos_error']:
        print("\n  Archivos con error:")
        for error_info in stats['archivos_error'][:5]:  # Mostrar primeros 5
            print(f"    • {error_info['archivo']}")
            print(f"      Error: {error_info['error']}")

        if len(stats['archivos_error']) > 5:
            print(f"    ... y {len(stats['archivos_error']) - 5} más")

    return stats


# ==============================================================================
# EJEMPLO DE USO COMBINADO
# ==============================================================================

def ejemplo_completo():
    """
    Ejemplo que combina varios casos de uso.
    """
    print("=" * 80)
    print("EJEMPLO COMPLETO: Proceso de fin de mes")
    print("=" * 80)

    # 1. Cargar todas las facturas del mes
    print("\n1. Cargando facturas del mes...")
    invoices_dict, stats = cargar_cfdis_desde_directorio(
        directorio_base='/home/usuario/facturas/2024/01',
        recursivo=True
    )

    if stats['cargados'] == 0:
        print("No se encontraron facturas.")
        return

    # 2. Complementar datos
    print("\n2. Procesando relaciones y pagos...")
    complement_invoices_data(invoices_dict)

    # 3. Generar reportes
    print("\n3. Generando reportes...")

    # Facturas emitidas
    facturas_emitidas = list(filter_invoices_iter(
        invoices_dict.values(),
        invoice_type=TipoDeComprobante.INGRESO
    ))

    # Pagos recibidos
    pagos_recibidos = list(filter_payments_iter(invoices_dict))

    # Pendientes de cobro
    pendientes = list(filter_invoices_iter(
        invoices_dict.values(),
        invoice_type=TipoDeComprobante.INGRESO,
        pending_balance=lambda x: x is not None and x > 0
    ))

    # 4. Calcular totales
    total_emitido = sum(f['Total'] for f in facturas_emitidas)
    total_cobrado = sum(p.total for p in pagos_recibidos)
    total_pendiente = sum(f.saldo_pendiente() for f in pendientes)

    # 5. Mostrar resumen
    print("\n" + "=" * 80)
    print("RESUMEN DEL MES")
    print("=" * 80)
    print(f"\n📊 Facturas emitidas: {len(facturas_emitidas)}")
    print(f"   Total: ${total_emitido:,.2f}")
    print(f"\n💰 Pagos recibidos: {len(pagos_recibidos)}")
    print(f"   Total: ${total_cobrado:,.2f}")
    print(f"\n⏳ Pendientes de cobro: {len(pendientes)}")
    print(f"   Total: ${total_pendiente:,.2f}")

    # 6. Exportar a Excel
    print("\n4. Exportando a Excel...")
    archivo = f"reporte_mensual_{datetime.now().strftime('%Y%m')}.xlsx"
    workbook = xlsxwriter.Workbook(archivo)

    if facturas_emitidas:
        invoices_export(workbook, 'Facturas Emitidas', facturas_emitidas)

    if pagos_recibidos:
        payments_export(workbook, 'Pagos Recibidos', pagos_recibidos)

    if pendientes:
        invoices_export(workbook, 'Por Cobrar', pendientes)

    workbook.close()
    print(f"   ✓ Reporte generado: {archivo}")

    print("\n" + "=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "EJEMPLOS DE USO - Carga de CFDIs" + " " * 24 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    print("Este archivo contiene 7 casos de uso diferentes.")
    print("Descomenta el caso que deseas ejecutar:\n")

    print("  • caso1_cargar_todo() - Cargar todas las facturas")
    print("  • caso2_cargar_mes_especifico() - Filtrar por mes")
    print("  • caso3_reporte_cuentas_por_cobrar() - Cuentas por cobrar")
    print("  • caso4_analisis_pagos() - Análisis de pagos")
    print("  • caso5_cargar_no_recursivo() - Sin subcarpetas")
    print("  • caso6_procesamiento_lotes() - Grandes volúmenes")
    print("  • caso7_validar_integridad() - Validar archivos")
    print("  • ejemplo_completo() - Proceso completo de fin de mes")

    print("\nEjemplo:")
    print("  Descomenta la línea siguiente para ejecutar:\n")

    # Descomentar el caso que desees ejecutar:
    # caso1_cargar_todo()
    # caso2_cargar_mes_especifico()
    # caso3_reporte_cuentas_por_cobrar()
    # caso4_analisis_pagos()
    # caso5_cargar_no_recursivo()
    # caso6_procesamiento_lotes()
    # caso7_validar_integridad()
    # ejemplo_completo()

    print("(Sin casos ejecutados - edita el archivo para ejecutar)")
