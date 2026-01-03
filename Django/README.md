# Plataforma CFDI Django

Sistema de gestión de Comprobantes Fiscales Digitales por Internet (CFDI) construido con Django y PostgreSQL.

## Características

- ✅ Gestión de múltiples empresas
- ✅ Importación masiva de XMLs desde carpetas (con subcarpetas)
- ✅ Validación de RFC contra empresa
- ✅ Soporte para CFDI 4.0, 3.3 y 3.2
- ✅ Modelos completos: Comprobantes, Nóminas, Pagos, Impuestos
- ✅ Catálogos del SAT integrados
- ✅ Base de datos PostgreSQL
- ✅ Auditoría automática (created_at, updated_at, created_by, updated_by)

## Requisitos

- Python 3.11+
- PostgreSQL 12+
- Librería python-satcfdi

## Instalación

### 1. Instalar dependencias

```bash
cd Django
pip install -r requirements.txt
```

### 2. Configurar base de datos PostgreSQL

Crear la base de datos en PostgreSQL:

```sql
CREATE DATABASE cfdi_platform;
CREATE USER cfdi_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE cfdi_platform TO cfdi_user;
```

### 3. Configurar variables de entorno

Copiar el archivo de ejemplo y editarlo:

```bash
cp .env.example .env
```

Editar `.env` con tus configuraciones:

```env
DB_NAME=cfdi_platform
DB_USER=cfdi_user
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

XML_IMPORT_PATH=/ruta/a/tus/xmls
```

### 4. Crear migraciones y aplicarlas

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

## Uso

### Importar XMLs

El sistema incluye un comando de Django para importar archivos XML de CFDI desde una carpeta (incluyendo subcarpetas).

#### Sintaxis básica:

```bash
python manage.py import_xmls <RFC_EMPRESA> <CARPETA_XML> [opciones]
```

#### Parámetros:

- `RFC_EMPRESA`: RFC de la empresa que importará los XMLs (debe existir en la base de datos)
- `CARPETA_XML`: Ruta de la carpeta que contiene los archivos XML

#### Opciones:

- `--validar-rfc`: Valida que el RFC del emisor o receptor coincida con el RFC de la empresa. Si no coincide, se omite el XML.
- `--actualizar`: Actualiza comprobantes existentes (por defecto se omiten duplicados)

#### Ejemplos:

**Importar todos los XMLs de una carpeta sin validación de RFC:**

```bash
python manage.py import_xmls AAA010101AAA /home/user/xmls/
```

**Importar solo los XMLs donde la empresa sea emisor o receptor:**

```bash
python manage.py import_xmls AAA010101AAA /home/user/xmls/ --validar-rfc
```

**Importar y actualizar XMLs existentes:**

```bash
python manage.py import_xmls AAA010101AAA /home/user/xmls/ --validar-rfc --actualizar
```

#### Proceso de importación:

El comando realiza las siguientes acciones:

1. ✓ Busca recursivamente todos los archivos `.xml` en la carpeta y subcarpetas
2. ✓ Parsea cada XML usando la librería `satcfdi`
3. ✓ Valida el RFC del emisor/receptor contra la empresa (si se usa `--validar-rfc`)
4. ✓ Crea o actualiza las entidades (emisores y receptores)
5. ✓ Crea o actualiza el comprobante con todos sus datos
6. ✓ Importa los conceptos (detalles) del comprobante
7. ✓ Importa los impuestos a nivel comprobante y detalle
8. ✓ Guarda el XML original completo

#### Salida del comando:

```
Empresa: Mi Empresa SA de CV (AAA010101AAA)
Carpeta: /home/user/xmls/
Validar RFC: True

Se encontraron 150 archivos XML

[1/150] ✓ /home/user/xmls/2024/enero/factura001.xml
[2/150] ✓ /home/user/xmls/2024/enero/factura002.xml
[3/150] ⊘ /home/user/xmls/2024/enero/factura003.xml
[4/150] ✗ /home/user/xmls/2024/enero/factura004.xml
    Error: No se encontró el UUID (TimbreFiscalDigital)
...

════════════════════════════════════════════════════════════
RESUMEN DE IMPORTACIÓN
════════════════════════════════════════════════════════════
Total de archivos procesados: 150
✓ Importados: 120
⊘ Omitidos: 25
✗ Errores: 5
```

