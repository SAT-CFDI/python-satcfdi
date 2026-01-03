"""
Modelos para gestión de comprobantes CFDI
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from decimal import Decimal
from core.models import AuditMixin
from empresas.models import Empresa, rfc_validator
from catalogos.models import (
    RegimenFiscal, TipoComprobante, UsoCFDI, FormaPago, MetodoPago,
    Moneda, Exportacion, Periodicidad, Meses, ClaveProdServ, ClaveUnidad,
    Impuesto, TipoFactor, ObjetoImp, TipoNomina, TipoContrato, TipoRegimen,
    TipoPercepcion, TipoDeduccion, TipoOtroPago, PeriodicidadPago, TipoJornada
)


class Entidad(AuditMixin):
    """
    Representa una entidad (emisor o receptor de CFDI)
    """
    TIPO_PERSONA = [
        ('F', 'Física'),
        ('M', 'Moral'),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='entidades',
        verbose_name='Empresa',
        help_text='Empresa a la que pertenece esta entidad'
    )
    rfc = models.CharField(
        'RFC',
        max_length=13,
        unique=True,
        validators=[rfc_validator],
        help_text='RFC de la entidad'
    )
    nombre = models.CharField(
        'Nombre',
        max_length=300,
        help_text='Nombre o razón social de la entidad'
    )
    tipo = models.CharField(
        'Tipo',
        max_length=1,
        choices=TIPO_PERSONA,
        help_text='Tipo de persona'
    )
    regimen_fiscal_actual = models.ForeignKey(
        RegimenFiscal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entidades',
        verbose_name='Régimen Fiscal Actual'
    )
    total_emitidos = models.IntegerField(
        'Total Emitidos',
        default=0,
        help_text='Total de CFDI emitidos por esta entidad'
    )
    total_recibidos = models.IntegerField(
        'Total Recibidos',
        default=0,
        help_text='Total de CFDI recibidos por esta entidad'
    )
    fecha_primer_cfdi = models.DateTimeField(
        'Fecha Primer CFDI',
        null=True,
        blank=True,
        help_text='Fecha del primer CFDI registrado'
    )
    fecha_ultimo_cfdi = models.DateTimeField(
        'Fecha Último CFDI',
        null=True,
        blank=True,
        help_text='Fecha del último CFDI registrado'
    )

    class Meta:
        verbose_name = 'Entidad'
        verbose_name_plural = 'Entidades'
        db_table = 'entidad'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.rfc} - {self.nombre}"

    def save(self, *args, **kwargs):
        if self.rfc:
            self.rfc = self.rfc.upper().strip()
        super().save(*args, **kwargs)


class Comprobante(AuditMixin):
    """
    Modelo principal para comprobantes CFDI
    """
    uuid = models.CharField(
        'UUID',
        max_length=36,
        unique=True,
        help_text='UUID del comprobante (folio fiscal)'
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='comprobantes',
        verbose_name='Empresa'
    )
    emisor = models.ForeignKey(
        Entidad,
        on_delete=models.PROTECT,
        related_name='comprobantes_emitidos',
        verbose_name='Emisor'
    )
    receptor = models.ForeignKey(
        Entidad,
        on_delete=models.PROTECT,
        related_name='comprobantes_recibidos',
        verbose_name='Receptor'
    )
    fecha_emision = models.DateTimeField(
        'Fecha de Emisión',
        help_text='Fecha y hora de emisión del comprobante'
    )
    fecha_timbrado = models.DateTimeField(
        'Fecha de Timbrado',
        help_text='Fecha y hora de timbrado del comprobante'
    )
    tipo_comprobante = models.ForeignKey(
        TipoComprobante,
        on_delete=models.PROTECT,
        related_name='comprobantes',
        verbose_name='Tipo de Comprobante'
    )
    uso_cfdi = models.ForeignKey(
        UsoCFDI,
        on_delete=models.PROTECT,
        related_name='comprobantes',
        verbose_name='Uso CFDI'
    )
    version = models.CharField(
        'Versión',
        max_length=3,
        default='4.0',
        help_text='Versión del CFDI'
    )
    serie = models.CharField(
        'Serie',
        max_length=25,
        blank=True,
        help_text='Serie del comprobante'
    )
    folio = models.CharField(
        'Folio',
        max_length=40,
        blank=True,
        help_text='Folio del comprobante'
    )
    lugar_expedicion = models.CharField(
        'Lugar de Expedición',
        max_length=5,
        help_text='Código postal del lugar de expedición'
    )
    exportacion = models.ForeignKey(
        Exportacion,
        on_delete=models.PROTECT,
        related_name='comprobantes',
        verbose_name='Exportación'
    )
    moneda = models.ForeignKey(
        Moneda,
        on_delete=models.PROTECT,
        related_name='comprobantes',
        verbose_name='Moneda'
    )
    tipo_cambio = models.DecimalField(
        'Tipo de Cambio',
        max_digits=19,
        decimal_places=6,
        null=True,
        blank=True,
        help_text='Tipo de cambio de la moneda'
    )
    subtotal = models.DecimalField(
        'Subtotal',
        max_digits=19,
        decimal_places=2,
        help_text='Subtotal del comprobante'
    )
    descuento = models.DecimalField(
        'Descuento',
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Descuento total del comprobante'
    )
    impuesto_trasladado_total = models.DecimalField(
        'Impuestos Trasladados Total',
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Total de impuestos trasladados'
    )
    impuesto_retenido_total = models.DecimalField(
        'Impuestos Retenidos Total',
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Total de impuestos retenidos'
    )
    total = models.DecimalField(
        'Total',
        max_digits=19,
        decimal_places=2,
        help_text='Total del comprobante'
    )
    metodo_pago = models.ForeignKey(
        MetodoPago,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='comprobantes',
        verbose_name='Método de Pago'
    )
    forma_pago = models.ForeignKey(
        FormaPago,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='comprobantes',
        verbose_name='Forma de Pago'
    )
    condiciones_pago = models.CharField(
        'Condiciones de Pago',
        max_length=1000,
        blank=True,
        help_text='Condiciones de pago'
    )
    periodicidad = models.ForeignKey(
        Periodicidad,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='comprobantes',
        verbose_name='Periodicidad'
    )
    meses = models.ForeignKey(
        Meses,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='comprobantes',
        verbose_name='Meses'
    )
    anio = models.IntegerField(
        'Año',
        null=True,
        blank=True,
        help_text='Año del comprobante global'
    )
    estatus_sat = models.CharField(
        'Estatus SAT',
        max_length=20,
        default='VIGENTE',
        help_text='Estatus del comprobante en el SAT'
    )
    fecha_ultima_verificacion = models.DateTimeField(
        'Fecha Última Verificación',
        null=True,
        blank=True,
        help_text='Fecha de última verificación con el SAT'
    )
    motivo_cancelacion = models.CharField(
        'Motivo de Cancelación',
        max_length=200,
        blank=True,
        help_text='Motivo de cancelación del comprobante'
    )
    fecha_cancelacion = models.DateTimeField(
        'Fecha de Cancelación',
        null=True,
        blank=True,
        help_text='Fecha en que se canceló el comprobante'
    )
    xml_original = models.TextField(
        'XML Original',
        help_text='Contenido XML original del comprobante'
    )

    class Meta:
        verbose_name = 'Comprobante'
        verbose_name_plural = 'Comprobantes'
        db_table = 'comprobante'
        ordering = ['-fecha_emision']
        indexes = [
            models.Index(fields=['uuid']),
            models.Index(fields=['empresa', 'fecha_emision']),
            models.Index(fields=['emisor', 'receptor']),
        ]

    def __str__(self):
        return f"{self.uuid} - {self.emisor.rfc} - ${self.total}"

    @property
    def es_emitido(self):
        """Indica si el comprobante fue emitido por la empresa"""
        return self.emisor.rfc == self.empresa.rfc

    @property
    def es_recibido(self):
        """Indica si el comprobante fue recibido por la empresa"""
        return self.receptor.rfc == self.empresa.rfc

    @property
    def es_venta(self):
        """Indica si es un comprobante de venta (ingreso emitido)"""
        return self.es_emitido and self.tipo_comprobante.clave == 'I'

    @property
    def es_compra(self):
        """Indica si es un comprobante de compra (ingreso recibido)"""
        return self.es_recibido and self.tipo_comprobante.clave == 'I'

    @property
    def es_pago(self):
        """Indica si es un complemento de pago"""
        return self.tipo_comprobante.clave == 'P'

    @property
    def es_nomina(self):
        """Indica si es un comprobante de nómina"""
        return self.tipo_comprobante.clave == 'N'

    @property
    def es_deducible(self):
        """Indica si el comprobante es deducible"""
        # Lógica simplificada, puede ser más compleja según reglas de negocio
        return self.es_compra and self.tipo_comprobante.clave in ['I', 'E']


class Detalle(models.Model):
    """
    Detalles (conceptos) del comprobante
    """
    comprobante = models.ForeignKey(
        Comprobante,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Comprobante'
    )
    numero_linea = models.IntegerField(
        'Número de Línea',
        help_text='Número de línea del concepto'
    )
    clave_prod_serv = models.ForeignKey(
        ClaveProdServ,
        on_delete=models.PROTECT,
        related_name='detalles',
        verbose_name='Clave Producto/Servicio'
    )
    no_identificacion = models.CharField(
        'Número de Identificación',
        max_length=100,
        blank=True,
        help_text='Número de identificación del producto/servicio'
    )
    cantidad = models.DecimalField(
        'Cantidad',
        max_digits=19,
        decimal_places=6,
        help_text='Cantidad del producto/servicio'
    )
    clave_unidad = models.ForeignKey(
        ClaveUnidad,
        on_delete=models.PROTECT,
        related_name='detalles',
        verbose_name='Clave Unidad'
    )
    unidad = models.CharField(
        'Unidad',
        max_length=50,
        blank=True,
        help_text='Unidad de medida'
    )
    descripcion = models.TextField(
        'Descripción',
        help_text='Descripción del producto/servicio'
    )
    valor_unitario = models.DecimalField(
        'Valor Unitario',
        max_digits=19,
        decimal_places=6,
        help_text='Valor unitario del producto/servicio'
    )
    importe = models.DecimalField(
        'Importe',
        max_digits=19,
        decimal_places=2,
        help_text='Importe del concepto (cantidad * valor unitario)'
    )
    descuento = models.DecimalField(
        'Descuento',
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Descuento aplicado al concepto'
    )
    articulo_normalizado = models.ForeignKey(
        'ArticuloNormalizado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='detalles',
        verbose_name='Artículo Normalizado'
    )
    objeto_imp = models.ForeignKey(
        ObjetoImp,
        on_delete=models.PROTECT,
        related_name='detalles',
        verbose_name='Objeto de Impuesto'
    )

    class Meta:
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'
        db_table = 'detalle'
        ordering = ['comprobante', 'numero_linea']

    def __str__(self):
        return f"{self.comprobante.uuid} - Línea {self.numero_linea}: {self.descripcion[:50]}"


class ImpuestoComprobante(models.Model):
    """
    Impuestos a nivel comprobante (resumen)
    """
    TIPO_IMPUESTO = [
        ('traslado', 'Traslado'),
        ('retencion', 'Retención'),
    ]

    comprobante = models.ForeignKey(
        Comprobante,
        on_delete=models.CASCADE,
        related_name='impuestos',
        verbose_name='Comprobante'
    )
    tipo = models.CharField(
        'Tipo',
        max_length=10,
        choices=TIPO_IMPUESTO,
        help_text='Tipo de impuesto (traslado o retención)'
    )
    impuesto = models.ForeignKey(
        Impuesto,
        on_delete=models.PROTECT,
        related_name='impuestos_comprobante',
        verbose_name='Impuesto'
    )
    tipo_factor = models.ForeignKey(
        TipoFactor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='impuestos_comprobante',
        verbose_name='Tipo de Factor'
    )
    tasa_cuota = models.DecimalField(
        'Tasa o Cuota',
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True,
        help_text='Tasa o cuota del impuesto'
    )
    importe = models.DecimalField(
        'Importe',
        max_digits=19,
        decimal_places=2,
        help_text='Importe del impuesto'
    )

    class Meta:
        verbose_name = 'Impuesto de Comprobante'
        verbose_name_plural = 'Impuestos de Comprobantes'
        db_table = 'impuesto_comprobante'


class ImpuestoDetalle(models.Model):
    """
    Impuestos a nivel detalle (concepto)
    """
    TIPO_IMPUESTO = [
        ('traslado', 'Traslado'),
        ('retencion', 'Retención'),
    ]

    detalle = models.ForeignKey(
        Detalle,
        on_delete=models.CASCADE,
        related_name='impuestos',
        verbose_name='Detalle'
    )
    tipo = models.CharField(
        'Tipo',
        max_length=10,
        choices=TIPO_IMPUESTO,
        help_text='Tipo de impuesto (traslado o retención)'
    )
    impuesto = models.ForeignKey(
        Impuesto,
        on_delete=models.PROTECT,
        related_name='impuestos_detalle',
        verbose_name='Impuesto'
    )
    tipo_factor = models.ForeignKey(
        TipoFactor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='impuestos_detalle',
        verbose_name='Tipo de Factor'
    )
    tasa_cuota = models.DecimalField(
        'Tasa o Cuota',
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True,
        help_text='Tasa o cuota del impuesto'
    )
    base = models.DecimalField(
        'Base',
        max_digits=19,
        decimal_places=2,
        help_text='Base del impuesto'
    )
    importe = models.DecimalField(
        'Importe',
        max_digits=19,
        decimal_places=2,
        help_text='Importe del impuesto'
    )

    class Meta:
        verbose_name = 'Impuesto de Detalle'
        verbose_name_plural = 'Impuestos de Detalles'
        db_table = 'impuesto_detalle'


class Pago(models.Model):
    """
    Pagos dentro de un complemento de pago
    """
    comprobante = models.ForeignKey(
        Comprobante,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name='Comprobante'
    )
    fecha_pago = models.DateTimeField(
        'Fecha de Pago',
        help_text='Fecha y hora del pago'
    )
    forma_pago = models.ForeignKey(
        FormaPago,
        on_delete=models.PROTECT,
        related_name='pagos',
        verbose_name='Forma de Pago'
    )
    moneda = models.ForeignKey(
        Moneda,
        on_delete=models.PROTECT,
        related_name='pagos',
        verbose_name='Moneda'
    )
    tipo_cambio = models.DecimalField(
        'Tipo de Cambio',
        max_digits=19,
        decimal_places=6,
        default=Decimal('1.000000'),
        help_text='Tipo de cambio de la moneda del pago'
    )
    monto = models.DecimalField(
        'Monto',
        max_digits=19,
        decimal_places=2,
        help_text='Monto del pago'
    )
    num_operacion = models.CharField(
        'Número de Operación',
        max_length=100,
        blank=True,
        help_text='Número de operación del pago'
    )

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        db_table = 'pago'
        ordering = ['comprobante', 'fecha_pago']


class PagoDocumentoRelacionado(models.Model):
    """
    Documentos relacionados dentro de un pago
    """
    pago = models.ForeignKey(
        Pago,
        on_delete=models.CASCADE,
        related_name='documentos_relacionados',
        verbose_name='Pago'
    )
    uuid_documento = models.CharField(
        'UUID Documento',
        max_length=36,
        help_text='UUID del documento que se está pagando'
    )
    serie = models.CharField(
        'Serie',
        max_length=25,
        blank=True,
        help_text='Serie del documento'
    )
    folio = models.CharField(
        'Folio',
        max_length=40,
        blank=True,
        help_text='Folio del documento'
    )
    moneda = models.ForeignKey(
        Moneda,
        on_delete=models.PROTECT,
        related_name='documentos_relacionados',
        verbose_name='Moneda'
    )
    equivalencia_dr = models.DecimalField(
        'Equivalencia DR',
        max_digits=19,
        decimal_places=6,
        default=Decimal('1.000000'),
        help_text='Equivalencia de la moneda del documento relacionado'
    )
    num_parcialidad = models.IntegerField(
        'Número de Parcialidad',
        help_text='Número de parcialidad que se está pagando'
    )
    saldo_anterior = models.DecimalField(
        'Saldo Anterior',
        max_digits=19,
        decimal_places=2,
        help_text='Saldo anterior del documento'
    )
    importe_pagado = models.DecimalField(
        'Importe Pagado',
        max_digits=19,
        decimal_places=2,
        help_text='Importe pagado en esta parcialidad'
    )
    saldo_insoluto = models.DecimalField(
        'Saldo Insoluto',
        max_digits=19,
        decimal_places=2,
        help_text='Saldo insoluto después del pago'
    )

    class Meta:
        verbose_name = 'Documento Relacionado de Pago'
        verbose_name_plural = 'Documentos Relacionados de Pagos'
        db_table = 'pago_documento_relacionado'


class Empleado(AuditMixin):
    """
    Empleados de la empresa
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='empleados',
        verbose_name='Empresa'
    )
    curp = models.CharField(
        'CURP',
        max_length=18,
        validators=[RegexValidator(
            regex=r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d$',
            message='CURP no válido'
        )],
        help_text='CURP del empleado'
    )
    num_seguridad_social = models.CharField(
        'Número de Seguridad Social',
        max_length=11,
        blank=True,
        help_text='Número de seguridad social del empleado'
    )
    fecha_inicio_rel_laboral = models.DateField(
        'Fecha de Inicio de Relación Laboral',
        help_text='Fecha de inicio de la relación laboral'
    )
    antiguedad = models.CharField(
        'Antigüedad',
        max_length=10,
        blank=True,
        help_text='Antigüedad del empleado (formato SAT)'
    )
    tipo_contrato = models.ForeignKey(
        TipoContrato,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='empleados',
        verbose_name='Tipo de Contrato'
    )
    sindicalizado = models.CharField(
        'Sindicalizado',
        max_length=2,
        choices=[('Si', 'Sí'), ('No', 'No')],
        default='No',
        help_text='Indica si el empleado está sindicalizado'
    )
    tipo_regimen = models.ForeignKey(
        TipoRegimen,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='empleados',
        verbose_name='Tipo de Régimen'
    )
    num_empleado = models.CharField(
        'Número de Empleado',
        max_length=15,
        help_text='Número de empleado interno'
    )
    departamento = models.CharField(
        'Departamento',
        max_length=100,
        blank=True,
        help_text='Departamento al que pertenece'
    )
    puesto = models.CharField(
        'Puesto',
        max_length=100,
        blank=True,
        help_text='Puesto del empleado'
    )
    activo = models.BooleanField(
        'Activo',
        default=True,
        help_text='Indica si el empleado está activo'
    )

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        db_table = 'empleado'
        unique_together = [['empresa', 'num_empleado']]
        ordering = ['empresa', 'num_empleado']

    def __str__(self):
        return f"{self.num_empleado} - {self.curp}"


