"""
Configuración del admin para empresas
"""
from django.contrib import admin
from .models import Empresa, UsuarioEmpresa, EmpresaRegimen


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['rfc', 'nombre', 'activo', 'fecha_alta', 'codigo_postal']
    list_filter = ['activo', 'fecha_alta']
    search_fields = ['rfc', 'nombre']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    fieldsets = (
        ('Información Básica', {
            'fields': ('rfc', 'nombre', 'giro_actividad', 'fecha_alta', 'activo')
        }),
        ('Domicilio Fiscal', {
            'fields': ('domicilio_fiscal', 'codigo_postal')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UsuarioEmpresa)
class UsuarioEmpresaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'empresa', 'rol', 'activo', 'fecha_asignacion']
    list_filter = ['rol', 'activo', 'fecha_asignacion', 'empresa']
    search_fields = ['usuario__username', 'empresa__nombre', 'empresa__rfc']
    readonly_fields = ['fecha_asignacion', 'created_at', 'updated_at']

    fieldsets = (
        ('Asignación', {
            'fields': ('usuario', 'empresa', 'rol', 'activo')
        }),
        ('Información Adicional', {
            'fields': ('notas', 'fecha_asignacion')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EmpresaRegimen)
class EmpresaRegimenAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'regimen_fiscal', 'fecha_inicio', 'fecha_fin']
    list_filter = ['regimen_fiscal', 'fecha_inicio']
    search_fields = ['empresa__nombre', 'empresa__rfc', 'regimen_fiscal__descripcion']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Régimen', {
            'fields': ('empresa', 'regimen_fiscal')
        }),
        ('Vigencia', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Notas', {
            'fields': ('notas',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
