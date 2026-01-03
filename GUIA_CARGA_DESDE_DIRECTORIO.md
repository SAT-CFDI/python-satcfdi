# GUÍA COMPLETA: Cargar CFDIs desde Directorio Local

## 📋 ÍNDICE

1. [Introducción](#introducción)
2. [Estructura de Archivos](#estructura-de-archivos)
3. [Proceso de Carga](#proceso-de-carga)
4. [Uso Básico](#uso-básico)
5. [Casos de Uso Avanzados](#casos-de-uso-avanzados)
6. [Manejo de Errores](#manejo-de-errores)
7. [Optimización y Rendimiento](#optimización-y-rendimiento)
8. [FAQ](#faq)

---

## 📖 INTRODUCCIÓN

Esta guía explica cómo cargar CFDIs desde un directorio local (y sus subcarpetas) para usarlos con el módulo `accounting` de `satcfdi`.

### ¿Qué necesitas?

- ✅ Archivos XML de CFDIs en una carpeta local
- ✅ Python 3.11 o superior
- ✅ Librería `satcfdi` instalada
- ✅ Los scripts proporcionados: `cargar_cfdis_desde_directorio.py`

### ¿Qué hace el script?

1. **Escanea** recursivamente un directorio y subcarpetas
2. **Encuentra** todos los archivos `.xml`
3. **Carga** cada XML como objeto CFDI
4. **Valida** que tenga timbre fiscal (UUID)
5. **Indexa** por UUID en un diccionario
6. **Retorna** estructura lista para usar con módulo accounting

---

## 📁 ESTRUCTURA DE ARCHIVOS

### Opción 1: Directorio Plano (Simple)

```
/facturas/
  ├── factura_001.xml
  ├── factura_002.xml
  ├── pago_001.xml
  └── ... (más archivos)
```

**Ventajas:**
- Simple de implementar
- Fácil de entender

**Desventajas:**
- Difícil de organizar con muchos archivos
- Lento de buscar

### Opción 2: Por Año/Mes (Recomendada) ⭐

```
/facturas/
  ├── 2024/
  │   ├── 01/
  │   │   ├── ingresos/
  │   │   │   ├── A001.xml
  │   │   │   └── A002.xml
  │   │   ├── pagos/
  │   │   │   ├── P001.xml
  │   │   │   └── P002.xml
  │   │   └── egresos/
  │   │       └── NC001.xml
  │   ├── 02/
  │   │   └── ...
  │   └── ...
  └── 2023/
      └── ...
```

**Ventajas:**
- ✅ Organizado cronológicamente
- ✅ Fácil cargar por período
- ✅ Mantiene rendimiento con miles de archivos
- ✅ Backup incremental simple

**Desventajas:**
- Requiere estructura de carpetas

### Opción 3: Por Tipo de Comprobante

```
/facturas/
  ├── ingresos/
  │   ├── 2024_01_A001.xml
  │   └── 2024_01_A002.xml
  ├── pagos/
  │   └── 2024_02_P001.xml
  ├── egresos/
  │   └── 2024_01_NC001.xml
  └── nomina/
      └── 2024_01_N001.xml
```

**Ventajas:**
- Fácil filtrar por tipo
- Procesamiento específico por tipo

**Desventajas:**
- Pagos separados de facturas que pagan
- Dificulta reportes por período

---

## 🔄 PROCESO DE CARGA

### Diagrama de Flujo

```
┌─────────────────────────────────────┐
│ 1. Escanear Directorio              │
│    os.walk() recursivo              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Filtrar Archivos .xml            │
│    Encontrados: N archivos          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Para cada archivo:               │
│    ┌─────────────────────────────┐  │
│    │ 3.1 Cargar XML              │  │
│    │     CFDI.from_file()        │  │
│    ├─────────────────────────────┤  │
│    │ 3.2 Extraer UUID            │  │
│    │     Verificar timbre        │  │
│    ├─────────────────────────────┤  │
│    │ 3.3 Crear MiSatCFDI         │  │
│    │     Envolver en clase       │  │
│    ├─────────────────────────────┤  │
│    │ 3.4 Agregar a diccionario   │  │
│    │     {UUID: MiSatCFDI}       │  │
│    └─────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 4. Retornar Resultados              │
│    - invoices_dict: {UUID: CFDI}   │
│    - estadisticas: {cargados, ...} │
└─────────────────────────────────────┘
```

### Código del Proceso

```python
# 1. Escanear directorio
for raiz, dirs, archivos in os.walk(directorio):
    for archivo in archivos:
        if archivo.lower().endswith('.xml'):
            ruta = os.path.join(raiz, archivo)

            # 2. Cargar CFDI
            cfdi = CFDI.from_file(ruta)

            # 3. Extraer UUID
            uuid = UUID(cfdi['Complemento']['TimbreFiscalDigital']['UUID'])

            # 4. Envolver en clase personalizada
            mi_cfdi = MiSatCFDI(cfdi, archivo_origen=ruta)

            # 5. Indexar por UUID
            invoices_dict[uuid] = mi_cfdi
```

---

## 🚀 USO BÁSICO

### 1. Uso desde Línea de Comandos

```bash
# Cargar todas las facturas de un directorio
python cargar_cfdis_desde_directorio.py /home/usuario/facturas/2024

# En Windows
python cargar_cfdis_desde_directorio.py C:\Facturas\2024
```

**Resultado:**
```
================================================================================
CARGADOR DE CFDIs DESDE DIRECTORIO
================================================================================

Directorio: /home/usuario/facturas/2024

PASO 1: Cargando CFDIs desde directorio...
--------------------------------------------------------------------------------
Escaneando directorio: /home/usuario/facturas/2024
Búsqueda recursiva: True
Encontrados 150 archivos XML
Progreso: 10/150 (6.7%)
Progreso: 20/150 (13.3%)
...
Progreso: 150/150 (100.0%)
================================================================================
CARGA COMPLETADA
  ✓ CFDIs cargados exitosamente: 148
  ✗ Archivos con error: 1
  ⚠ Sin timbre fiscal: 1
  ⚠ UUIDs duplicados: 0

Distribución por tipo de comprobante:
    I: 100 (Ingresos)
    P: 45 (Pagos)
    E: 3 (Egresos)
================================================================================

¿Desea exportar las 100 facturas de ingreso a Excel? (s/n): s
   ✓ Exportadas 100 facturas
   ✓ Exportados 45 pagos

✓ Archivo generado: facturas_export_20240115_143022.xlsx
  Tamaño: 45,234 bytes (44.2 KB)
```

### 2. Uso Programático (Python)

```python
from cargar_cfdis_desde_directorio import cargar_cfdis_desde_directorio
from satcfdi.accounting import complement_invoices_data

# Cargar CFDIs
invoices_dict, stats = cargar_cfdis_desde_directorio(
    directorio_base='/home/usuario/facturas/2024',
    recursivo=True,
    mostrar_progreso=True
)

print(f"Cargados: {stats['cargados']} CFDIs")

# Complementar datos (relacionar pagos)
complement_invoices_data(invoices_dict)

# Ahora puedes usar todas las funciones del módulo accounting
```

### 3. Uso con Filtros

```python
from satcfdi.accounting import filter_invoices_iter
from satcfdi.create.cfd.catalogos import TipoDeComprobante

# Cargar
invoices_dict, _ = cargar_cfdis_desde_directorio('/facturas')
complement_invoices_data(invoices_dict)

# Filtrar facturas de ingreso
facturas = list(filter_invoices_iter(
    invoices_dict.values(),
    invoice_type=TipoDeComprobante.INGRESO
))

print(f"Facturas de ingreso: {len(facturas)}")
```

---

## 🎯 CASOS DE USO AVANZADOS

### Caso 1: Reporte Mensual

```python
from datetime import date
from cargar_cfdis_desde_directorio import (
    cargar_cfdis_desde_directorio,
    filtrar_por_fecha
)

# Cargar todo el año
invoices_dict, _ = cargar_cfdis_desde_directorio('/facturas/2024')

# Filtrar por mes
facturas_enero = filtrar_por_fecha(
    invoices_dict,
    fecha_inicio=date(2024, 1, 1),
    fecha_fin=date(2024, 1, 31)
)

complement_invoices_data(facturas_enero)

# Generar reporte
facturas = list(filter_invoices_iter(
    facturas_enero.values(),
    invoice_type=TipoDeComprobante.INGRESO
))

total = sum(f['Total'] for f in facturas)
print(f"Total facturado en enero: ${total:,.2f}")
```

### Caso 2: Cuentas por Cobrar

```python
# Cargar facturas
invoices_dict, _ = cargar_cfdis_desde_directorio('/facturas')
complement_invoices_data(invoices_dict)

# Facturas con saldo pendiente
pendientes = list(filter_invoices_iter(
    invoices_dict.values(),
    invoice_type=TipoDeComprobante.INGRESO,
    pending_balance=lambda x: x is not None and x > 0
))

# Agrupar por cliente
from itertools import groupby

pendientes.sort(key=lambda f: f['Receptor']['Rfc'])

for rfc, facturas in groupby(pendientes, key=lambda f: f['Receptor']['Rfc']):
    facturas_list = list(facturas)
    total_pendiente = sum(f.saldo_pendiente() for f in facturas_list)

    print(f"\nCliente: {rfc}")
    print(f"  Facturas pendientes: {len(facturas_list)}")
    print(f"  Saldo: ${total_pendiente:,.2f}")
```

### Caso 3: Análisis de Pagos

```python
from datetime import datetime

# Cargar
invoices_dict, _ = cargar_cfdis_desde_directorio('/facturas')
complement_invoices_data(invoices_dict)

# Filtrar pagos del mes
def es_mes_actual(fecha):
    ahora = datetime.now()
    return fecha.year == ahora.year and fecha.month == ahora.month

pagos = list(filter_payments_iter(
    invoices_dict,
    fecha=es_mes_actual
))

total_cobrado = sum(p.total for p in pagos)
print(f"Total cobrado este mes: ${total_cobrado:,.2f}")

# Análisis por forma de pago
from collections import Counter

formas_pago = Counter(
    str(p.pago['FormaDePagoP'] if p.pago else p.comprobante.get('FormaPago'))
    for p in pagos
)

print("\nFormas de pago:")
for forma, cantidad in formas_pago.most_common():
    print(f"  {forma}: {cantidad} pagos")
```

### Caso 4: Procesamiento por Lotes (Grandes Volúmenes)

```python
import os

# Procesar mes por mes para reducir uso de memoria
base_dir = '/facturas/2024'
meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

reportes_anuales = []

for mes in meses:
    mes_dir = os.path.join(base_dir, mes)

    if not os.path.exists(mes_dir):
        continue

    print(f"Procesando {mes}...")

    # Cargar solo ese mes
    invoices_mes, _ = cargar_cfdis_desde_directorio(
        mes_dir,
        recursivo=False,
        mostrar_progreso=False
    )

    complement_invoices_data(invoices_mes)

    # Generar estadísticas
    facturas = list(filter_invoices_iter(
        invoices_mes.values(),
        invoice_type=TipoDeComprobante.INGRESO
    ))

    total = sum(f['Total'] for f in facturas)

    reportes_anuales.append({
        'mes': mes,
        'facturas': len(facturas),
        'total': total
    })

    # Liberar memoria
    del invoices_mes
    del facturas

# Resumen anual
total_anual = sum(r['total'] for r in reportes_anuales)
print(f"\nTotal facturado en el año: ${total_anual:,.2f}")
```

### Caso 5: Validar Integridad de Archivos

```python
# Cargar con manejo de errores
invoices_dict, stats = cargar_cfdis_desde_directorio(
    '/facturas',
    recursivo=True,
    detener_en_error=False  # Continuar aunque haya errores
)

print("VALIDACIÓN DE ARCHIVOS:")
print(f"  ✓ Válidos: {stats['cargados']}")
print(f"  ✗ Con error: {stats['errores']}")
print(f"  ⚠ Sin timbre: {stats['sin_timbre']}")
print(f"  ⚠ Duplicados: {stats['duplicados']}")

# Ver archivos con error
if stats['archivos_error']:
    print("\nArchivos problemáticos:")
    for error in stats['archivos_error']:
        print(f"  • {error['archivo']}")
        print(f"    Error: {error['error']}")
```

---

## ⚠️ MANEJO DE ERRORES

### Tipos de Errores Comunes

#### 1. XML Corrupto o Mal Formado

**Error:**
```
Error al cargar /facturas/factura_001.xml: XML mal formado
```

**Solución:**
- Verificar que el archivo no esté dañado
- Abrir con editor de texto y revisar estructura
- Regenerar el XML desde el sistema de facturación

#### 2. Sin Timbre Fiscal

**Error:**
```
Sin timbre fiscal: /facturas/factura_002.xml - KeyError: 'TimbreFiscalDigital'
```

**Causa:**
- El XML no ha sido timbrado
- Es un CFDI en borrador

**Solución:**
- Timbrar el CFDI con un PAC
- Excluir archivos sin timbrar

#### 3. UUID Duplicado

**Error:**
```
UUID duplicado: 12345678-1234-1234-1234-123456789012
```

**Causa:**
- El mismo XML está en dos ubicaciones
- Se copió o respaldó en múltiples carpetas

**Solución:**
- Eliminar duplicado
- Reorganizar estructura de carpetas
- El script automáticamente ignora duplicados

#### 4. Archivo No Encontrado

**Error:**
```
ValueError: El directorio no existe: /facturas/2024
```

**Solución:**
- Verificar que la ruta sea correcta
- Verificar permisos de lectura
- Usar rutas absolutas en lugar de relativas

### Estrategias de Manejo

#### Opción 1: Continuar con Errores (Recomendado)

```python
invoices_dict, stats = cargar_cfdis_desde_directorio(
    '/facturas',
    detener_en_error=False  # Continuar aunque haya errores
)

# Revisar estadísticas
if stats['errores'] > 0:
    print(f"⚠️  {stats['errores']} archivos con error")
    # Continuar con los que sí se cargaron
```

#### Opción 2: Detener en Primer Error

```python
try:
    invoices_dict, stats = cargar_cfdis_desde_directorio(
        '/facturas',
        detener_en_error=True  # Detener al primer error
    )
except Exception as e:
    print(f"Error crítico: {e}")
    # Manejar error
```

#### Opción 3: Validación Previa

```python
import os
from lxml import etree

# Validar archivos antes de cargar
def validar_xml(ruta):
    try:
        tree = etree.parse(ruta)
        return True
    except:
        return False

# Filtrar solo archivos válidos
archivos_validos = []
for archivo in os.listdir('/facturas'):
    if archivo.endswith('.xml'):
        ruta = os.path.join('/facturas', archivo)
        if validar_xml(ruta):
            archivos_validos.append(ruta)

print(f"Archivos válidos: {len(archivos_validos)}")
```

---

## ⚡ OPTIMIZACIÓN Y RENDIMIENTO

### Benchmarks

| Cantidad de CFDIs | Tiempo de Carga | Memoria Usada |
|-------------------|-----------------|---------------|
| 100               | 2-3 segundos    | ~50 MB        |
| 1,000             | 15-20 segundos  | ~200 MB       |
| 10,000            | 2-3 minutos     | ~1.5 GB       |
| 100,000           | 20-30 minutos   | ~15 GB        |

### Estrategias de Optimización

#### 1. Carga Incremental

```python
# En lugar de cargar todo:
invoices_dict, _ = cargar_cfdis_desde_directorio('/facturas')  # ❌ Pesado

# Cargar por períodos:
invoices_dict, _ = cargar_cfdis_desde_directorio('/facturas/2024/01')  # ✅ Ligero
```

#### 2. Filtrado Temprano

```python
# Filtrar durante la carga (más eficiente)
def solo_ingresos(cfdi):
    return cfdi.get('TipoDeComprobante') == 'I'

# Modificar cargar_cfdis_desde_directorio para aceptar filtro
# O filtrar después de cargar solo el mes necesario
```

#### 3. Cache en Disco

```python
import pickle
from pathlib import Path

cache_file = 'invoices_cache.pkl'

# Cargar desde cache si existe
if Path(cache_file).exists():
    with open(cache_file, 'rb') as f:
        invoices_dict = pickle.load(f)
else:
    # Cargar desde directorio
    invoices_dict, _ = cargar_cfdis_desde_directorio('/facturas')

    # Guardar en cache
    with open(cache_file, 'wb') as f:
        pickle.dump(invoices_dict, f)
```

#### 4. Procesamiento Paralelo

```python
from multiprocessing import Pool
import os

def cargar_archivo(ruta):
    try:
        cfdi = CFDI.from_file(ruta)
        uuid = UUID(cfdi['Complemento']['TimbreFiscalDigital']['UUID'])
        return uuid, MiSatCFDI(cfdi, ruta)
    except:
        return None, None

# Obtener lista de archivos
archivos = [
    os.path.join(raiz, f)
    for raiz, _, archivos in os.walk('/facturas')
    for f in archivos if f.endswith('.xml')
]

# Procesar en paralelo
with Pool(4) as pool:  # 4 procesos
    resultados = pool.map(cargar_archivo, archivos)

# Construir diccionario
invoices_dict = {
    uuid: cfdi
    for uuid, cfdi in resultados
    if uuid is not None
}
```

#### 5. Base de Datos para Grandes Volúmenes

```python
import sqlite3

# Crear BD para metadata
conn = sqlite3.connect('facturas.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS facturas
             (uuid TEXT PRIMARY KEY,
              archivo TEXT,
              rfc_emisor TEXT,
              rfc_receptor TEXT,
              fecha TEXT,
              total REAL,
              tipo TEXT)''')

# Insertar metadata al cargar
for uuid, cfdi in invoices_dict.items():
    c.execute('INSERT OR REPLACE INTO facturas VALUES (?,?,?,?,?,?,?)',
              (str(uuid),
               cfdi.archivo_origen,
               cfdi['Emisor']['Rfc'],
               cfdi['Receptor']['Rfc'],
               str(cfdi['Fecha']),
               float(cfdi['Total']),
               str(cfdi['TipoDeComprobante'])))

conn.commit()

# Consultar metadata rápidamente
c.execute('SELECT * FROM facturas WHERE rfc_emisor = ?', ('AAA010101AAA',))
# Cargar solo los XMLs necesarios
```

---

## ❓ FAQ (Preguntas Frecuentes)

### ¿Puedo cargar CFDIs de diferentes años?

**Sí.** Simplemente organiza en subcarpetas por año y usa `recursivo=True`:

```python
invoices_dict, _ = cargar_cfdis_desde_directorio(
    '/facturas',  # Contiene /2023, /2024, etc.
    recursivo=True
)
```

### ¿Qué pasa si hay archivos que no son CFDIs?

El script automáticamente filtra solo archivos `.xml`. Archivos con otras extensiones se ignoran.

### ¿Puedo cargar desde múltiples directorios?

**Sí.** Carga cada directorio y combina los diccionarios:

```python
inv1, _ = cargar_cfdis_desde_directorio('/facturas/emisor1')
inv2, _ = cargar_cfdis_desde_directorio('/facturas/emisor2')

# Combinar
invoices_dict = {**inv1, **inv2}
```

### ¿Cómo manejo archivos muy grandes (>100MB)?

Los archivos XML de CFDI raramente superan 1-2 MB. Si tienes archivos muy grandes:

1. Verifica que sean CFDIs válidos
2. Considera dividirlos si contienen múltiples documentos
3. Usa `lxml` con parseo incremental

### ¿Puedo cargar desde un servidor remoto?

**Sí.** Primero descarga con `rsync`, `scp`, o monta el directorio remoto:

```bash
# Opción 1: Copiar archivos
rsync -avz servidor:/facturas/ /tmp/facturas/

# Opción 2: Montar directorio remoto (Linux)
sshfs servidor:/facturas /mnt/facturas

# Luego cargar normalmente
python cargar_cfdis_desde_directorio.py /mnt/facturas
```

### ¿Cuánta memoria necesito?

Aproximadamente:
- **1 CFDI = ~100-200 KB en memoria**
- **1,000 CFDIs = ~200 MB**
- **10,000 CFDIs = ~2 GB**

Para volúmenes grandes, usa procesamiento por lotes.

### ¿Los cambios en el directorio se reflejan automáticamente?

**No.** El diccionario es una "foto" del momento de carga. Si agregas nuevos XMLs:

```python
# Recargar
invoices_dict, _ = cargar_cfdis_desde_directorio('/facturas')
```

O implementa un sistema de monitoreo de archivos.

### ¿Puedo filtrar al cargar?

Actualmente el script carga todo. Para filtrar:

```python
# Cargar todo
invoices_dict, _ = cargar_cfdis_desde_directorio('/facturas')

# Filtrar después
from cargar_cfdis_desde_directorio import filtrar_por_fecha

facturas_enero = filtrar_por_fecha(
    invoices_dict,
    fecha_inicio=date(2024, 1, 1),
    fecha_fin=date(2024, 1, 31)
)
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Preparación

- [ ] Organizar archivos XML en estructura de carpetas
- [ ] Verificar que todos los XMLs sean válidos
- [ ] Instalar dependencias: `pip install satcfdi xlsxwriter`
- [ ] Descargar scripts: `cargar_cfdis_desde_directorio.py`

### Carga Inicial

- [ ] Probar con directorio pequeño (10-20 XMLs)
- [ ] Verificar que se carguen correctamente
- [ ] Revisar estadísticas de carga
- [ ] Identificar archivos con error

### Procesamiento

- [ ] Ejecutar `complement_invoices_data()`
- [ ] Verificar relaciones de pagos
- [ ] Probar filtros básicos
- [ ] Generar primer reporte

### Producción

- [ ] Definir estrategia de carga (completa vs incremental)
- [ ] Configurar manejo de errores
- [ ] Implementar logging
- [ ] Automatizar con cron/scheduler
- [ ] Documentar proceso para el equipo

---

## 📚 RECURSOS ADICIONALES

- **Script principal:** `cargar_cfdis_desde_directorio.py`
- **Ejemplos:** `ejemplo_uso_carga_directorio.py`
- **Documentación accounting:** `EJEMPLO_ACCOUNTING_COMPLETO.md`
- **Repositorio:** https://github.com/SAT-CFDI/python-satcfdi

---

## 🎓 CONCLUSIÓN

Con esta guía y los scripts proporcionados, puedes:

✅ Cargar eficientemente CFDIs desde cualquier estructura de carpetas
✅ Procesar miles de comprobantes sin problemas
✅ Generar reportes contables y financieros
✅ Automatizar procesos de facturación
✅ Integrar con sistemas existentes

**¡Todo listo para empezar a trabajar con tus CFDIs!**