class Nomina(models.Model):
    """
    Complemento de nómina
    """
    comprobante = models.OneToOneField(
        Comprobante,
        on_delete=models.CASCADE,
        related_name='nomina',
        verbose_name='Comprobante'
    )
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        related_name='nominas',
        verbose_name='Empleado'
    )
    tipo_nomina = models.ForeignKey(
        TipoNomina,
        on_delete=models.PROTECT,
        related_name='nominas',
        verbose_name='Tipo de Nómina'
    )
    fecha_pago = models.DateField(
        'Fecha de Pago',
        help_text='Fecha de pago de la nómina'
    )
    fecha_inicial_pago = models.DateField(
        'Fecha Inicial de Pago',
        help_text='Fecha inicial del período de pago'
    )
    fecha_final_pago = models.DateField(
        'Fecha Final de Pago',
        help_text='Fecha final del período de pago'
    )
    num_dias_pagados = models.DecimalField(
        'Número de Días Pagados',
        max_digits=5,
        decimal_places=3,
        help_text='Número de días pagados'
    )
    salario_base_cot_apor = models.DecimalField(
        'Salario Base de Cotización',
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Salario base de cotización y aportación'
    )
    salario_diario_integrado = models.DecimalField(
        'Salario Diario Integrado',
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Salario diario integrado'
    )
    periodicidad_pago = models.ForeignKey(
        PeriodicidadPago,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='nominas',
        verbose_name='Periodicidad de Pago'
    )
    clave_ent_fed = models.CharField(
        'Clave Entidad Federativa',
        max_length=3,
        blank=True,
        help_text='Clave de la entidad federativa'
    )
    tipo_jornada = models.ForeignKey(
        TipoJornada,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='nominas',
        verbose_name='Tipo de Jornada'
    )
    total_percepciones = models.DecimalField(
        'Total Percepciones',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Total de percepciones'
    )
    total_deducciones = models.DecimalField(
        'Total Deducciones',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Total de deducciones'
    )
    total_otros_pagos = models.DecimalField(
        'Total Otros Pagos',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Total de otros pagos'
    )

    class Meta:
        verbose_name = 'Nómina'
        verbose_name_plural = 'Nóminas'
        db_table = 'nomina'
        ordering = ['-fecha_pago']


