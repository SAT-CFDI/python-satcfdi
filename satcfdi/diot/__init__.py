import os
from datetime import date, datetime
from decimal import Decimal
from io import BytesIO
from typing import Sequence

from .catalog import *
from .code import *
from .utils import _format_rfc, DIOTWriter, encrypt_triple_des, period_code, catalog_code
from ..ans1e import *
from ..models import RFC, RFCType, CURP, Certificate
from ..utils import iterate

__all__ = [
    'DIOT',
    'DatosIdentificacion',
    'ProveedorTercero',
    'DatosComplementaria',
    'TipoOperacion',
    'TipoTercero',
    'Periodo',
    'Pais'
]

from ..zip import zip_create, ZipData

current_dir = os.path.dirname(__file__)

VERSION_DEMC = 10
CODES = "0123456789ABCDEFGHIJKLMNOPQRSTUV"

CERTIFICATE = Certificate.load_certificate(
    certificate=open(os.path.join(current_dir, 'De_srv_x509.CER'), 'rb').read()
)


class DatosIdentificacion:
    def __init__(
            self,
            rfc: str | RFC,
            ejercicio: int,
            curp: str = None,
            nombre: str = None,
            apellido_paterno: str = None,
            apellido_materno: str = None,
            razon_social: str = None):

        self.rfc = RFC(rfc)
        self.ejercicio = ejercicio
        self.curp = CURP(curp) if curp else None
        self.nombre = nombre.upper() if nombre else None
        self.apellido_paterno = apellido_paterno.upper() if apellido_paterno else None
        self.apellido_materno = apellido_materno.upper() if apellido_materno else None
        self.razon_social = razon_social.upper() if razon_social else None

    def to_dict(self):
        return {
            "RFC": self.rfc,
            "CURP": self.curp,
            "Ejercicio": self.ejercicio,
            "ApellidoPaterno": self.apellido_paterno,
            "ApellidoMaterno": self.apellido_materno,
            "Nombre": self.nombre,
            "RazonSocial": self.razon_social
        }

    def render(self, w: DIOTWriter):
        w(10001, 0, 0, _format_rfc(self.rfc))
        if self.rfc.type == RFCType.FISICA:
            w(10002, 0, 0, self.curp)

        w(10021, 0, 0, self.ejercicio)
        if self.rfc.type == RFCType.FISICA:
            w(10003, 0, 0, self.apellido_paterno)
            w(10004, 0, 0, self.apellido_materno)
            w(10005, 0, 0, self.nombre)
        else:
            w(10006, 0, 0, self.razon_social)


