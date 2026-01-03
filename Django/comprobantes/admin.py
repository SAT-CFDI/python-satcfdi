"""
Configuración del admin para comprobantes
"""
from django.contrib import admin
from .models import (
    Entidad, Comprobante, Detalle, ImpuestoComprobante, ImpuestoDetalle,
    Pago, PagoDocumentoRelacionado, Empleado, Nomina, NominaConcepto,
    ProveedorCliente, ArticuloNormalizado, ArticuloAlias
)


@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = ['rfc', 'nombre', 'tipo', 'empresa', 'total_emitidos', 'total_recibidos']
    list_filter = ['tipo', 'empresa']
    search_fields = ['rfc', 'nombre']
    readonly_fields = ['created_at', 'updated_at', 'total_emitidos', 'total_recibidos']


class DetalleInline(admin.TabularInline):
    model = Detalle
    extra = 0
    fields = ['numero_linea', 'descripcion', 'cantidad', 'valor_unitario', 'importe']
    readonly_fields = ['numero_linea', 'descripcion', 'cantidad', 'valor_unitario', 'importe']


class ImpuestoComprobanteInline(admin.TabularInline):
    model = ImpuestoComprobante
    extra = 0
    fields = ['tipo', 'impuesto', 'tipo_factor', 'tasa_cuota', 'importe']
    readonly_fields = ['tipo', 'impuesto', 'tipo_factor', 'tasa_cuota', 'importe']


@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    list_display = [
        'uuid', 'fecha_emision', 'tipo_comprobante', 'emisor',
        'receptor', 'total', 'moneda', 'estatus_sat'
    ]
    list_filter = [
        'tipo_comprobante', 'estatus_sat', 'moneda',
        'fecha_emision', 'empresa'
    ]
    search_fields = ['uuid', 'emisor__rfc', 'receptor__rfc', 'serie', 'folio']
    readonly_fields = [
        'uuid', 'created_at', 'updated_at', 'xml_original',
        'es_emitido', 'es_recibido', 'es_venta', 'es_compra'
    ]
    inlines = [DetalleInline, ImpuestoComprobanteInline]
    date_hierarchy = 'fecha_emision'

    fieldsets = (
        ('Identificación', {
            'fields': ('uuid', 'empresa', 'version', 'serie', 'folio')
        }),
        ('Emisor y Receptor', {
            'fields': ('emisor', 'receptor', 'uso_cfdi')
        }),
        ('Fechas', {
            'fields': ('fecha_emision', 'fecha_timbrado', 'lugar_expedicion')
        }),
        ('Tipo', {
            'fields': ('tipo_comprobante', 'exportacion')
        }),
        ('Montos', {
            'fields': (
                'moneda', 'tipo_cambio', 'subtotal', 'descuento',
                'impuesto_trasladado_total', 'impuesto_retenido_total', 'total'
            )
        }),
        ('Pago', {
            'fields': ('metodo_pago', 'forma_pago', 'condiciones_pago')
        }),
        ('Información Global', {
            'fields': ('periodicidad', 'meses', 'anio'),
            'classes': ('collapse',)
        }),
        ('Estatus SAT', {
            'fields': (
                'estatus_sat', 'fecha_ultima_verificacion',
                'motivo_cancelacion', 'fecha_cancelacion'
            )
        }),
        ('Propiedades Calculadas', {
            'fields': ('es_emitido', 'es_recibido', 'es_venta', 'es_compra'),
            'classes': ('collapse',)
        }),
        ('XML Original', {
            'fields': ('xml_original',),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Detalle)
class DetalleAdmin(admin.ModelAdmin):
    list_display = [
        'comprobante', 'numero_linea', 'descripcion',
        'cantidad', 'valor_unitario', 'importe'
    ]
    list_filter = ['comprobante__empresa']
    search_fields = ['comprobante__uuid', 'descripcion', 'no_identificacion']


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = [
        'num_empleado', 'curp', 'empresa', 'departamento',
        'puesto', 'activo'
    ]
    list_filter = ['activo', 'empresa', 'departamento']
    search_fields = ['num_empleado', 'curp', 'puesto']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = [
        'comprobante', 'empleado', 'tipo_nomina', 'fecha_pago',
        'total_percepciones', 'total_deducciones'
    ]
    list_filter = ['tipo_nomina', 'fecha_pago']
    search_fields = ['comprobante__uuid', 'empleado__num_empleado']
    date_hierarchy = 'fecha_pago'


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['comprobante', 'fecha_pago', 'forma_pago', 'moneda', 'monto']
    list_filter = ['forma_pago', 'moneda', 'fecha_pago']
    search_fields = ['comprobante__uuid', 'num_operacion']
    date_hierarchy = 'fecha_pago'


@admin.register(ProveedorCliente)
class ProveedorClienteAdmin(admin.ModelAdmin):
    list_display = [
        'empresa', 'entidad', 'tipo', 'neto_operaciones',
        'persona_contacto', 'activo'
    ]
    list_filter = ['tipo', 'activo', 'empresa']
    search_fields = [
        'entidad__rfc', 'entidad__nombre', 'persona_contacto',
        'correo_contacto'
    ]
    readonly_fields = ['created_at', 'updated_at', 'neto_operaciones']


@admin.register(ArticuloNormalizado)
class ArticuloNormalizadoAdmin(admin.ModelAdmin):
    list_display = [
        'descripcion_normalizada', 'empresa', 'veces_comprado',
        'precio_promedio', 'precio_minimo', 'precio_maximo', 'activo'
    ]
    list_filter = ['activo', 'empresa']
    search_fields = ['descripcion_normalizada']
    readonly_fields = [
        'created_at', 'updated_at', 'veces_comprado',
        'precio_promedio', 'precio_minimo', 'precio_maximo'
    ]


@admin.register(ArticuloAlias)
class ArticuloAliasAdmin(admin.ModelAdmin):
    list_display = [
        'alias', 'descripcion_normalizada', 'articulo_normalizado',
        'empresa', 'activo'
    ]
    list_filter = ['activo', 'empresa']
    search_fields = ['alias', 'descripcion_normalizada']


# Registrar los demás modelos de forma simple
admin.site.register(ImpuestoComprobante)
admin.site.register(ImpuestoDetalle)
admin.site.register(PagoDocumentoRelacionado)
admin.site.register(NominaConcepto)