class NominaConcepto(models.Model):
    """
    Conceptos de nómina (percepciones, deducciones, otros pagos)
    """
    TIPO_CONCEPTO = [
        ('percepcion', 'Percepción'),
        ('deduccion', 'Deducción'),
        ('otro_pago', 'Otro Pago'),
    ]

    nomina = models.ForeignKey(
        Nomina,
        on_delete=models.CASCADE,
        related_name='conceptos',
        verbose_name='Nómina'
    )
    tipo_concepto = models.CharField(
        'Tipo de Concepto',
        max_length=15,
        choices=TIPO_CONCEPTO,
        help_text='Tipo de concepto de nómina'
    )
    tipo_percepcion = models.ForeignKey(
        TipoPercepcion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='conceptos_nomina',
        verbose_name='Tipo de Percepción'
    )
    tipo_deduccion = models.ForeignKey(
        TipoDeduccion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='conceptos_nomina',
        verbose_name='Tipo de Deducción'
    )
    tipo_otro_pago = models.ForeignKey(
        TipoOtroPago,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='conceptos_nomina',
        verbose_name='Tipo de Otro Pago'
    )
    clave = models.CharField(
        'Clave',
        max_length=10,
        help_text='Clave del concepto'
    )
    concepto = models.CharField(
        'Concepto',
        max_length=200,
        help_text='Descripción del concepto'
    )
    importe_gravado = models.DecimalField(
        'Importe Gravado',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Importe gravado'
    )
    importe_exento = models.DecimalField(
        'Importe Exento',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Importe exento'
    )
    importe = models.DecimalField(
        'Importe',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Importe total'
    )

    class Meta:
        verbose_name = 'Concepto de Nómina'
        verbose_name_plural = 'Conceptos de Nómina'
        db_table = 'nomina_concepto'


