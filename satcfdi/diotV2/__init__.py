from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Optional, Sequence
from satcfdi.models import RFC

class TipoOperacion(StrEnum):
    ENAJENACION_DE_BIENES = "02"
    PRESTACION_DE_SERVICIOS_PROFESIONALES = "03"
    USO_O_GOSE_TEMPORAL_DE_BIENES = "06"
    IMPORTACION_DE_BIENES_O_SERVICIOS = "07" # Solo extranjeros
    IMPORTACION_POR_TRASFERENCIA_VIRTUAL = "08"
    OTROS = "85"
    OPERACIONES_GLOBALES = "87" # Solo proveedor global

class TipoTercero(StrEnum):
    PROVEEDOR_NACIONAL = "04"
    PROVEEDOR_EXTRANJERO = "05"
    PROVEEDOR_GLOBAL = "15"


@dataclass
class ProveedorTercero:
    tipo_tercero: TipoTercero
    tipo_operacion: TipoOperacion
    rfc: Optional[str | RFC] = None
    iva16base: Optional[int] = 0
    iva0base: Optional[int] = 0
    iva16descuento: Optional[int] = 0
    iva16acreditable: Optional[int] = 0
    iva16noacreditable: Optional[int] = 0
    actividadesNoObjeto: Optional[int] = 0
    actividadesExentos: Optional[int] = 0

    def to_list(self):
        return [
            # 3.1 Datos del tercero declarado

            # Tipo de tercero
            self.tipo_tercero,
            # Tipo de operación
            self.tipo_operacion,
            # Registro Federal de Contribuyentes
            self.rfc,
            # Número de identificación fiscal
            "",
            # Nombre del extranjero,
            "",
            # País o jurisdicción de residencia fiscal
            "",
            # Especificar lugar de jurisdicción fiscal
            "",

            # 3.2 Valor de los actos o actividades

            # Valor total de actos o actividades pagadas / Actos
            # o actividades pagados en la región fronteriza norte
            "",
            # Devoluciones, descuentos y bonificaciones / Actos
            # o actividades pagados en la región fronteriza norte
            "",
            # Valor total de actos o actividades pagadas / Actos
            # o actividades pagados en la región fronteriza sur
            "",
            # Devoluciones, descuentos y bonificaciones / Actos
            # o actividades pagados en la región fronteriza sur
            "",
            # Valor total de actos o actividades pagadas / Actos
            # o actividades totales pagados a la tasadel 16 % de IVA
            round(self.iva16base),
            # Devoluciones, descuentos y bonificaciones / Actos
            # o actividades totales pagados a la tasa del 16 % de IVA
            round(self.iva16descuento),
            # Valor total de actos o actividades pagadas / Actos
            # o actividades pagados en la importación por
            # aduana de bienes tangibles a la tasa del 16 % de IVA
            "",
            # Devoluciones, descuentos y bonificaciones / Actos
            # o actividades pagados en la importación por
            # aduana de bienes tangibles a la tasa del 16 % de IVA
            "",
            # Valor total de actos o actividades pagadas / Actos
            # o actividades pagados en la importación de bienes
            # intangibles y servicios a la tasa del 16 % de IVA
            "",
            # Devoluciones, descuentos y bonificaciones / Actos
            # o actividades pagados en la importación de bienes
            # intangibles y servicios a la tasa del 16 % de IVA
            "",

            # 3.3 IVA acreditable

            # Exclusivamente de actividades gravadas / Actos o
            # actividades pagados en la región fronteriza norte
            "",
            # Asociado a actividades por las cuales se aplicó una
            # proporción / Actos o actividades pagados en la
            # región fronteriza norte,
            "",
            # Exclusivamente de actividades gravadas / Actos o
            # actividades pagados en la región fronteriza sur
            "",
            # Asociado a actividades por las cuales se aplicó una
            # proporción / Actos o actividades pagados en la
            # región fronteriza sur
            "",
            # Exclusivamente de actividades gravadas / Actos o
            # actividades totales pagados a la tasa del 16 % de IVA
            min(round(self.iva16acreditable), round(round(self.iva16base) * Decimal("0.16"))),
            # Asociado a actividades por las cuales se aplicó una
            # proporción / Actos o actividades totales pagados a
            # la tasa del 16% de IVA
            "",
            # Exclusivamente de actividades gravadas / Actos o
            # actividades pagados en la importación por aduana
            # de bienes tangibles a la tasa del 16 % de IVA
            "",
            # Asociado a actividades por las cuales se aplicó una
            # proporción / Actos o actividades pagados en la
            # importación por aduana de bienes tangibles a la
            # tasa del 16 % de IVA
            "",
            # Exclusivamente de actividades gravadas / Actos o
            # actividades pagados en la importación de bienes
            # intangibles y servicios a la tasa del 16 % de IVA
            "",
            # Asociado a actividades por las cuales se aplicó una
            # proporción / Actos o actividades pagados en la
            # importación de bienes intangibles y servicios a la
            # tasa del 16 % de IVA
            "",

            # 3.4 IVA no acreditable

            # Asociado a actividades por las cuales se aplicó una
            # proporción / Actos o actividades pagados en la región
            # fronteriza norte
            "",
            # Asociado a actividades que no cumple con
            # requisitos / Actos o actividades pagados en la
            # región fronteriza norte
            "",
            # Asociado a actividades exentas / Actos o
            # actividades pagados en la región fronteriza norte
            "",
            # Asociado a actividades no objeto / Actos o
            # actividades pagados en la región fronteriza norte
            "",
            # Asociado a actividades por las cuales se aplicó una
            # proporción / Actos o actividades pagados en la
            # región fronteriza sur
            "",
            # Asociado a actividades que no cumple con
            # requisitos / Actos o actividades pagados en la
            # región fronteriza sur
            "",
            # Asociado a actividades exentas / Actos o
            # actividades pagados en la región fronteriza sur
            "",
            # Asociado a actividades no objeto / Actos o
            # actividades pagados en la región fronteriza sur
            "",
            # Asociado a actividades por las cuales se aplicó una
            # proporción / Actos o actividades totales pagados a
            # la tasa del 16% de IVA
            "",
            # Asociado a actividades que no cumple con
            # requisitos / Actos o actividades totales pagados a
            # la tasa del 16% de IVA
            round(self.iva16noacreditable) or "",
            # Asociado a actividades exentas / Actos o
            # actividades totales pagados a la tasa del 16% de
            # IVA
            "",
            # Asociado a actividades no objeto / Actos o
            # actividades totales pagados a la tasa del 16% de
            # IVA
            "",
            # Asociado a actividades por las cuales se aplicó una
            # proporción / Actos o actividades pagados en la
            # importación por aduana de bienes tangibles a la
            # tasa del 16% de IVA
            "",
            # Asociado a actividades que no cumple con
            # requisitos / Actos o actividades pagados en la
            # importación por aduana de bienes tangibles a la
            # tasa del 16% de IVA
            "",
            # Asociado a actividades exentas / Actos o
            # actividades pagados en la importación por aduana
            # de bienes tangibles a la tasa del 16% de IVA
            "",
            # Asociado a actividades no objeto / Actos o
            # actividades pagados en la importación por aduana
            # de bienes tangibles a la tasa del 16% de IVA
            "",
            # Asociado a actividades por las cuales se aplicó una
            # proporción / Actos o actividades pagados en la
            # importación de bienes intangibles y servicios a la
            # tasa del 16% del IVA
            "",
            # Asociado a actividades que no cumple con
            # requisitos / Actos o actividades pagados en la
            # importación de bienes intangibles y servicios a la
            # tasa del 16% del IVA
            "",
            # Asociado a actividades exentas / Actos o
            # actividades pagados en la importación de bienes
            # intangibles y servicios a la tasa del 16% del IVA
            "",
            # Asociado a actividades no objeto / Actos o
            # actividades pagados en la importación de bienes
            # intangibles y servicios a la tasa del 16% del IVA
            "",

            # 3.5  Datos adicionales

            # IVA retenido por el contribuyente
            "",
            # Actos o actividades pagados en la importación de
            # bienes y servicios por los que no se pagara el IVA
            # (Exentos)
            "",
            # Actos o actividades pagados por los que no se
            # pagará el IVA (Exentos)
            round(self.actividadesExentos),
            # Demás actos o actividades pagados a la tasa del 0%
            # de IVA
            round(self.iva0base) or "",
            # Actos o actividades no objeto del IVA realizados en
            # territorio nacional
            round(self.actividadesNoObjeto),
            # Actos o actividades no objeto del IVA por no contar
            # con establecimiento en territorio nacional
            "",
            # Manifiesto que se dio efectos fiscales a los
            # comprobantes que amparan las operaciones
            # realizadas con el proveedor
            "01"

        ]

class DIOTV2:
    def __init__(
            self,
            proveedores: Sequence[ProveedorTercero] = None
    ):
        self.proveedores = proveedores

    def export(self, target):
        for p in self.proveedores.values():
            target.write("|".join(str(v or "") for v in p.to_list()).encode('utf-8'))
            target.write(b"\r\n")