class ProveedorTercero:
    def __init__(
            self,
            tipo_tercero: TipoTercero,
            tipo_operacion: TipoOperacion,
            rfc: str | RFC = None,
            id_fiscal: str = None,
            nombre_extranjero: str = None,
            pais: Pais = None,
            nacionalidad: str = None,
            iva16: int = None,
            iva16_na: int = None,
            iva_rfn: int = None,
            iva_rfn_na: int = None,
            iva_import16: int = None,
            iva_import16_na: int = None,
            iva_import_exento: int = None,
            iva0: int = None,
            iva_exento: int = None,
            retenido: int = None,
            devoluciones: int = None):
        """
        :param tipo_tercero:
        :param tipo_operacion:
        :param rfc:
        :param id_fiscal: Numero de ID Fiscal
        :param nombre_extranjero: Nombre del Extranjero
        :param pais: Pais de residencia
        :param nacionalidad: Nacionalidad
        :param iva16: Total de los actos o actividades pagados a la tasa 16% de IVA
        :param iva16_na: Total del IVA pagado no acreditable a la tasa 16%
        :param iva_rfn: Total de los actos o actividades pagados sujeto al estimulo de la region fronteriza norte
        :param iva_rfn_na: Total del IVA pagado no acreditable sujeto al estimulo de la region fronteriza norte
        :param iva_import16: Total de los actos o actividades pagados en la importacion de bienes y servicios a la tasa 16%
        :param iva_import16_na: Total del IVA pagado no acreditable en la importacion de bienes y servicios a la tasa 16%
        :param iva_import_exento: Total de los actos o actividades pagados en la importacion de bienes y servicios por los que no se pagara IVA (Exentos)
        :param iva0: Total de los actos o actividades pagados a la tasa 0% de IVA
        :param iva_exento: Total de los actos o actividades pagados por los que no se pagara IVA (Exentos)
        :param retenido: Total del IVA Retenido por el contribuyente
        :param devoluciones: Total del IVA correspondiente a las devoluciones, descuentos y bonificaciones sobre compras
        """

        self.tipo_tercero = tipo_tercero
        self.tipo_operacion = tipo_operacion
        self.rfc = RFC(rfc) if rfc else None
        self.id_fiscal = id_fiscal
        self.nombre_extranjero = nombre_extranjero
        self.pais = pais
        self.nacionalidad = nacionalidad

        self.iva16 = iva16
        self.iva16_na = iva16_na
        self.iva_rfn = iva_rfn
        self.iva_rfn_na = iva_rfn_na
        self.iva_import16 = iva_import16
        self.iva_import16_na = iva_import16_na
        self.iva_import_exento = iva_import_exento
        self.iva0 = iva0
        self.iva_exento = iva_exento
        self.retenido = retenido
        self.devoluciones = devoluciones

        match self.tipo_tercero:
            case TipoTercero.PROVEEDOR_NACIONAL:
                if not self.rfc:
                    raise ValueError("RFC is required for NACIONAL")
            case TipoTercero.PROVEEDOR_EXTRANJERO:
                pass
            case TipoTercero.PROVEEDOR_GLOBAL:
                if self.rfc:
                    raise ValueError("RFC must be empty for GLOBAL")

    def to_dict(self):
        return {
            "TipoTercero": catalog_code(TIPO_TERC, self.tipo_tercero),
            "TipoOperacion": catalog_code(TIP_OPERA, self.tipo_operacion),
            "RFC": self.rfc,
            "NumeroIDFiscal": self.id_fiscal,
            "NombreExtranjero": self.nombre_extranjero,
            "PaisResidencia": catalog_code(PAISES, self.pais),
            "Nacionalidad": self.nacionalidad,

            "ActividadesIVATasa16": self.iva16,
            "NoAcreditableIVATasa16": self.iva16_na,
            "ActividadesRegionFronterizaNorte": self.iva_rfn,
            "NoAcreditableRegionFronterizaNorte": self.iva_rfn_na,
            "ActividadesImportacionIVATasa16": self.iva_import16,
            "NoAcreditableImportacionIVATasa16": self.iva_import16_na,
            "ActividadesImportacionExento": self.iva_import_exento,
            "ActividadesIVATasa0": self.iva0,
            "ActividadesIVAExento": self.iva_exento,
            "Retenido": self.retenido,
            "Devoluciones": self.devoluciones
        }

    def render(self, w: DIOTWriter):
        w(200261, 1, 1, int(self.tipo_tercero))
        w(200361, 1, 1, int(self.tipo_operacion))
        if self.id_fiscal:
            w(200561, 1, 1, self.id_fiscal)
        if self.nombre_extranjero:
            w(200661, 1, 1, self.nombre_extranjero)
        if self.pais:
            w(200761, 1, 1, self.pais)
        if self.nacionalidad:
            w(200861, 1, 1, self.nacionalidad)
        if self.rfc:
            w(200461, 1, 1, _format_rfc(self.rfc))

        if self.iva16 is not None:
            w(301061, 1, 1, self.iva16)
        if self.iva16_na is not None:
            w(301161, 1, 1, self.iva16_na)
        if self.iva_rfn is not None:
            w(302461, 1, 1, self.iva_rfn)
        if self.iva_rfn_na is not None:
            w(301361, 1, 1, self.iva_rfn_na)
        if self.iva_import16 is not None:
            w(301461, 1, 1, self.iva_import16)
        if self.iva_import16_na is not None:
            w(301561, 1, 1, self.iva_import16_na)
        if self.iva_import_exento is not None:
            w(301861, 1, 1, self.iva_import_exento)
        if self.iva0 is not None:
            w(301961, 1, 1, self.iva0)
        if self.iva_exento is not None:
            w(302061, 1, 1, self.iva_exento)
        if self.retenido is not None:
            w(302161, 1, 1, self.retenido)
        if self.devoluciones is not None:
            w(302261, 1, 1, self.devoluciones)

    def to_list(self):
        return [
            self.tipo_tercero,
            self.tipo_operacion,
            self.rfc,
            self.id_fiscal,
            self.nombre_extranjero,
            self.pais,
            self.nacionalidad,
            self.iva16,
            "",
            self.iva16_na,
            "",
            "",
            self.iva_rfn,
            "",
            self.iva_rfn_na,
            self.iva_import16,
            self.iva_import16_na,
            "",
            "",
            self.iva_import_exento,
            self.iva0,
            self.iva_exento,
            self.retenido,
            self.devoluciones
        ]