class ProveedorCliente(AuditMixin):
    """
    Proveedores y clientes de la empresa
    """
    TIPO_CHOICES = [
        ('proveedor', 'Proveedor'),
        ('cliente', 'Cliente'),
        ('ambos', 'Ambos'),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='proveedores_clientes',
        verbose_name='Empresa'
    )
    entidad = models.ForeignKey(
        Entidad,
        on_delete=models.PROTECT,
        related_name='relaciones_comerciales',
        verbose_name='Entidad'
    )
    tipo = models.CharField(
        'Tipo',
        max_length=20,
        choices=TIPO_CHOICES,
        default='cliente',
        help_text='Tipo de relación comercial'
    )
    neto_operaciones = models.DecimalField(
        'Neto de Operaciones',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Neto de operaciones con esta entidad'
    )
    correo_contacto = models.EmailField(
        'Correo de Contacto',
        blank=True,
        help_text='Correo de contacto'
    )
    telefono_contacto = models.CharField(
        'Teléfono de Contacto',
        max_length=20,
        blank=True,
        help_text='Teléfono de contacto'
    )
    persona_contacto = models.CharField(
        'Persona de Contacto',
        max_length=100,
        blank=True,
        help_text='Nombre de la persona de contacto'
    )
    notas = models.TextField(
        'Notas',
        blank=True,
        help_text='Notas adicionales'
    )
    activo = models.BooleanField(
        'Activo',
        default=True,
        help_text='Indica si la relación comercial está activa'
    )

    class Meta:
        verbose_name = 'Proveedor/Cliente'
        verbose_name_plural = 'Proveedores/Clientes'
        db_table = 'proveedor_cliente'
        unique_together = [['empresa', 'entidad']]
        ordering = ['empresa', 'entidad']

    def __str__(self):
        return f"{self.empresa.rfc} - {self.entidad.rfc} ({self.tipo})"

    def actualizar_neto_operaciones(self):
        """Actualiza el neto de operaciones basado en los comprobantes"""
        # TODO: Implementar lógica para calcular neto de operaciones
        pass


