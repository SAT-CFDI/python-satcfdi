"""
Catálogos del SAT para la plataforma CFDI
"""
from django.db import models
from core.models import CatalogoSATBase


class RegimenFiscal(CatalogoSATBase):
    """Catálogo de Regímenes Fiscales del SAT"""
    persona_fisica = models.BooleanField(
        'Aplica a Persona Física',
        default=False,
        help_text='Indica si aplica a personas físicas'
    )
    persona_moral = models.BooleanField(
        'Aplica a Persona Moral',
        default=False,
        help_text='Indica si aplica a personas morales'
    )

    class Meta:
        verbose_name = 'Régimen Fiscal'
        verbose_name_plural = 'Regímenes Fiscales'
        db_table = 'cat_regimen_fiscal'


class UsoCFDI(CatalogoSATBase):
    """Catálogo de Usos del CFDI"""
    persona_fisica = models.BooleanField(
        'Aplica a Persona Física',
        default=False
    )
    persona_moral = models.BooleanField(
        'Aplica a Persona Moral',
        default=False
    )
    regimen_fiscal = models.ManyToManyField(
        RegimenFiscal,
        blank=True,
        verbose_name='Regímenes Fiscales',
        help_text='Regímenes fiscales a los que aplica este uso'
    )

    class Meta:
        verbose_name = 'Uso de CFDI'
        verbose_name_plural = 'Usos de CFDI'
        db_table = 'cat_uso_cfdi'


class FormaPago(CatalogoSATBase):
    """Catálogo de Formas de Pago"""
    bancarizado = models.BooleanField(
        'Bancarizado',
        default=False,
        help_text='Indica si la forma de pago requiere operación bancaria'
    )
    numero_operacion = models.BooleanField(
        'Número de Operación',
        default=False,
        help_text='Indica si requiere número de operación'
    )
    cuenta_ordenante = models.BooleanField(
        'Cuenta Ordenante',
        default=False,
        help_text='Indica si requiere cuenta ordenante'
    )
    cuenta_beneficiario = models.BooleanField(
        'Cuenta Beneficiario',
        default=False,
        help_text='Indica si requiere cuenta beneficiario'
    )
    tipo_cadena_pago = models.BooleanField(
        'Tipo Cadena Pago',
        default=False,
        help_text='Indica si requiere tipo de cadena de pago'
    )

    class Meta:
        verbose_name = 'Forma de Pago'
        verbose_name_plural = 'Formas de Pago'
        db_table = 'cat_forma_pago'


class MetodoPago(CatalogoSATBase):
    """Catálogo de Métodos de Pago"""

    class Meta:
        verbose_name = 'Método de Pago'
        verbose_name_plural = 'Métodos de Pago'
        db_table = 'cat_metodo_pago'


class TipoComprobante(CatalogoSATBase):
    """Catálogo de Tipos de Comprobante"""
    valor_maximo = models.DecimalField(
        'Valor Máximo',
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor máximo permitido para este tipo de comprobante'
    )

    class Meta:
        verbose_name = 'Tipo de Comprobante'
        verbose_name_plural = 'Tipos de Comprobante'
        db_table = 'cat_tipo_comprobante'


class Moneda(CatalogoSATBase):
    """Catálogo de Monedas"""
    decimales = models.IntegerField(
        'Decimales',
        default=2,
        help_text='Número de decimales que maneja la moneda'
    )
    porcentaje_variacion = models.IntegerField(
        'Porcentaje Variación',
        default=10,
        help_text='Porcentaje de variación aceptable'
    )

    class Meta:
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'
        db_table = 'cat_moneda'


class ClaveProdServ(CatalogoSATBase):
    """Catálogo de Productos y Servicios"""
    incluye_iva = models.BooleanField(
        'Incluye IVA',
        default=False,
        help_text='Indica si incluye IVA'
    )
    incluye_ieps = models.BooleanField(
        'Incluye IEPS',
        default=False,
        help_text='Indica si incluye IEPS'
    )
    complemento = models.CharField(
        'Complemento',
        max_length=100,
        blank=True,
        help_text='Complemento que debe incluir'
    )
    similar = models.CharField(
        'Palabras Similares',
        max_length=500,
        blank=True,
        help_text='Palabras similares para búsqueda'
    )

    class Meta:
        verbose_name = 'Clave de Producto/Servicio'
        verbose_name_plural = 'Claves de Productos/Servicios'
        db_table = 'cat_clave_prod_serv'


