"""
Comando de Django para importar archivos XML de CFDI
"""
import os
import sys
from pathlib import Path
from decimal import Decimal
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from empresas.models import Empresa
from comprobantes.models import (
    Entidad, Comprobante, Detalle, ImpuestoComprobante,
    ImpuestoDetalle, Pago, PagoDocumentoRelacionado,
    Nomina, NominaConcepto
)
from catalogos.models import (
    TipoComprobante, UsoCFDI, FormaPago, MetodoPago, Moneda,
    Exportacion, Periodicidad, Meses, ClaveProdServ, ClaveUnidad,
    Impuesto, TipoFactor, ObjetoImp, RegimenFiscal
)

# Importar la librería satcfdi
# Agregar el path de satcfdi al PYTHONPATH
satcfdi_path = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
sys.path.insert(0, str(satcfdi_path))

try:
    from satcfdi import Comprobante as CFDIComprobante
except ImportError:
    CFDIComprobante = None


class Command(BaseCommand):
    help = 'Importa archivos XML de CFDI desde una carpeta (incluye subcarpetas)'

    def add_arguments(self, parser):
        parser.add_argument(
            'rfc_empresa',
            type=str,
            help='RFC de la empresa que importará los XMLs'
        )
        parser.add_argument(
            'carpeta_xml',
            type=str,
            help='Ruta de la carpeta que contiene los archivos XML'
        )
        parser.add_argument(
            '--validar-rfc',
            action='store_true',
            help='Validar que el RFC del emisor o receptor coincida con el RFC de la empresa'
        )
        parser.add_argument(
            '--actualizar',
            action='store_true',
            help='Actualizar comprobantes existentes'
        )

    def handle(self, *args, **options):
        rfc_empresa = options['rfc_empresa'].upper().strip()
        carpeta_xml = options['carpeta_xml']
        validar_rfc = options['validar_rfc']
        actualizar = options['actualizar']

        # Validar que la carpeta exista
        if not os.path.exists(carpeta_xml):
            raise CommandError(f'La carpeta "{carpeta_xml}" no existe')

        if not os.path.isdir(carpeta_xml):
            raise CommandError(f'"{carpeta_xml}" no es una carpeta')

        # Validar que la librería satcfdi esté disponible
        if CFDIComprobante is None:
            raise CommandError(
                'No se pudo importar la librería satcfdi. '
                'Asegúrate de que esté instalada o en el PYTHONPATH.'
            )

        # Obtener la empresa
        try:
            empresa = Empresa.objects.get(rfc=rfc_empresa)
        except Empresa.DoesNotExist:
            raise CommandError(f'No se encontró la empresa con RFC "{rfc_empresa}"')

        self.stdout.write(
            self.style.SUCCESS(f'Empresa: {empresa.nombre} ({empresa.rfc})')
        )
        self.stdout.write(f'Carpeta: {carpeta_xml}')
        self.stdout.write(f'Validar RFC: {validar_rfc}')
        self.stdout.write('')

        # Buscar archivos XML recursivamente
        archivos_xml = []
        for root, dirs, files in os.walk(carpeta_xml):
            for file in files:
                if file.lower().endswith('.xml'):
                    archivos_xml.append(os.path.join(root, file))

        total_archivos = len(archivos_xml)
        self.stdout.write(f'Se encontraron {total_archivos} archivos XML')
        self.stdout.write('')

        if total_archivos == 0:
            self.stdout.write(
                self.style.WARNING('No se encontraron archivos XML en la carpeta')
            )
            return

        # Contadores
        importados = 0
        actualizados = 0
        omitidos = 0
        errores = 0

        # Procesar cada archivo
        for i, archivo_xml in enumerate(archivos_xml, 1):
            try:
                resultado = self.procesar_xml(
                    archivo_xml, empresa, validar_rfc, actualizar
                )

                if resultado == 'importado':
                    importados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'[{i}/{total_archivos}] ✓ {archivo_xml}')
                    )
                elif resultado == 'actualizado':
                    actualizados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'[{i}/{total_archivos}] ↻ {archivo_xml}')
                    )
                elif resultado == 'omitido':
                    omitidos += 1
                    self.stdout.write(
                        self.style.WARNING(f'[{i}/{total_archivos}] ⊘ {archivo_xml}')
                    )

            except Exception as e:
                errores += 1
                self.stdout.write(
                    self.style.ERROR(f'[{i}/{total_archivos}] ✗ {archivo_xml}')
                )
                self.stdout.write(
                    self.style.ERROR(f'    Error: {str(e)}')
                )

        # Resumen
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═' * 60))
        self.stdout.write(self.style.SUCCESS('RESUMEN DE IMPORTACIÓN'))
        self.stdout.write(self.style.SUCCESS('═' * 60))
        self.stdout.write(f'Total de archivos procesados: {total_archivos}')
        self.stdout.write(self.style.SUCCESS(f'✓ Importados: {importados}'))
        if actualizados > 0:
            self.stdout.write(self.style.SUCCESS(f'↻ Actualizados: {actualizados}'))
        if omitidos > 0:
            self.stdout.write(self.style.WARNING(f'⊘ Omitidos: {omitidos}'))
        if errores > 0:
            self.stdout.write(self.style.ERROR(f'✗ Errores: {errores}'))

    def procesar_xml(self, archivo_xml, empresa, validar_rfc, actualizar):
        """
        Procesa un archivo XML y lo importa a la base de datos

        Returns:
            str: 'importado', 'actualizado', u 'omitido'
        """
        # Leer y parsear el XML
        try:
            cfdi = CFDIComprobante.from_file(archivo_xml)
        except Exception as e:
            raise Exception(f'Error al parsear XML: {str(e)}')

        # Obtener datos básicos
        try:
            uuid = cfdi.complemento.timbre_fiscal_digital.UUID
        except AttributeError:
            raise Exception('No se encontró el UUID (TimbreFiscalDigital)')

        # Obtener RFC emisor y receptor
        rfc_emisor = cfdi.emisor.Rfc
        rfc_receptor = cfdi.receptor.Rfc

        # Validar RFC si está activada la opción
        if validar_rfc:
            if empresa.rfc not in [rfc_emisor, rfc_receptor]:
                return 'omitido'  # No pertenece a la empresa

        # Verificar si ya existe
        comprobante_existente = Comprobante.objects.filter(uuid=uuid).first()

        if comprobante_existente and not actualizar:
            return 'omitido'

        # Importar el comprobante
        with transaction.atomic():
            # Obtener o crear entidades
            entidad_emisor = self.obtener_o_crear_entidad(
                empresa, rfc_emisor,
                cfdi.emisor.Nombre,
                cfdi.emisor.RegimenFiscal if hasattr(cfdi.emisor, 'RegimenFiscal') else None
            )

            entidad_receptor = self.obtener_o_crear_entidad(
                empresa, rfc_receptor,
                cfdi.receptor.Nombre,
                cfdi.receptor.RegimenFiscalReceptor if hasattr(cfdi.receptor, 'RegimenFiscalReceptor') else None
            )

            # Obtener catálogos
            tipo_comprobante = self.obtener_catalogo(TipoComprobante, cfdi.TipoDeComprobante)
            uso_cfdi = self.obtener_catalogo(UsoCFDI, cfdi.receptor.UsoCFDI)
            moneda = self.obtener_catalogo(Moneda, cfdi.Moneda)
            exportacion = self.obtener_catalogo(Exportacion, cfdi.Exportacion)

            metodo_pago = None
            if hasattr(cfdi, 'MetodoPago') and cfdi.MetodoPago:
                metodo_pago = self.obtener_catalogo(MetodoPago, cfdi.MetodoPago)

            forma_pago = None
            if hasattr(cfdi, 'FormaPago') and cfdi.FormaPago:
                forma_pago = self.obtener_catalogo(FormaPago, cfdi.FormaPago)

            # Leer el XML completo como texto
            with open(archivo_xml, 'r', encoding='utf-8') as f:
                xml_original = f.read()

            # Crear o actualizar comprobante
            comprobante_data = {
                'empresa': empresa,
                'emisor': entidad_emisor,
                'receptor': entidad_receptor,
                'fecha_emision': self.parse_datetime(cfdi.Fecha),
                'fecha_timbrado': self.parse_datetime(cfdi.complemento.timbre_fiscal_digital.FechaTimbrado),
                'tipo_comprobante': tipo_comprobante,
                'uso_cfdi': uso_cfdi,
                'version': cfdi.Version,
                'serie': cfdi.Serie if hasattr(cfdi, 'Serie') and cfdi.Serie else '',
                'folio': cfdi.Folio if hasattr(cfdi, 'Folio') and cfdi.Folio else '',
                'lugar_expedicion': cfdi.LugarExpedicion,
                'exportacion': exportacion,
                'moneda': moneda,
                'tipo_cambio': Decimal(str(cfdi.TipoCambio)) if hasattr(cfdi, 'TipoCambio') and cfdi.TipoCambio else None,
                'subtotal': Decimal(str(cfdi.SubTotal)),
                'descuento': Decimal(str(cfdi.Descuento)) if hasattr(cfdi, 'Descuento') and cfdi.Descuento else Decimal('0.00'),
                'total': Decimal(str(cfdi.Total)),
                'metodo_pago': metodo_pago,
                'forma_pago': forma_pago,
                'condiciones_pago': cfdi.CondicionesDePago if hasattr(cfdi, 'CondicionesDePago') and cfdi.CondicionesDePago else '',
                'xml_original': xml_original,
            }

            # Calcular totales de impuestos
            if hasattr(cfdi, 'impuestos') and cfdi.impuestos:
                if hasattr(cfdi.impuestos, 'TotalImpuestosTrasladados') and cfdi.impuestos.TotalImpuestosTrasladados:
                    comprobante_data['impuesto_trasladado_total'] = Decimal(str(cfdi.impuestos.TotalImpuestosTrasladados))
                if hasattr(cfdi.impuestos, 'TotalImpuestosRetenidos') and cfdi.impuestos.TotalImpuestosRetenidos:
                    comprobante_data['impuesto_retenido_total'] = Decimal(str(cfdi.impuestos.TotalImpuestosRetenidos))

            if comprobante_existente:
                for key, value in comprobante_data.items():
                    setattr(comprobante_existente, key, value)
                comprobante = comprobante_existente
                comprobante.save()
                es_nuevo = False
            else:
                comprobante = Comprobante.objects.create(
                    uuid=uuid,
                    **comprobante_data
                )
                es_nuevo = True

            # Importar conceptos (detalles)
            if es_nuevo or actualizar:
                # Eliminar detalles existentes si se está actualizando
                if not es_nuevo:
                    comprobante.detalles.all().delete()

                for idx, concepto in enumerate(cfdi.conceptos, 1):
                    self.importar_concepto(comprobante, concepto, idx)

        return 'importado' if es_nuevo else 'actualizado'

    def obtener_o_crear_entidad(self, empresa, rfc, nombre, regimen_fiscal_clave=None):
        """Obtiene o crea una entidad"""
        rfc = rfc.upper().strip()

        entidad, created = Entidad.objects.get_or_create(
            rfc=rfc,
            defaults={
                'empresa': empresa,
                'nombre': nombre,
                'tipo': 'F' if len(rfc) == 13 else 'M',
            }
        )

        # Actualizar nombre si cambió
        if not created and entidad.nombre != nombre:
            entidad.nombre = nombre
            entidad.save()

        # Actualizar régimen fiscal si se proporciona
        if regimen_fiscal_clave and not entidad.regimen_fiscal_actual:
            try:
                regimen = RegimenFiscal.objects.get(clave=regimen_fiscal_clave)
                entidad.regimen_fiscal_actual = regimen
                entidad.save()
            except RegimenFiscal.DoesNotExist:
                pass

        return entidad

    def obtener_catalogo(self, modelo, clave):
        """Obtiene un registro de catálogo, creándolo si no existe"""
        try:
            return modelo.objects.get(clave=clave)
        except modelo.DoesNotExist:
            # Crear el catálogo si no existe
            return modelo.objects.create(
                clave=clave,
                descripcion=f'Catálogo {clave} (auto-creado)'
            )

    def importar_concepto(self, comprobante, concepto, numero_linea):
        """Importa un concepto (detalle) del CFDI"""
        clave_prod_serv = self.obtener_catalogo(ClaveProdServ, concepto.ClaveProdServ)
        clave_unidad = self.obtener_catalogo(ClaveUnidad, concepto.ClaveUnidad)
        objeto_imp = self.obtener_catalogo(ObjetoImp, concepto.ObjetoImp)

        detalle = Detalle.objects.create(
            comprobante=comprobante,
            numero_linea=numero_linea,
            clave_prod_serv=clave_prod_serv,
            no_identificacion=concepto.NoIdentificacion if hasattr(concepto, 'NoIdentificacion') and concepto.NoIdentificacion else '',
            cantidad=Decimal(str(concepto.Cantidad)),
            clave_unidad=clave_unidad,
            unidad=concepto.Unidad if hasattr(concepto, 'Unidad') and concepto.Unidad else '',
            descripcion=concepto.Descripcion,
            valor_unitario=Decimal(str(concepto.ValorUnitario)),
            importe=Decimal(str(concepto.Importe)),
            descuento=Decimal(str(concepto.Descuento)) if hasattr(concepto, 'Descuento') and concepto.Descuento else Decimal('0.00'),
            objeto_imp=objeto_imp,
        )

        # Importar impuestos del concepto
        if hasattr(concepto, 'impuestos') and concepto.impuestos:
            # Traslados
            if hasattr(concepto.impuestos, 'traslados') and concepto.impuestos.traslados:
                for traslado in concepto.impuestos.traslados:
                    impuesto = self.obtener_catalogo(Impuesto, traslado.Impuesto)
                    tipo_factor = None
                    if hasattr(traslado, 'TipoFactor') and traslado.TipoFactor:
                        tipo_factor = self.obtener_catalogo(TipoFactor, traslado.TipoFactor)

                    ImpuestoDetalle.objects.create(
                        detalle=detalle,
                        tipo='traslado',
                        impuesto=impuesto,
                        tipo_factor=tipo_factor,
                        tasa_cuota=Decimal(str(traslado.TasaOCuota)) if hasattr(traslado, 'TasaOCuota') and traslado.TasaOCuota else None,
                        base=Decimal(str(traslado.Base)),
                        importe=Decimal(str(traslado.Importe)) if hasattr(traslado, 'Importe') and traslado.Importe else Decimal('0.00'),
                    )

            # Retenciones
            if hasattr(concepto.impuestos, 'retenciones') and concepto.impuestos.retenciones:
                for retencion in concepto.impuestos.retenciones:
                    impuesto = self.obtener_catalogo(Impuesto, retencion.Impuesto)
                    tipo_factor = None
                    if hasattr(retencion, 'TipoFactor') and retencion.TipoFactor:
                        tipo_factor = self.obtener_catalogo(TipoFactor, retencion.TipoFactor)

                    ImpuestoDetalle.objects.create(
                        detalle=detalle,
                        tipo='retencion',
                        impuesto=impuesto,
                        tipo_factor=tipo_factor,
                        tasa_cuota=Decimal(str(retencion.TasaOCuota)) if hasattr(retencion, 'TasaOCuota') and retencion.TasaOCuota else None,
                        base=Decimal(str(retencion.Base)),
                        importe=Decimal(str(retencion.Importe)),
                    )

        return detalle

    def parse_datetime(self, fecha_str):
        """Parsea una fecha/hora del CFDI al formato de Django"""
        try:
            # Intentar parsear con timezone
            dt = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
            return timezone.make_aware(dt, timezone.utc)
        except:
            # Si falla, intentar sin timezone
            try:
                dt = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S')
                return timezone.make_aware(dt)
            except:
                raise Exception(f'No se pudo parsear la fecha: {fecha_str}')