class DatosComplementaria:
    def __init__(
            self,
            folio_anterior: str,
            fecha_presentacion_anterior: date
    ):
        self.folio_anterior = folio_anterior
        self.fecha_presentacion_anterior = fecha_presentacion_anterior

    def render(self, w: DIOTWriter):
        w(361, 0, 0, self.folio_anterior)
        w(461, 0, 0, self.fecha_presentacion_anterior.strftime('%Y%m%d'))

    def to_dict(self):
        return {
            "FolioAnterior": self.folio_anterior,
            "FechaPresentacionAnterior": self.fecha_presentacion_anterior
        }


class Totales:
    def __init__(self, providers: Sequence[ProveedorTercero]):
        self.operations_count = len(providers)

        self.iva16 = sum(p.iva16 or 0 for p in providers)
        self.iva16_na = sum(p.iva16_na or 0 for p in providers)
        self.iva_rfn = sum(p.iva_rfn or 0 for p in providers)
        self.iva_rfn_na = sum(p.iva_rfn_na or 0 for p in providers)
        self.iva_import16 = sum(p.iva_import16 or 0 for p in providers)
        self.iva_import16_na = sum(p.iva_import16_na or 0 for p in providers)
        self.iva_import_exento = sum(p.iva_import_exento or 0 for p in providers)
        self.iva0 = sum(p.iva0 or 0 for p in providers)
        self.iva_exento = sum(p.iva_exento or 0 for p in providers)
        self.retenido = sum(p.retenido or 0 for p in providers)
        self.devoluciones = sum(p.devoluciones or 0 for p in providers)

        # N102561=®((((N101261*16)/100)+((N101461*11)/100)+((N102761*15)/100)+((N102961*16)/100)*0.5)-(10/1000))
        # Note: N102961 es N102861
        self.total = round(self.iva16 * Decimal(".16") + self.iva_rfn * Decimal(".08") - Decimal(".01"))

        # N102661=®(((N101661*16)/100)+((N101861*11)/100)-(10/1000))
        self.total_import = round(self.iva_import16 * Decimal(".16") - Decimal(".01"))

    def to_dict(self):
        return {
            "TotalOperaciones": self.operations_count,

            "ActividadesIVATasa16": self.iva16,
            "NoAcreditableIVATasa16": self.iva16_na,
            "ActividadesRegionFronterizaNorte": self.iva_rfn,
            "NoAcreditableRegionFronterizaNorte": self.iva_rfn_na,
            "ActividadesImportacionIVATasa16": self.iva_import16,
            "NoAcreditableImportacionIVATasa16": self.iva_import16_na,
            "ActividadesImportacionExento": self.iva_import_exento,
            "ActividadesIVATasa0": self.iva0,
            "ActividadesIVAExento": self.iva_exento,
            "Retenido": self.retenido,
            "Devoluciones": self.devoluciones,

            "TotalExceptoImportaciones": self.total,
            "TotalImportaciones": self.total_import
        }

    def render(self, w: DIOTWriter):
        w(100161, 1, 0, self.operations_count)
        w(101261, 1, 0, self.iva16)
        w(101361, 1, 0, self.iva16_na)
        w(101461, 1, 0, 0)
        w(102861, 1, 0, self.iva_rfn)
        w(101561, 1, 0, self.iva_rfn_na)
        w(101661, 1, 0, self.iva_import16)
        w(101761, 1, 0, self.iva_import16_na)
        w(101861, 1, 0, 0)
        w(101961, 1, 0, 0)
        w(102061, 1, 0, self.iva_import_exento)
        w(102161, 1, 0, self.iva0)
        w(102261, 1, 0, self.iva_exento)
        w(102361, 1, 0, self.retenido)
        w(102461, 1, 0, self.devoluciones)
        w(102561, 1, 0, self.total)
        w(102661, 1, 0, self.total_import)


class DatosGenerales:
    def __init__(
            self,
            declaracion: str,
            periodo: Periodo,
            complementaria: DatosComplementaria = None,
    ):
        self.periodo = periodo
        self.periodicidad = period_code(self.periodo)

        self.complementaria = complementaria
        if complementaria:
            self.type = "2"
        else:
            self.type = "1"

        self.declaracion = declaracion

    def render(self, w: DIOTWriter):
        w(161, 0, 0, self.declaracion)
        w(261, 0, 0, self.type)
        if self.complementaria:
            self.complementaria.render(w)
        w(661, 0, 0, int(self.periodicidad))
        w(561, 0, 0, int(self.periodo))

    def to_dict(self):
        return {
            "Declaracion": catalog_code(PRESENTA, self.declaracion),
            "TipoDeclaracion": catalog_code(TIP_DECLA, self.type),
            "Complementaria": self.complementaria.to_dict() if self.complementaria else None,
            "Periodicidad": catalog_code(PERIODIC, self.periodicidad),
            "Periodo": catalog_code(PERIODO, self.periodo)
        }