**Símbolos:**
- ✓ = Importado exitosamente
- ↻ = Actualizado
- ⊘ = Omitido (RFC no coincide o ya existe)
- ✗ = Error al procesar

### Administración Django

Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

Acceder al admin en: `http://localhost:8000/admin/`

## Modelos Principales

### Empresas

- **Empresa**: Empresas del sistema
- **UsuarioEmpresa**: Relación usuario-empresa con roles
- **EmpresaRegimen**: Regímenes fiscales históricos de la empresa

### Comprobantes

- **Entidad**: Emisores y receptores de CFDI
- **Comprobante**: Comprobante fiscal principal
- **Detalle**: Conceptos del comprobante
- **ImpuestoComprobante**: Impuestos a nivel comprobante
- **ImpuestoDetalle**: Impuestos a nivel concepto
- **Pago**: Complemento de pago
- **PagoDocumentoRelacionado**: Documentos relacionados en pagos
- **Nomina**: Complemento de nómina
- **NominaConcepto**: Conceptos de nómina
- **Empleado**: Empleados de la empresa
- **ProveedorCliente**: Proveedores y clientes
- **ArticuloNormalizado**: Artículos normalizados
- **ArticuloAlias**: Alias de artículos

### Catálogos SAT

- RegimenFiscal
- UsoCFDI
- FormaPago
- MetodoPago
- TipoComprobante
- Moneda
- ClaveProdServ
- ClaveUnidad
- Impuesto
- TipoFactor
- Exportacion
- ObjetoImp
- Periodicidad
- Meses
- Y más...

## Estructura del Proyecto

```
Django/
├── cfdi_platform/          # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # App core con modelos base
│   └── models.py          # AuditMixin, CatalogoSATBase
├── catalogos/             # App de catálogos SAT
│   ├── models.py
│   └── admin.py
├── empresas/              # App de empresas
│   ├── models.py
│   └── admin.py
├── comprobantes/          # App de comprobantes
│   ├── models.py
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── import_xmls.py
├── manage.py
├── requirements.txt
└── README.md
```

## Validaciones Implementadas

### Validación de RFC

El comando `import_xmls` incluye validación automática de RFC:

- ✅ El RFC debe tener formato válido (12 o 13 caracteres)
- ✅ Con `--validar-rfc` solo importa XMLs donde la empresa sea emisor o receptor
- ✅ Los RFCs se normalizan automáticamente (mayúsculas, sin espacios)

### Otras Validaciones

- ✅ UUID único por comprobante
- ✅ Fechas de inicio/fin en regímenes fiscales
- ✅ Códigos postales de 5 dígitos
- ✅ CURP válido para empleados
- ✅ Formato de email válido

## Propiedades Calculadas

El modelo `Comprobante` incluye propiedades útiles:

- `es_emitido`: Indica si fue emitido por la empresa
- `es_recibido`: Indica si fue recibido por la empresa
- `es_venta`: Indica si es una venta (ingreso emitido)
- `es_compra`: Indica si es una compra (ingreso recibido)
- `es_pago`: Indica si es complemento de pago
- `es_nomina`: Indica si es comprobante de nómina
- `es_deducible`: Indica si es deducible

## Desarrollo

### Crear nuevas migraciones

```bash
python manage.py makemigrations
```

### Aplicar migraciones

```bash
python manage.py migrate
```

### Crear app nueva

```bash
python manage.py startapp nombre_app
```

## Notas Importantes

1. **Primera vez**: Antes de importar XMLs, asegúrate de:
   - Tener al menos una Empresa creada en la base de datos
   - Tener los catálogos SAT básicos cargados (el comando los crea automáticamente si no existen)

2. **Rendimiento**:
   - La importación usa transacciones para garantizar integridad
   - Para grandes volúmenes, considera importar en lotes

3. **Almacenamiento del XML**:
   - El XML original se guarda completo en el campo `xml_original`
   - Esto permite re-procesar o validar después

4. **Timezone**:
   - El proyecto está configurado para zona horaria de México (America/Mexico_City)
   - Las fechas se convierten automáticamente

## Licencia

Este proyecto es de código abierto.
