"""
Modelos para gestión de empresas
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from core.models import AuditMixin
from catalogos.models import RegimenFiscal
import re


# Validadores
rfc_validator = RegexValidator(
    regex=r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$',
    message='El RFC no tiene un formato válido. Debe ser de 12 o 13 caracteres.'
)


class Empresa(AuditMixin):
    """
    Modelo para representar una empresa
    """
    nombre = models.CharField(
        'Nombre',
        max_length=200,
        help_text='Nombre o razón social de la empresa'
    )
    rfc = models.CharField(
        'RFC',
        max_length=13,
        unique=True,
        validators=[rfc_validator],
        help_text='RFC de la empresa (12 o 13 caracteres)'
    )
    giro_actividad = models.CharField(
        'Giro o Actividad',
        max_length=200,
        blank=True,
        help_text='Giro o actividad principal de la empresa'
    )
    fecha_alta = models.DateField(
        'Fecha de Alta',
        help_text='Fecha de alta ante el SAT'
    )
    activo = models.BooleanField(
        'Activo',
        default=True,
        help_text='Indica si la empresa está activa'
    )
    domicilio_fiscal = models.CharField(
        'Domicilio Fiscal',
        max_length=300,
        help_text='Domicilio fiscal completo'
    )
    codigo_postal = models.CharField(
        'Código Postal',
        max_length=5,
        validators=[RegexValidator(
            regex=r'^\d{5}$',
            message='El código postal debe tener 5 dígitos'
        )],
        help_text='Código postal del domicilio fiscal'
    )
    telefono = models.CharField(
        'Teléfono',
        max_length=15,
        blank=True,
        help_text='Teléfono de contacto'
    )
    email = models.EmailField(
        'Email',
        help_text='Email de contacto'
    )

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        db_table = 'empresa'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.rfc} - {self.nombre}"

    def clean(self):
        """Validación personalizada"""
        if self.rfc:
            self.rfc = self.rfc.upper().strip()
            # Validar que el RFC sea válido según su longitud
            if len(self.rfc) not in [12, 13]:
                raise ValidationError({
                    'rfc': 'El RFC debe tener 12 o 13 caracteres'
                })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def es_persona_fisica(self):
        """Determina si es persona física según la longitud del RFC"""
        return len(self.rfc) == 13

    @property
    def es_persona_moral(self):
        """Determina si es persona moral según la longitud del RFC"""
        return len(self.rfc) == 12


class UsuarioEmpresa(AuditMixin):
    """
    Relación entre usuarios y empresas con roles
    """
    ROLES = [
        ('admin', 'Administrador'),
        ('capturista', 'Capturista'),
        ('consulta', 'Consulta'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='empresas_asignadas',
        verbose_name='Usuario'
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='usuarios',
        verbose_name='Empresa'
    )
    rol = models.CharField(
        'Rol',
        max_length=20,
        choices=ROLES,
        default='consulta',
        help_text='Rol del usuario en la empresa'
    )
    activo = models.BooleanField(
        'Activo',
        default=True,
        help_text='Indica si la asignación está activa'
    )
    fecha_asignacion = models.DateTimeField(
        'Fecha de Asignación',
        auto_now_add=True,
        help_text='Fecha en que se asignó el usuario a la empresa'
    )
    notas = models.TextField(
        'Notas',
        blank=True,
        help_text='Notas adicionales sobre la asignación'
    )

    class Meta:
        verbose_name = 'Usuario Empresa'
        verbose_name_plural = 'Usuarios Empresas'
        db_table = 'usuario_empresa'
        unique_together = [['usuario', 'empresa']]
        ordering = ['empresa', 'usuario']

    def __str__(self):
        return f"{self.usuario.username} - {self.empresa.nombre} ({self.rol})"


class EmpresaRegimen(AuditMixin):
    """
    Regímenes fiscales de una empresa en diferentes períodos
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='regimenes',
        verbose_name='Empresa'
    )
    regimen_fiscal = models.ForeignKey(
        RegimenFiscal,
        on_delete=models.PROTECT,
        related_name='empresas',
        verbose_name='Régimen Fiscal'
    )
    fecha_inicio = models.DateField(
        'Fecha de Inicio',
        help_text='Fecha de inicio de vigencia del régimen'
    )
    fecha_fin = models.DateField(
        'Fecha de Fin',
        null=True,
        blank=True,
        help_text='Fecha de fin de vigencia del régimen'
    )
    notas = models.TextField(
        'Notas',
        blank=True,
        help_text='Notas adicionales sobre el régimen'
    )

    class Meta:
        verbose_name = 'Régimen Fiscal de Empresa'
        verbose_name_plural = 'Regímenes Fiscales de Empresas'
        db_table = 'empresa_regimen'
        ordering = ['empresa', '-fecha_inicio']

    def __str__(self):
        return f"{self.empresa.rfc} - {self.regimen_fiscal.clave} ({self.fecha_inicio})"

    def clean(self):
        """Validación personalizada"""
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin < self.fecha_inicio:
                raise ValidationError({
                    'fecha_fin': 'La fecha de fin no puede ser anterior a la fecha de inicio'
                })