class ClaveUnidad(CatalogoSATBase):
    """Catálogo de Claves de Unidad"""
    nombre = models.CharField(
        'Nombre',
        max_length=200,
        help_text='Nombre de la unidad'
    )
    simbolo = models.CharField(
        'Símbolo',
        max_length=20,
        blank=True,
        help_text='Símbolo de la unidad'
    )

    class Meta:
        verbose_name = 'Clave de Unidad'
        verbose_name_plural = 'Claves de Unidad'
        db_table = 'cat_clave_unidad'


class Impuesto(CatalogoSATBase):
    """Catálogo de Impuestos"""
    retencion = models.BooleanField(
        'Retención',
        default=False,
        help_text='Indica si es un impuesto de retención'
    )
    traslado = models.BooleanField(
        'Traslado',
        default=False,
        help_text='Indica si es un impuesto trasladado'
    )
    local = models.BooleanField(
        'Local',
        default=False,
        help_text='Indica si es un impuesto local'
    )
    federal = models.BooleanField(
        'Federal',
        default=True,
        help_text='Indica si es un impuesto federal'
    )

    class Meta:
        verbose_name = 'Impuesto'
        verbose_name_plural = 'Impuestos'
        db_table = 'cat_impuesto'


class TipoFactor(CatalogoSATBase):
    """Catálogo de Tipos de Factor"""

    class Meta:
        verbose_name = 'Tipo de Factor'
        verbose_name_plural = 'Tipos de Factor'
        db_table = 'cat_tipo_factor'


class Exportacion(CatalogoSATBase):
    """Catálogo de Exportación"""

    class Meta:
        verbose_name = 'Exportación'
        verbose_name_plural = 'Exportaciones'
        db_table = 'cat_exportacion'


class ObjetoImp(CatalogoSATBase):
    """Catálogo de Objeto de Impuestos"""

    class Meta:
        verbose_name = 'Objeto de Impuesto'
        verbose_name_plural = 'Objetos de Impuestos'
        db_table = 'cat_objeto_imp'


class Periodicidad(CatalogoSATBase):
    """Catálogo de Periodicidad"""

    class Meta:
        verbose_name = 'Periodicidad'
        verbose_name_plural = 'Periodicidades'
        db_table = 'cat_periodicidad'


class Meses(CatalogoSATBase):
    """Catálogo de Meses"""

    class Meta:
        verbose_name = 'Mes'
        verbose_name_plural = 'Meses'
        db_table = 'cat_meses'


class TipoNomina(CatalogoSATBase):
    """Catálogo de Tipos de Nómina"""

    class Meta:
        verbose_name = 'Tipo de Nómina'
        verbose_name_plural = 'Tipos de Nómina'
        db_table = 'cat_tipo_nomina'


class TipoContrato(CatalogoSATBase):
    """Catálogo de Tipos de Contrato"""

    class Meta:
        verbose_name = 'Tipo de Contrato'
        verbose_name_plural = 'Tipos de Contrato'
        db_table = 'cat_tipo_contrato'


class TipoPercepcion(CatalogoSATBase):
    """Catálogo de Tipos de Percepción"""
    ingreso_acumulable = models.BooleanField(
        'Ingreso Acumulable',
        default=False,
        help_text='Indica si es ingreso acumulable'
    )

    class Meta:
        verbose_name = 'Tipo de Percepción'
        verbose_name_plural = 'Tipos de Percepción'
        db_table = 'cat_tipo_percepcion'


class TipoDeduccion(CatalogoSATBase):
    """Catálogo de Tipos de Deducción"""

    class Meta:
        verbose_name = 'Tipo de Deducción'
        verbose_name_plural = 'Tipos de Deducción'
        db_table = 'cat_tipo_deduccion'