class DIOT:
    tag = "DIOT"

    def __init__(
            self,
            datos_identificacion: DatosIdentificacion,
            periodo: Periodo,
            complementaria: DatosComplementaria = None,
            proveedores: Sequence[ProveedorTercero] = None
    ):
        proveedores = list(iterate(proveedores))

        self.datos_identificacion = datos_identificacion
        self.datos_generales = DatosGenerales(
            declaracion="1" if proveedores else "0",
            periodo=periodo,
            complementaria=complementaria
        )
        self.proveedores = proveedores
        self.totales = Totales(proveedores)

    def to_dict(self):
        return {
            "DatosIdentificacion": self.datos_identificacion.to_dict(),
            "DatosGenerales": self.datos_generales.to_dict(),
            "Proveedores": [p.to_dict() for p in self.proveedores],
            "Totales": self.totales.to_dict(),
        }

    def render(self, w: DIOTWriter):
        w(40006, 0, 0, '20062')
        w(10040, 0, 0, '081')

        self.datos_identificacion.render(w)
        self.datos_generales.render(w)

        if self.proveedores:
            self.totales.render(w)
            for i, p in enumerate(self.proveedores, start=1):
                w(200161, 1, 1, i)
                p.render(w)

        w.end()

    def filename(self):
        rfc = self.datos_identificacion.rfc

        if len(rfc) == 12:
            rfc = f"_{rfc}"

        v_dem = "0"
        n_formulario = 'DOT'
        ver_clte = CODES[VERSION_DEMC]
        ver_form = CODES[10]
        mes_inicial = CODES[1]
        mes_final = CODES[12]
        period = CODES[self.datos_identificacion.ejercicio % 100]

        x_date = datetime.now()
        anio = CODES[x_date.year % 100]
        mes = CODES[x_date.month]
        dia = CODES[x_date.day]
        hora = x_date.strftime("%H%M")

        suffix = "2" if len(self.proveedores) > 40000 else "1"

        return f"{rfc}{v_dem}{n_formulario}{ver_clte}{ver_form}{period}{mes_inicial}{period}{mes_final}{anio}{mes}{dia}{hora}{suffix}"

    def export(self, target):
        for p in self.proveedores:
            target.write("|".join(str(v or "") for v in p.to_list()).encode('windows-1252'))
            target.write(b"|\r\n")

    def plain_bytes(self) -> bytes:
        with BytesIO() as b:
            self.plain_write(b)
            return b.getvalue()

    def plain_write(self, target):
        w = DIOTWriter(target)
        self.render(w)

    def _zip_bytes(self, tmp_filename) -> bytes:
        with BytesIO() as b:
            self._zip_write(b, tmp_filename)
            return b.getvalue()

    def _zip_write(self, target: BytesIO, tmp_filename):
        zip_create(target, [
            ZipData(f"C:\\{tmp_filename}.txt", lambda s: self.render(DIOTWriter(s)))
        ])

    def _encrypted_bytes(self, tmp_filename) -> bytes:
        with BytesIO() as b:
            self._encrypted_write(b, tmp_filename)
            return b.getvalue()

    def _encrypted_write(self, target, tmp_filename):
        with BytesIO() as zip_data:
            self._zip_write(zip_data, tmp_filename)
            algo, key, iv, data_encrypted = encrypt_triple_des(zip_data)
            issuer = CERTIFICATE.certificate.get_issuer().der()
            enc_key = CERTIFICATE.encrypt(key)

        # SERIALIZE ANS1 FILE
        e = Ans1Encoder()
        with e.seq():
            e.oid("1.2.840.113549.1.7.3")
            with e.enter(nr=0, cls=Classes.Context):
                with e.seq():
                    e(0)
                    with e.set():
                        with e.seq():
                            e(0)
                            with e.seq():
                                e.write(issuer)
                                e(CERTIFICATE.serial_number)
                            with e.seq():
                                e.oid("1.2.840.113549.1.1.1")
                                e()
                            e(enc_key)
                    with e.seq():
                        e.oid("1.2.840.113549.1.7.1")
                        with e.seq():
                            e.oid(algo)
                            e(iv)
                        e(data_encrypted.getvalue(), nr=0, cls=Classes.Context)
        e.stream(target)

    def generate_package(self, dirname: str = None, filename: str = None) -> str:
        """
        Generate Package, return filename
        """
        filename = filename or self.filename()
        if dirname:
            out_file = os.path.join(dirname, filename + ".dec")
        else:
            out_file = filename + ".dec"
        with open(out_file, 'wb') as f:
            self._encrypted_write(f, filename)
        return out_file
