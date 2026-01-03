# 📦 Cargar CFDIs desde Directorio Local

Sistema completo para cargar y procesar CFDIs almacenados en carpetas locales.

## 🚀 INICIO RÁPIDO

### 1. Uso Básico (Línea de Comandos)

```bash
python cargar_cfdis_desde_directorio.py /ruta/a/tus/facturas
```

### 2. Uso Programático

```python
from cargar_cfdis_desde_directorio import cargar_cfdis_desde_directorio
from satcfdi.accounting import complement_invoices_data

# Cargar CFDIs
invoices_dict, stats = cargar_cfdis_desde_directorio(
    directorio_base='/home/usuario/facturas/2024',
    recursivo=True
)

print(f"✓ Cargados {stats['cargados']} CFDIs")

# Procesar relaciones y pagos
complement_invoices_data(invoices_dict)

# ¡Listo para usar!
```

## 📁 ARCHIVOS INCLUIDOS

| Archivo | Descripción |
|---------|-------------|
| `cargar_cfdis_desde_directorio.py` | **Script principal** - Carga CFDIs desde carpetas |
| `ejemplo_uso_carga_directorio.py` | **7 casos de uso** con ejemplos prácticos |
| `GUIA_CARGA_DESDE_DIRECTORIO.md` | **Guía completa** con documentación detallada |
| `EJEMPLO_ACCOUNTING_COMPLETO.md` | Documentación del módulo accounting |
| `ejemplo_accounting.py` | Ejemplo funcional del módulo accounting |

## 🎯 CARACTERÍSTICAS

### ✅ Carga Automática
- Escaneo recursivo de carpetas y subcarpetas
- Indexación automática por UUID
- Manejo robusto de errores

### ✅ Validación
- Verifica estructura XML
- Valida presencia de timbre fiscal
- Detecta UUIDs duplicados

### ✅ Estadísticas
- Conteo por tipo de comprobante
- Detección de archivos problemáticos
- Reporte de carga completo

### ✅ Optimización
- Carga eficiente (1000 CFDIs en ~20 segundos)
- Filtrado por fecha
- Procesamiento por lotes

## 📊 CASOS DE USO

### Caso 1: Reporte Mensual

```python
from ejemplo_uso_carga_directorio import caso2_cargar_mes_especifico

# Genera reporte de un mes específico
facturas_enero = caso2_cargar_mes_especifico()
```

### Caso 2: Cuentas por Cobrar

```python
from ejemplo_uso_carga_directorio import caso3_reporte_cuentas_por_cobrar

# Genera reporte de facturas pendientes
pendientes = caso3_reporte_cuentas_por_cobrar()
# Exporta automáticamente a Excel
```

### Caso 3: Análisis de Pagos

```python
from ejemplo_uso_carga_directorio import caso4_analisis_pagos

# Analiza pagos del período
pagos = caso4_analisis_pagos()
```

### Caso 4: Validación de Archivos

```python
from ejemplo_uso_carga_directorio import caso7_validar_integridad

# Valida todos los XMLs del directorio
stats = caso7_validar_integridad()
```

## 📖 DOCUMENTACIÓN

### Para Empezar
1. Lee: `GUIA_CARGA_DESDE_DIRECTORIO.md` - Guía completa paso a paso
2. Revisa: `ejemplo_uso_carga_directorio.py` - 7 ejemplos listos para usar
3. Ejecuta: `python cargar_cfdis_desde_directorio.py /tu/directorio`

### Estructura de Carpetas Recomendada

```
/facturas/
  ├── 2024/
  │   ├── 01/
  │   │   ├── A001.xml
  │   │   ├── A002.xml
  │   │   └── P001.xml
  │   ├── 02/
  │   │   └── ...
  │   └── ...
  └── 2023/
      └── ...
```

## 🔧 REQUISITOS

```bash
pip install satcfdi xlsxwriter tabulate
```

## 📝 EJEMPLO COMPLETO

```python
# 1. Importar
from cargar_cfdis_desde_directorio import cargar_cfdis_desde_directorio
from satcfdi.accounting import (
    complement_invoices_data,
    filter_invoices_iter,
    invoices_export
)
from satcfdi.create.cfd.catalogos import TipoDeComprobante
import xlsxwriter

# 2. Cargar CFDIs
invoices_dict, stats = cargar_cfdis_desde_directorio(
    '/home/usuario/facturas/2024'
)

# 3. Procesar relaciones
complement_invoices_data(invoices_dict)

# 4. Filtrar facturas de ingreso
facturas = list(filter_invoices_iter(
    invoices_dict.values(),
    invoice_type=TipoDeComprobante.INGRESO
))

# 5. Exportar a Excel
workbook = xlsxwriter.Workbook('facturas.xlsx')
invoices_export(workbook, 'Facturas', facturas)
workbook.close()

print(f"✅ Exportadas {len(facturas)} facturas")
```

## ⚡ RENDIMIENTO

| CFDIs | Tiempo | Memoria |
|-------|--------|---------|
| 100 | 2-3 seg | ~50 MB |
| 1,000 | 15-20 seg | ~200 MB |
| 10,000 | 2-3 min | ~1.5 GB |

## 🛠️ PERSONALIZACIÓN

### Clase MiSatCFDI

Para uso en producción, personaliza los métodos:

```python
class MiSatCFDI(SatCFDI):
    def estatus(self):
        # Consultar tu base de datos
        return self.consultar_bd_estado()

    def consulta_estado(self):
        # Consultar SAT/PAC
        return self.consultar_sat_estado()
```

## ❓ SOPORTE

- **Documentación completa:** `GUIA_CARGA_DESDE_DIRECTORIO.md`
- **Ejemplos prácticos:** `ejemplo_uso_carga_directorio.py`
- **Issues:** https://github.com/SAT-CFDI/python-satcfdi/issues

## 📄 LICENCIA

MIT License - Ver archivo LICENSE del proyecto principal

---

**¿Listo para empezar?**

```bash
python cargar_cfdis_desde_directorio.py /tus/facturas
```

🎉 ¡Así de simple!