class TipoOtroPago(CatalogoSATBase):
    """Catálogo de Tipos de Otro Pago"""

    class Meta:
        verbose_name = 'Tipo de Otro Pago'
        verbose_name_plural = 'Tipos de Otros Pagos'
        db_table = 'cat_tipo_otro_pago'


class PeriodicidadPago(CatalogoSATBase):
    """Catálogo de Periodicidad de Pago"""

    class Meta:
        verbose_name = 'Periodicidad de Pago'
        verbose_name_plural = 'Periodicidades de Pago'
        db_table = 'cat_periodicidad_pago'


class TipoJornada(CatalogoSATBase):
    """Catálogo de Tipos de Jornada"""

    class Meta:
        verbose_name = 'Tipo de Jornada'
        verbose_name_plural = 'Tipos de Jornada'
        db_table = 'cat_tipo_jornada'


class TipoRegimen(CatalogoSATBase):
    """Catálogo de Tipos de Régimen (Laboral)"""

    class Meta:
        verbose_name = 'Tipo de Régimen Laboral'
        verbose_name_plural = 'Tipos de Régimen Laboral'
        db_table = 'cat_tipo_regimen'


class Banco(CatalogoSATBase):
    """Catálogo de Bancos"""
    razon_social = models.CharField(
        'Razón Social',
        max_length=300,
        help_text='Razón social del banco'
    )

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        db_table = 'cat_banco'


class TipoRelacion(CatalogoSATBase):
    """Catálogo de Tipos de Relación entre CFDI"""

    class Meta:
        verbose_name = 'Tipo de Relación'
        verbose_name_plural = 'Tipos de Relación'
        db_table = 'cat_tipo_relacion'


class Pais(CatalogoSATBase):
    """Catálogo de Países"""
    formato_codigo_postal = models.CharField(
        'Formato Código Postal',
        max_length=50,
        blank=True,
        help_text='Formato del código postal para validación'
    )
    agrupaciones = models.CharField(
        'Agrupaciones',
        max_length=200,
        blank=True,
        help_text='Agrupaciones a las que pertenece (UE, TLCAN, etc.)'
    )

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        db_table = 'cat_pais'


class Estado(models.Model):
    """Catálogo de Estados de México"""
    clave = models.CharField(
        'Clave',
        max_length=3,
        unique=True,
        help_text='Clave del estado'
    )
    nombre = models.CharField(
        'Nombre',
        max_length=100,
        help_text='Nombre del estado'
    )
    pais = models.ForeignKey(
        Pais,
        on_delete=models.CASCADE,
        related_name='estados',
        verbose_name='País'
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        db_table = 'cat_estado'
        ordering = ['clave']

    def __str__(self):
        return f"{self.clave} - {self.nombre}"


class Municipio(models.Model):
    """Catálogo de Municipios de México"""
    clave = models.CharField(
        'Clave',
        max_length=3,
        help_text='Clave del municipio'
    )
    nombre = models.CharField(
        'Nombre',
        max_length=100,
        help_text='Nombre del municipio'
    )
    estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE,
        related_name='municipios',
        verbose_name='Estado'
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )

    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        db_table = 'cat_municipio'
        ordering = ['estado', 'clave']
        unique_together = [['estado', 'clave']]

    def __str__(self):
        return f"{self.estado.clave}{self.clave} - {self.nombre}"


class CodigoPostal(models.Model):
    """Catálogo de Códigos Postales de México"""
    codigo_postal = models.CharField(
        'Código Postal',
        max_length=5,
        unique=True,
        help_text='Código postal'
    )
    estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE,
        related_name='codigos_postales',
        verbose_name='Estado'
    )
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.CASCADE,
        related_name='codigos_postales',
        verbose_name='Municipio',
        null=True,
        blank=True
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )

    class Meta:
        verbose_name = 'Código Postal'
        verbose_name_plural = 'Códigos Postales'
        db_table = 'cat_codigo_postal'
        ordering = ['codigo_postal']

    def __str__(self):
        return self.codigo_postal
