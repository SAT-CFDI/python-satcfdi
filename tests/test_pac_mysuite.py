import json
from datetime import datetime
from decimal import Decimal
from unittest import mock

from requests.auth import HTTPBasicAuth

from satcfdi.create import Issuer
from satcfdi.create.cfd import cfdi40
from satcfdi.pacs import Environment
from satcfdi.pacs.mysuite import MYSuite
from utils import get_signer, verify_result


def test_mysuite_test():
    mysuite = MYSuite(
        requestor="0c320b03-d4f1-47bc-9fb4-77995f9bf33e",
        country="MX",
        user_name="Juan",
        environment=Environment.PRODUCTION
    )

    signer = get_signer('JES900109Q90')
    emisor = Issuer(signer=signer, tax_system="601")

    invoice = cfdi40.Comprobante(
        emisor=emisor,
        lugar_expedicion="27200",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="H&E951128469",
            nombre="H & E",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="34500",
            regimen_fiscal_receptor="601"
        ),
        metodo_pago="PPD",
        forma_pago="99",
        serie="T",
        folio="1000",
        conceptos=cfdi40.Concepto(
            cuenta_predial='1234567890',
            clave_prod_serv='10101702',
            cantidad=Decimal('.10'),
            clave_unidad='E48',
            descripcion='SERVICIOS DE RENTA',
            valor_unitario=Decimal("1.00"),
            impuestos=cfdi40.Impuestos(
                traslados=cfdi40.Impuesto.parse('002|Tasa|0.160000'),
                retenciones=[cfdi40.Impuesto.parse('001|Tasa|0.100000'), cfdi40.Impuesto.parse('002|Tasa|0.106667')],
            ),
            _traslados_incluidos=True
        )
    )

    res = mysuite.stamp(
        cfdi=invoice
    )