class ArticuloNormalizado(AuditMixin):
    """
    Artículos normalizados para el catálogo de la empresa
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='articulos_normalizados',
        verbose_name='Empresa'
    )
    descripcion_normalizada = models.CharField(
        'Descripción Normalizada',
        max_length=200,
        help_text='Descripción normalizada del artículo'
    )
    clave_unidad_mas_comun = models.CharField(
        'Clave Unidad Más Común',
        max_length=10,
        blank=True,
        help_text='Clave de unidad más común para este artículo'
    )
    veces_comprado = models.IntegerField(
        'Veces Comprado',
        default=0,
        help_text='Número de veces que se ha comprado este artículo'
    )
    precio_promedio = models.DecimalField(
        'Precio Promedio',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Precio promedio del artículo'
    )
    precio_minimo = models.DecimalField(
        'Precio Mínimo',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Precio mínimo registrado'
    )
    precio_maximo = models.DecimalField(
        'Precio Máximo',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Precio máximo registrado'
    )
    activo = models.BooleanField(
        'Activo',
        default=True,
        help_text='Indica si el artículo está activo'
    )

    class Meta:
        verbose_name = 'Artículo Normalizado'
        verbose_name_plural = 'Artículos Normalizados'
        db_table = 'articulo_normalizado'
        unique_together = [['empresa', 'descripcion_normalizada']]
        ordering = ['empresa', 'descripcion_normalizada']

    def __str__(self):
        return f"{self.empresa.rfc} - {self.descripcion_normalizada}"


class ArticuloAlias(models.Model):
    """
    Alias para artículos normalizados
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='articulos_alias',
        verbose_name='Empresa'
    )
    alias = models.CharField(
        'Alias',
        max_length=200,
        help_text='Alias del artículo'
    )
    articulo_normalizado = models.ForeignKey(
        ArticuloNormalizado,
        on_delete=models.CASCADE,
        related_name='alias',
        verbose_name='Artículo Normalizado'
    )
    descripcion_normalizada = models.CharField(
        'Descripción Normalizada',
        max_length=200,
        help_text='Descripción normalizada (copia para búsqueda rápida)'
    )
    activo = models.BooleanField(
        'Activo',
        default=True,
        help_text='Indica si el alias está activo'
    )

    class Meta:
        verbose_name = 'Alias de Artículo'
        verbose_name_plural = 'Alias de Artículos'
        db_table = 'articulo_alias'
        unique_together = [['empresa', 'alias']]
        ordering = ['empresa', 'alias']

    def __str__(self):
        return f"{self.alias} -> {self.descripcion_normalizada}"
