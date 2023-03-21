import json
import os
from datetime import datetime
from decimal import Decimal
from unittest import mock

from requests.auth import HTTPBasicAuth
from satcfdi import Signer

from satcfdi.create import Issuer
from satcfdi.create.cfd import cfdi40
from satcfdi.pacs import Environment
from satcfdi.pacs.mysuite import MYSuite
from utils import get_signer, verify_result

current_dir = os.path.dirname(__file__)


def test_mysuite_test():
    mysuite = MYSuite(
        requestor="0c320b03-d4f1-47bc-9fb4-77995f9bf33e",
        country="MX",
        user_name="Juan",
        environment=Environment.TEST
    )

    signer = Signer.load(
        certificate=open(os.path.join(current_dir, f'csd/Certificado_Prueba_Vigente_SAT_JES900109Q90/30001000000400002436.cer'), 'rb').read(),
        key=open(os.path.join(current_dir, f'csd/Certificado_Prueba_Vigente_SAT_JES900109Q90/30001000000400002436.key'), 'rb').read(),
        password=open(os.path.join(current_dir, f'csd/Certificado_Prueba_Vigente_SAT_JES900109Q90/pass.txt'), 'rb').read()
    )
    emisor = Issuer(signer=signer, tax_system="601")

    invoice = cfdi40.Comprobante(
        emisor=emisor,
        lugar_expedicion="27200",
        fecha=datetime.now(),  # datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="JES900109Q90",
            nombre="JIMENEZ ESTRADA SALAS A A",
            uso_cfdi="G01",
            domicilio_fiscal_receptor="01030",
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
