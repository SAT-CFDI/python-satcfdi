"""
Configuración del admin para catálogos SAT
"""
from django.contrib import admin
from .models import (
    RegimenFiscal, UsoCFDI, FormaPago, MetodoPago, TipoComprobante,
    Moneda, ClaveProdServ, ClaveUnidad, Impuesto, TipoFactor,
    Exportacion, ObjetoImp, Periodicidad, Meses, TipoNomina,
    TipoContrato, TipoPercepcion, TipoDeduccion, TipoOtroPago,
    PeriodicidadPago, TipoJornada, TipoRegimen, Banco, TipoRelacion,
    Pais, Estado, Municipio, CodigoPostal
)


@admin.register(RegimenFiscal)
class RegimenFiscalAdmin(admin.ModelAdmin):
    list_display = ['clave', 'descripcion', 'persona_fisica', 'persona_moral', 'activo']
    list_filter = ['activo', 'persona_fisica', 'persona_moral']
    search_fields = ['clave', 'descripcion']


@admin.register(UsoCFDI)
class UsoCFDIAdmin(admin.ModelAdmin):
    list_display = ['clave', 'descripcion', 'persona_fisica', 'persona_moral', 'activo']
    list_filter = ['activo', 'persona_fisica', 'persona_moral']
    search_fields = ['clave', 'descripcion']


@admin.register(FormaPago)
class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ['clave', 'descripcion', 'bancarizado', 'activo']
    list_filter = ['activo', 'bancarizado']
    search_fields = ['clave', 'descripcion']


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ['clave', 'descripcion', 'activo']
    list_filter = ['activo']
    search_fields = ['clave', 'descripcion']


@admin.register(TipoComprobante)
class TipoComprobanteAdmin(admin.ModelAdmin):
    list_display = ['clave', 'descripcion', 'activo']
    list_filter = ['activo']
    search_fields = ['clave', 'descripcion']


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ['clave', 'descripcion', 'decimales', 'activo']
    list_filter = ['activo']
    search_fields = ['clave', 'descripcion']


@admin.register(ClaveProdServ)
class ClaveProdServAdmin(admin.ModelAdmin):
    list_display = ['clave', 'descripcion', 'incluye_iva', 'incluye_ieps', 'activo']
    list_filter = ['activo', 'incluye_iva', 'incluye_ieps']
    search_fields = ['clave', 'descripcion', 'similar']


@admin.register(ClaveUnidad)
class ClaveUnidadAdmin(admin.ModelAdmin):
    list_display = ['clave', 'nombre', 'simbolo', 'activo']
    list_filter = ['activo']
    search_fields = ['clave', 'nombre', 'simbolo']


@admin.register(Impuesto)
class ImpuestoAdmin(admin.ModelAdmin):
    list_display = ['clave', 'descripcion', 'retencion', 'traslado', 'activo']
    list_filter = ['activo', 'retencion', 'traslado', 'federal', 'local']
    search_fields = ['clave', 'descripcion']


# Registrar los demás catálogos de forma simple
admin.site.register(TipoFactor)
admin.site.register(Exportacion)
admin.site.register(ObjetoImp)
admin.site.register(Periodicidad)
admin.site.register(Meses)
admin.site.register(TipoNomina)
admin.site.register(TipoContrato)
admin.site.register(TipoPercepcion)
admin.site.register(TipoDeduccion)
admin.site.register(TipoOtroPago)
admin.site.register(PeriodicidadPago)
admin.site.register(TipoJornada)
admin.site.register(TipoRegimen)
admin.site.register(Banco)
admin.site.register(TipoRelacion)


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ['clave', 'descripcion', 'activo']
    list_filter = ['activo']
    search_fields = ['clave', 'descripcion']


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ['clave', 'nombre', 'pais', 'activo']
    list_filter = ['activo', 'pais']
    search_fields = ['clave', 'nombre']


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ['clave', 'nombre', 'estado', 'activo']
    list_filter = ['activo', 'estado']
    search_fields = ['clave', 'nombre']


@admin.register(CodigoPostal)
class CodigoPostalAdmin(admin.ModelAdmin):
    list_display = ['codigo_postal', 'estado', 'municipio', 'activo']
    list_filter = ['activo', 'estado']
    search_fields = ['codigo_postal']
