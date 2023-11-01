import json
import os
from datetime import datetime
from decimal import Decimal
from unittest import mock

from satcfdi.create.cfd.catalogos import Impuesto, TipoFactor
from satcfdi.models import Signer
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
    emisor = cfdi40.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )

    invoice = cfdi40.Comprobante(
        emisor=emisor,
        lugar_expedicion="27200",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
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
                traslados=cfdi40.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.160000')),
                retenciones=[cfdi40.Traslado(impuesto=Impuesto.ISR, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.100000')), cfdi40.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.106667'))],
            ),
            _traslados_incluidos=True
        )
    )
    invoice.sign(signer)

    with mock.patch(f'requests.post') as mk:
        mk.return_value.content = b"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <soap:Body>
                <RequestTransactionResponse xmlns="http://www.fact.com.mx/schema/ws">
                    <RequestTransactionResult>
                        <Request>
                            <Requestor>00000000-0000-0000-0000-000000000000</Requestor>
                            <RequestorActive>true</RequestorActive>
                            <Transaction>TIMBRAR</Transaction>
                            <Country>MX</Country>
                            <Entity>JES900109Q90</Entity>
                            <User>00000000-0000-0000-0000-000000000000</User>
                            <UserName>MX.JES900109Q90.Juan</UserName>
                            <Id>96f342f4-a28a-487a-907f-7d00f388a8ce</Id>
                            <TimeStamp>2023-03-21T10:56:25.5256369-06:00</TimeStamp>
                        </Request>
                        <Response>
                            <Result>true</Result>
                            <TimeStamp>2023-03-21T10:56:26.1661906-06:00</TimeStamp>
                            <LastResult/>
                            <Code>1</Code>
                            <Description/>
                            <Hint/>
                            <Data> 20393 96f342f4-a28a-487a-907f-7d00f388a8ce</Data>
                            <Processor>TEST-BACK02</Processor>
                        </Response>
                        <ResponseData>
                            <ResponseData1>PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48dGZkOlRpbWJyZUZpc2NhbERpZ2l0YWwgeHNpOnNjaGVtYUxvY2F0aW9uPSJodHRwOi8vd3d3LnNhdC5nb2IubXgvVGltYnJlRmlzY2FsRGlnaXRhbCBodHRwOi8vd3d3LnNhdC5nb2IubXgvc2l0aW9faW50ZXJuZXQvY2ZkL1RpbWJyZUZpc2NhbERpZ2l0YWwvVGltYnJlRmlzY2FsRGlnaXRhbHYxMS54c2QiIFZlcnNpb249IjEuMSIgVVVJRD0iOTZmMzQyZjQtYTI4YS00ODdhLTkwN2YtN2QwMGYzODhhOGNlIiBGZWNoYVRpbWJyYWRvPSIyMDIzLTAzLTIxVDEwOjU2OjI2IiBSZmNQcm92Q2VydGlmPSJTUFIxOTA2MTNJNTIiIFNlbGxvQ0ZEPSJ5TU0rSVk3azd6UzloQzVvZkZGekM4bjVFendFL3Mvd3dWOE56M1l4dHh0K082Um1Cbm8vUTdENFJKeGpoS2dSOE1sRjJpQ0ROK1BkTmptWEZxYU04RnVnbkZOd2k1eEgxbVZsRk84OGcyT0REZXFib0d6bTFNN2lXM0IvN0RDTjRhRlZTa0hmdi9sUVFHNi9aWmFCMkdVNWhsMzd6MnVVRTZndW5Db1RtUUFQZUpOY1NxUjNJTTNyS3dPRmUxVGxDZm9iM3FBYWFwY0R4c0RYSStHM0huQ1llRW9JYjIyV1krRWNrTmhRdndlUUQydGtXTFZPc2xYNUxHTzVwSFRrR3dyZGV3L0NmVlVFeDVLNlpwK2lKaXFTQ0NqS1VLMythTVpLOURZeUdWTFRsQWdDR2FvZllZSDNJOGxFVFJUVXlmWHNIS0ZIa0xtaks4Q05RbjRJR0E9PSIgTm9DZXJ0aWZpY2Fkb1NBVD0iMzAwMDEwMDAwMDA0MDAwMDI0OTUiIFNlbGxvU0FUPSJJazd0dEpiYjcyNXJSNDFnUFYxQVJNdGdTc3UxT2FYRklyL3ZWaE5qU1ZtWVdlSHNYV2oyUHg3YzFhUW5YeXU4Uno0cXQxMGN2ZjMrQXZ4anVZcSszMmdsZmdFL0c2UHZWMVNYbkFKaHFoRk1sUFhJTFpHZ1Q5S0lXbE9ZdlVPRDJLMXgyTTBONzFlNWgwdW5HYVBHWTM3N3pWUlNDT20yR0U2VVBPZXhVQTB1OXRFSnIrQm5rR3dpZVpYbFJyY01DekowRTJwbVZBS2VFTndFRExOOWVGUjhGbno3M2hQZUtHTVFlNmc3VVZtczJvNktKbDlJMERuR1c4MGhoTWd4Uy9KdzM5RW5EazRtektVbVV1SHBqRnh5Rm1tZjlvY2FsOFlUMXVNTS95bjdhVHFwSFk4Vm8rZWZHb1VGWHRIWVllK3YzZVliOXdaZ0d1bE5hSHFhaGc9PSIgeG1sbnM6dGZkPSJodHRwOi8vd3d3LnNhdC5nb2IubXgvVGltYnJlRmlzY2FsRGlnaXRhbCIgeG1sbnM6eHNpPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYS1pbnN0YW5jZSIgLz4=</ResponseData1>
                            <ResponseData2>51749</ResponseData2>
                            <ResponseData3>OK</ResponseData3>
                        </ResponseData>
                    </RequestTransactionResult>
                </RequestTransactionResponse>
            </soap:Body>
        </soap:Envelope>
        """

        res = mysuite.stamp(
            cfdi=invoice
        )
        verify = verify_result(data=res.xml, filename="test_mysuite_stamp.xml")
        assert verify
        assert not res.pdf

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="test_mysuite_stamp.json")
        assert verify


