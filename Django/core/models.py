"""
Modelos base para la plataforma CFDI
"""
from django.db import models
from django.contrib.auth.models import User


class AuditMixin(models.Model):
    """
    Mixin para auditoría de modelos.
    Agrega campos de creación y modificación automáticos.
    """
    created_at = models.DateTimeField(
        'Fecha de creación',
        auto_now_add=True,
        help_text='Fecha y hora de creación del registro'
    )
    updated_at = models.DateTimeField(
        'Fecha de actualización',
        auto_now=True,
        help_text='Fecha y hora de última actualización del registro'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name='Creado por',
        help_text='Usuario que creó el registro'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name='Actualizado por',
        help_text='Usuario que actualizó el registro por última vez'
    )

    class Meta:
        abstract = True


class CatalogoSATBase(models.Model):
    """
    Clase base para catálogos del SAT.
    Todos los catálogos SAT heredan de esta clase.
    """
    clave = models.CharField(
        'Clave',
        max_length=10,
        unique=True,
        help_text='Clave del catálogo SAT'
    )
    descripcion = models.CharField(
        'Descripción',
        max_length=500,
        help_text='Descripción del catálogo'
    )
    activo = models.BooleanField(
        'Activo',
        default=True,
        help_text='Indica si el catálogo está activo'
    )
    fecha_inicio_vigencia = models.DateField(
        'Fecha inicio vigencia',
        null=True,
        blank=True,
        help_text='Fecha de inicio de vigencia del catálogo'
    )
    fecha_fin_vigencia = models.DateField(
        'Fecha fin vigencia',
        null=True,
        blank=True,
        help_text='Fecha de fin de vigencia del catálogo'
    )

    class Meta:
        abstract = True
        ordering = ['clave']

    def __str__(self):
        return f"{self.clave} - {self.descripcion}"
