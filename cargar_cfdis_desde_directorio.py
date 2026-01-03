#!/usr/bin/env python3
"""
SCRIPT PARA CARGAR CFDIs DESDE DIRECTORIO LOCAL
================================================

Este script recorre recursivamente un directorio y todas sus subcarpetas,
carga todos los archivos XML (CFDIs), y genera la estructura de datos
necesaria para usar el módulo accounting de satcfdi.

Características:
- Búsqueda recursiva en carpetas y subcarpetas
- Manejo de errores (XMLs corruptos, sin timbre, etc.)
- Indexación por UUID para búsqueda rápida
- Estadísticas de carga
- Clase SatCFDI personalizada con estado simulado
- Ejemplos de uso con funciones del módulo accounting

Uso:
    python cargar_cfdis_desde_directorio.py /ruta/a/carpeta/facturas
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from collections import Counter
import logging

# Importar módulos de satcfdi
from satcfdi.cfdi import CFDI
from satcfdi.accounting import (
    SatCFDI,
    complement_invoices_data,
    filter_invoices_iter,
    filter_payments_iter,
    invoices_print,
    payments_print,
    invoices_export,
    payments_export
)
from satcfdi.create.catalogos import EstadoComprobante
from satcfdi.create.cfd.catalogos import TipoDeComprobante

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# CLASE PERSONALIZADA DE SatCFDI
# ==============================================================================

class MiSatCFDI(SatCFDI):
    """
    Extensión personalizada de SatCFDI para implementar métodos requeridos.

    En producción, estos métodos deberían:
    - consultar_estado(): Consultar el estado real con el PAC o SAT
    - estatus(): Obtener de base de datos o consultar SAT
    - fecha_cancelacion(): Obtener de base de datos o consultar SAT

    Para este ejemplo, usamos valores simulados.
    """

    def __init__(self, cfdi_data, archivo_origen=None):
        super().__init__(cfdi_data)
        self.archivo_origen = archivo_origen
        self._estado = EstadoComprobante.VIGENTE
        self._consulta_estado_cache = None
        self._fecha_cancelacion = None

    def estatus(self) -> EstadoComprobante:
        """
        Retorna el estado del comprobante.

        En producción, esto debería:
        - Consultar tu base de datos
        - O consultar el estado con el PAC/SAT
        - O usar un cache
        """
        return self._estado

    def consulta_estado(self) -> dict:
        """
        Consulta el estado del CFDI en el SAT.

        En producción, esto haría una petición HTTP al SAT o PAC.
        Para el ejemplo, retornamos valores simulados.
        """
        if self._consulta_estado_cache is None:
            # Simular consulta (en producción, hacer petición HTTP real)
            self._consulta_estado_cache = {
                'CodigoEstatus': '1',
                'Estado': 'Vigente',
                'EsCancelable': 'Cancelable sin aceptación',
                'EstatusCancelacion': 'No cancelado'
            }
        return self._consulta_estado_cache

    @property
    def fecha_cancelacion(self) -> datetime | None:
        """
        Retorna la fecha de cancelación si existe.

        En producción, obtener de base de datos o del resultado
        de consulta_estado().
        """
        return self._fecha_cancelacion

    def marcar_como_cancelado(self, fecha_cancelacion=None):
        """Método auxiliar para marcar un CFDI como cancelado"""
        self._estado = EstadoComprobante.CANCELADO
        self._fecha_cancelacion = fecha_cancelacion or datetime.now()
        self._consulta_estado_cache = {
            'CodigoEstatus': '2',
            'Estado': 'Cancelado',
            'EsCancelable': 'No cancelable',
            'EstatusCancelacion': 'Cancelado'
        }


# ==============================================================================
# FUNCIÓN PRINCIPAL: CARGAR CFDIs DESDE DIRECTORIO
# ==============================================================================

def cargar_cfdis_desde_directorio(
    directorio_base,
    extensiones=('.xml',),
    recursivo=True,
    mostrar_progreso=True,
    detener_en_error=False
):
    """
    Carga todos los CFDIs desde un directorio y sus subcarpetas.

    Args:
        directorio_base (str): Ruta del directorio a escanear
        extensiones (tuple): Extensiones de archivo a buscar (default: .xml)
        recursivo (bool): Si True, busca en subcarpetas (default: True)
        mostrar_progreso (bool): Mostrar progreso de carga (default: True)
        detener_en_error (bool): Detener si hay error al cargar XML (default: False)

    Returns:
        dict: Diccionario {UUID: MiSatCFDI} con todos los CFDIs cargados
        dict: Diccionario con estadísticas de la carga

    Example:
        >>> invoices, stats = cargar_cfdis_desde_directorio('/facturas/2024')
        >>> print(f"Cargadas {stats['cargados']} facturas")
    """

    directorio = Path(directorio_base)

    if not directorio.exists():
        raise ValueError(f"El directorio no existe: {directorio_base}")

    if not directorio.is_dir():
        raise ValueError(f"La ruta no es un directorio: {directorio_base}")

    logger.info(f"Escaneando directorio: {directorio.absolute()}")
    logger.info(f"Búsqueda recursiva: {recursivo}")

    # Buscar archivos
    archivos_xml = []

    if recursivo:
        # Buscar recursivamente con os.walk
        for raiz, dirs, archivos in os.walk(directorio):
            for archivo in archivos:
                if archivo.lower().endswith(extensiones):
                    ruta_completa = os.path.join(raiz, archivo)
                    archivos_xml.append(ruta_completa)
    else:
        # Buscar solo en el directorio actual
        for archivo in os.listdir(directorio):
            if archivo.lower().endswith(extensiones):
                ruta_completa = os.path.join(directorio, archivo)
                if os.path.isfile(ruta_completa):
                    archivos_xml.append(ruta_completa)

    total_archivos = len(archivos_xml)
    logger.info(f"Encontrados {total_archivos} archivos XML")

    if total_archivos == 0:
        logger.warning("No se encontraron archivos XML en el directorio")
        return {}, {'cargados': 0, 'errores': 0, 'sin_timbre': 0}

    # Cargar CFDIs
    invoices_dict = {}
    estadisticas = {
        'cargados': 0,
        'errores': 0,
        'sin_timbre': 0,
        'duplicados': 0,
        'por_tipo': Counter(),
        'archivos_error': []
    }

    for idx, ruta_archivo in enumerate(archivos_xml, 1):
        if mostrar_progreso and idx % 10 == 0:
            porcentaje = (idx / total_archivos) * 100
            logger.info(f"Progreso: {idx}/{total_archivos} ({porcentaje:.1f}%)")

        try:
            # Cargar CFDI desde archivo
            cfdi = CFDI.from_file(ruta_archivo)

            # Verificar que tiene TimbreFiscalDigital
            try:
                uuid_str = cfdi['Complemento']['TimbreFiscalDigital']['UUID']
                uuid = UUID(uuid_str)
            except (KeyError, TypeError, ValueError) as e:
                logger.warning(f"Sin timbre fiscal: {ruta_archivo} - {e}")
                estadisticas['sin_timbre'] += 1
                continue

            # Verificar si ya existe (UUID duplicado)
            if uuid in invoices_dict:
                logger.warning(f"UUID duplicado: {uuid} - {ruta_archivo}")
                estadisticas['duplicados'] += 1
                continue

            # Crear objeto MiSatCFDI
            mi_cfdi = MiSatCFDI(cfdi, archivo_origen=ruta_archivo)

            # Agregar al diccionario
            invoices_dict[uuid] = mi_cfdi

            # Estadísticas
            estadisticas['cargados'] += 1
            tipo = cfdi.get('TipoDeComprobante', 'Desconocido')
            estadisticas['por_tipo'][str(tipo)] += 1

        except Exception as e:
            logger.error(f"Error al cargar {ruta_archivo}: {e}")
            estadisticas['errores'] += 1
            estadisticas['archivos_error'].append({
                'archivo': ruta_archivo,
                'error': str(e)
            })

            if detener_en_error:
                raise

    logger.info("=" * 80)
    logger.info("CARGA COMPLETADA")
    logger.info(f"  ✓ CFDIs cargados exitosamente: {estadisticas['cargados']}")
    logger.info(f"  ✗ Archivos con error: {estadisticas['errores']}")
    logger.info(f"  ⚠ Sin timbre fiscal: {estadisticas['sin_timbre']}")
    logger.info(f"  ⚠ UUIDs duplicados: {estadisticas['duplicados']}")

    if estadisticas['por_tipo']:
        logger.info("\nDistribución por tipo de comprobante:")
        for tipo, cantidad in estadisticas['por_tipo'].most_common():
            logger.info(f"    {tipo}: {cantidad}")

    logger.info("=" * 80)

    return invoices_dict, estadisticas


# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================

def filtrar_por_fecha(invoices_dict, fecha_inicio=None, fecha_fin=None):
    """
    Filtra CFDIs por rango de fechas.

    Args:
        invoices_dict: Diccionario de CFDIs
        fecha_inicio: Fecha inicial (datetime o date)
        fecha_fin: Fecha final (datetime o date)

    Returns:
        dict: Diccionario filtrado
    """
    resultado = {}

    for uuid, cfdi in invoices_dict.items():
        fecha_cfdi = cfdi['Fecha']

        # Convertir a date si es datetime para comparación
        if isinstance(fecha_cfdi, datetime):
            fecha_cfdi = fecha_cfdi.date()

        incluir = True

        if fecha_inicio:
            if isinstance(fecha_inicio, datetime):
                fecha_inicio = fecha_inicio.date()
            if fecha_cfdi < fecha_inicio:
                incluir = False

        if fecha_fin:
            if isinstance(fecha_fin, datetime):
                fecha_fin = fecha_fin.date()
            if fecha_cfdi > fecha_fin:
                incluir = False

        if incluir:
            resultado[uuid] = cfdi

    return resultado


def mostrar_resumen(invoices_dict):
    """
    Muestra un resumen de los CFDIs cargados.

    Args:
        invoices_dict: Diccionario de CFDIs
    """
    total = len(invoices_dict)

    # Contar por tipo
    tipos = Counter(
        str(cfdi.get('TipoDeComprobante', 'Desconocido'))
        for cfdi in invoices_dict.values()
    )

    # Contar por RFC emisor
    emisores = Counter(
        cfdi['Emisor']['Rfc']
        for cfdi in invoices_dict.values()
    )

    # Calcular totales
    total_facturado = sum(
        cfdi.get('Total', 0)
        for cfdi in invoices_dict.values()
        if cfdi.get('TipoDeComprobante') == TipoDeComprobante.INGRESO
    )

    print("\n" + "=" * 80)
    print("RESUMEN DE CFDIs CARGADOS")
    print("=" * 80)
    print(f"\n📊 Total de CFDIs: {total}")

    print("\n📋 Por tipo de comprobante:")
    for tipo, cantidad in tipos.most_common():
        porcentaje = (cantidad / total * 100) if total > 0 else 0
        print(f"   • {tipo}: {cantidad} ({porcentaje:.1f}%)")

    print(f"\n💰 Total facturado (Ingresos): ${total_facturado:,.2f}")

    print(f"\n🏢 Emisores únicos: {len(emisores)}")
    if len(emisores) <= 5:
        for rfc, cantidad in emisores.most_common():
            print(f"   • {rfc}: {cantidad} CFDIs")
    else:
        print("   (Mostrando top 5)")
        for rfc, cantidad in emisores.most_common(5):
            print(f"   • {rfc}: {cantidad} CFDIs")

    print("=" * 80 + "\n")


# ==============================================================================
# FUNCIÓN PRINCIPAL PARA EJEMPLO
# ==============================================================================

def main():
    """
    Función principal de ejemplo que demuestra cómo usar el script.
    """

    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python cargar_cfdis_desde_directorio.py <directorio>")
        print("\nEjemplo:")
        print("  python cargar_cfdis_desde_directorio.py /home/usuario/facturas/2024")
        print("  python cargar_cfdis_desde_directorio.py C:\\Facturas\\2024")
        sys.exit(1)

    directorio = sys.argv[1]

    print("=" * 80)
    print("CARGADOR DE CFDIs DESDE DIRECTORIO")
    print("=" * 80)
    print(f"\nDirectorio: {directorio}")
    print()

    # PASO 1: Cargar CFDIs desde directorio
    print("PASO 1: Cargando CFDIs desde directorio...")
    print("-" * 80)

    invoices_dict, stats = cargar_cfdis_desde_directorio(
        directorio,
        recursivo=True,
        mostrar_progreso=True,
        detener_en_error=False
    )

    if stats['cargados'] == 0:
        print("\n⚠️  No se cargaron CFDIs. Verifica el directorio.")
        sys.exit(0)

    # PASO 2: Mostrar resumen
    mostrar_resumen(invoices_dict)

    # PASO 3: Complementar datos (relacionar pagos con facturas)
    print("\nPASO 2: Complementando datos (relaciones y pagos)...")
    print("-" * 80)

    complement_invoices_data(invoices_dict)

    # Verificar cuántas facturas tienen pagos
    facturas_con_pagos = sum(
        1 for cfdi in invoices_dict.values()
        if cfdi.get('TipoDeComprobante') == TipoDeComprobante.INGRESO and len(cfdi.payments) > 0
    )

    print(f"✓ Datos complementados exitosamente")
    print(f"  • Facturas con pagos registrados: {facturas_con_pagos}")

    # PASO 4: Ejemplos de filtrado
    print("\n" + "=" * 80)
    print("EJEMPLOS DE USO")
    print("=" * 80)

    # Ejemplo 1: Filtrar facturas de ingreso
    print("\n1. Facturas de INGRESO:")
    facturas_ingreso = list(filter_invoices_iter(
        invoices_dict.values(),
        invoice_type=TipoDeComprobante.INGRESO
    ))
    print(f"   → Encontradas: {len(facturas_ingreso)} facturas")

    # Ejemplo 2: Facturas con saldo pendiente
    print("\n2. Facturas con SALDO PENDIENTE:")
    facturas_pendientes = list(filter_invoices_iter(
        invoices_dict.values(),
        invoice_type=TipoDeComprobante.INGRESO,
        pending_balance=lambda x: x is not None and x > 0
    ))
    print(f"   → Encontradas: {len(facturas_pendientes)} facturas")

    if facturas_pendientes:
        total_pendiente = sum(f.saldo_pendiente() for f in facturas_pendientes)
        print(f"   → Total por cobrar: ${total_pendiente:,.2f}")

    # Ejemplo 3: Pagos realizados
    print("\n3. Pagos REALIZADOS:")
    pagos = list(filter_payments_iter(invoices_dict))
    print(f"   → Encontrados: {len(pagos)} pagos")

    if pagos:
        total_cobrado = sum(p.total for p in pagos)
        print(f"   → Total cobrado: ${total_cobrado:,.2f}")

    # PASO 5: Preguntar si desea exportar
    print("\n" + "=" * 80)
    print("OPCIONES DE EXPORTACIÓN")
    print("=" * 80)

    if facturas_ingreso:
        print(f"\n¿Desea exportar las {len(facturas_ingreso)} facturas de ingreso a Excel? (s/n): ", end="")
        respuesta = input().strip().lower()

        if respuesta == 's':
            import xlsxwriter

            archivo_excel = f"facturas_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            workbook = xlsxwriter.Workbook(archivo_excel)

            # Exportar facturas
            if facturas_ingreso:
                invoices_export(workbook, 'Facturas', facturas_ingreso)
                print(f"   ✓ Exportadas {len(facturas_ingreso)} facturas")

            # Exportar pagos
            if pagos:
                payments_export(workbook, 'Pagos', pagos)
                print(f"   ✓ Exportados {len(pagos)} pagos")

            workbook.close()
            print(f"\n✓ Archivo generado: {archivo_excel}")

            # Mostrar tamaño
            size = os.path.getsize(archivo_excel)
            print(f"  Tamaño: {size:,} bytes ({size/1024:.1f} KB)")

    print("\n" + "=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)
    print("\nLos CFDIs están cargados en memoria y listos para usar.")
    print("Puedes usar las funciones del módulo accounting con 'invoices_dict'")
    print("\nEjemplos:")
    print("  - filter_invoices_iter(invoices_dict.values(), ...)")
    print("  - filter_payments_iter(invoices_dict, ...)")
    print("  - invoices_print(facturas)")
    print("  - payments_print(pagos)")
    print()


# ==============================================================================
# PUNTO DE ENTRADA
# ==============================================================================

if __name__ == "__main__":
    main()
