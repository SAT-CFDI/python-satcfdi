import json
from decimal import Decimal
from unittest import mock

from utils import get_signer, verify_result

from satcfdi.create.cfd import cfdi40
from satcfdi.create.cfd.catalogos import Impuesto, RegimenFiscal, TipoFactor, UsoCFDI
from satcfdi.pacs import Environment
from satcfdi.pacs.finkok import Finkok

finkok = Finkok(
    username="user@email.com",
    password="password",
    environment=Environment.TEST,
)


def test_finkok_issue():
    signer = get_signer("eku9003173c9", get_csd=True)
    emisor = cfdi40.Emisor(
        rfc=signer.rfc, nombre=signer.legal_name, regimen_fiscal="601"
    )
    assert emisor["Nombre"] == "ESCUELA KEMPER URGATE"

    receptor = cfdi40.Receptor(
        rfc="ICV060329BY0",
        nombre="INMOBILIARIA CVA",
        uso_cfdi=UsoCFDI.GASTOS_EN_GENERAL,
        domicilio_fiscal_receptor="33826",
        regimen_fiscal_receptor=RegimenFiscal.GENERAL_DE_LEY_PERSONAS_MORALES,
    )

    concepto = cfdi40.Concepto(
        clave_prod_serv="84111506",
        cantidad=Decimal("1.00"),
        clave_unidad="E48",
        descripcion="SERVICIOS DE FACTURACION",
        valor_unitario=Decimal("1250.30"),
        impuestos=cfdi40.Impuestos(
            traslados=cfdi40.Traslado(
                impuesto=Impuesto.IVA,
                tipo_factor=TipoFactor.TASA,
                tasa_o_cuota=Decimal("0.160000"),
            ),
            retenciones=[
                cfdi40.Retencion(
                    impuesto=Impuesto.ISR,
                    tipo_factor=TipoFactor.TASA,
                    tasa_o_cuota=Decimal("0.100000"),
                ),
                cfdi40.Retencion(
                    impuesto=Impuesto.IVA,
                    tipo_factor=TipoFactor.TASA,
                    tasa_o_cuota=Decimal("0.106667"),
                ),
            ],
        ),
        _traslados_incluidos=False,  # indica si el valor unitario incluye los traslados
    )

    invoice = cfdi40.Comprobante(
        emisor=emisor,
        lugar_expedicion="27200",
        receptor=receptor,
        metodo_pago="PPD",
        forma_pago="99",
        serie="T",
        folio="1000",
        conceptos=concepto,
    )

    with mock.patch(f"requests.post") as mk:
        mk.return_value.ok = True
        mk.return_value.content = b'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<senv:Envelope xmlns:plink="http://schemas.xmlsoap.org/ws/2003/05/partner-link/" xmlns:s0="apps.services.soap.core.views" xmlns:s1="https://facturacion.finkok.com/servicios/async" xmlns:s12enc="http://www.w3.org/2003/05/soap-encoding/" xmlns:s12env="http://www.w3.org/2003/05/soap-envelope/" xmlns:senc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:senv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:tns="http://facturacion.finkok.com/stamp" xmlns:wsa="http://schemas.xmlsoap.org/ws/2003/03/addressing" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><senv:Body><tns:sign_stampResponse><tns:sign_stampResult><s0:xml>&lt;?xml version="1.0" encoding="utf-8"?&gt;\n&lt;cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="4.0" Serie="T" Folio="1000" Fecha="2024-06-12T00:50:21" Sello="Lg1Ea6SUqUxLrfZi0RwGhi+efWT29on4wdsfUyrfn40DCxK7QKkkqwLlPawHjAFBTkiKue5oOZ0eksJbu3TkgAomx1LuxdG6JIcwI5xTlxBR4IHNqwrPH126K/hOReCwGtoqq0vVemfiz8FDf6FtmcJXj3W4rHSA2LGI1nW6vszPRDCE9BL/2cs5ja16qAeoy7pi6JxbpT/mop2Jt9GUnZCqRcEiTwdTiS1DJuLis49H1JlqzDIRD6B1PmaT/9x4DDNTaPlmcLFuP9aadF6XxJNdM+SLTEW5ic/p6uTONYTEB1hbie2cbSh3LT/UsOtWyeLHUSg7/BnkstgIOn4/Tw==" FormaPago="99" NoCertificado="30001000000500003416" Certificado="MIIFsDCCA5igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0MTYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTE0MzUxWhcNMjcwNTE4MTE0MzUxWjCB1zEnMCUGA1UEAxMeRVNDVUVMQSBLRU1QRVIgVVJHQVRFIFNBIERFIENWMScwJQYDVQQpEx5FU0NVRUxBIEtFTVBFUiBVUkdBVEUgU0EgREUgQ1YxJzAlBgNVBAoTHkVTQ1VFTEEgS0VNUEVSIFVSR0FURSBTQSBERSBDVjElMCMGA1UELRMcRUtVOTAwMzE3M0M5IC8gVkFEQTgwMDkyN0RKMzEeMBwGA1UEBRMVIC8gVkFEQTgwMDkyN0hTUlNSTDA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtmecO6n2GS0zL025gbHGQVxznPDICoXzR2uUngz4DqxVUC/w9cE6FxSiXm2ap8Gcjg7wmcZfm85EBaxCx/0J2u5CqnhzIoGCdhBPuhWQnIh5TLgj/X6uNquwZkKChbNe9aeFirU/JbyN7Egia9oKH9KZUsodiM/pWAH00PCtoKJ9OBcSHMq8Rqa3KKoBcfkg1ZrgueffwRLws9yOcRWLb02sDOPzGIm/jEFicVYt2Hw1qdRE5xmTZ7AGG0UHs+unkGjpCVeJ+BEBn0JPLWVvDKHZAQMj6s5Bku35+d/MyATkpOPsGT/VTnsouxekDfikJD1f7A1ZpJbqDpkJnss3vQIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAFaUgj5PqgvJigNMgtrdXZnbPfVBbukAbW4OGnUhNrA7SRAAfv2BSGk16PI0nBOr7qF2mItmBnjgEwk+DTv8Zr7w5qp7vleC6dIsZFNJoa6ZndrE/f7KO1CYruLXr5gwEkIyGfJ9NwyIagvHHMszzyHiSZIA850fWtbqtythpAliJ2jF35M5pNS+YTkRB+T6L/c6m00ymN3q9lT1rB03YywxrLreRSFZOSrbwWfg34EJbHfbFXpCSVYdJRfiVdvHnewN0r5fUlPtR9stQHyuqewzdkyb5jTTw02D2cUfL57vlPStBj7SEi3uOWvLrsiDnnCIxRMYJ2UA2ktDKHk+zWnsDmaeleSzonv2CHW42yXYPCvWi88oE1DJNYLNkIjua7MxAnkNZbScNw01A6zbLsZ3y8G6eEYnxSTRfwjd8EP4kdiHNJftm7Z4iRU7HOVh79/lRWB+gd171s3d/mI9kte3MRy6V8MMEMCAnMboGpaooYwgAmwclI2XZCczNWXfhaWe0ZS5PmytD/GDpXzkX0oEgY9K/uYo5V77NdZbGAjmyi8cE2B2ogvyaN2XfIInrZPgEffJ4AB7kFA2mwesdLOCh0BLD9itmCve3A1FGR4+stO2ANUoiI3w3Tv2yQSg4bjeDlJ08lXaaFCLW2peEXMXjQUk7fmpb5MNuOUTW6BE=" SubTotal="1250.30" Moneda="MXN" Total="1191.95" TipoDeComprobante="I" Exportacion="01" MetodoPago="PPD" LugarExpedicion="27200" xsi:schemaLocation="http://www.sat.gob.mx/cfd/4 http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd"&gt;&lt;cfdi:Emisor Rfc="EKU9003173C9" Nombre="ESCUELA KEMPER URGATE" RegimenFiscal="601"/&gt;&lt;cfdi:Receptor Rfc="ICV060329BY0" Nombre="INMOBILIARIA CVA" DomicilioFiscalReceptor="33826" RegimenFiscalReceptor="601" UsoCFDI="G03"/&gt;&lt;cfdi:Conceptos&gt;&lt;cfdi:Concepto ClaveProdServ="84111506" Cantidad="1.00" ClaveUnidad="E48" Descripcion="SERVICIOS DE FACTURACION" ValorUnitario="1250.30" Importe="1250.30" ObjetoImp="02"&gt;&lt;cfdi:Impuestos&gt;&lt;cfdi:Traslados&gt;&lt;cfdi:Traslado Base="1250.30" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="200.05"/&gt;&lt;/cfdi:Traslados&gt;&lt;cfdi:Retenciones&gt;&lt;cfdi:Retencion Base="1250.30" Impuesto="001" TipoFactor="Tasa" TasaOCuota="0.100000" Importe="125.03"/&gt;&lt;cfdi:Retencion Base="1250.30" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.106667" Importe="133.37"/&gt;&lt;/cfdi:Retenciones&gt;&lt;/cfdi:Impuestos&gt;&lt;/cfdi:Concepto&gt;&lt;/cfdi:Conceptos&gt;&lt;cfdi:Impuestos TotalImpuestosRetenidos="258.40" TotalImpuestosTrasladados="200.05"&gt;&lt;cfdi:Retenciones&gt;&lt;cfdi:Retencion Impuesto="001" Importe="125.03"/&gt;&lt;cfdi:Retencion Impuesto="002" Importe="133.37"/&gt;&lt;/cfdi:Retenciones&gt;&lt;cfdi:Traslados&gt;&lt;cfdi:Traslado Base="1250.30" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="200.05"/&gt;&lt;/cfdi:Traslados&gt;&lt;/cfdi:Impuestos&gt;&lt;cfdi:Complemento&gt;&lt;tfd:TimbreFiscalDigital xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital" xsi:schemaLocation="http://www.sat.gob.mx/TimbreFiscalDigital http://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xsd" Version="1.1" SelloCFD="Lg1Ea6SUqUxLrfZi0RwGhi+efWT29on4wdsfUyrfn40DCxK7QKkkqwLlPawHjAFBTkiKue5oOZ0eksJbu3TkgAomx1LuxdG6JIcwI5xTlxBR4IHNqwrPH126K/hOReCwGtoqq0vVemfiz8FDf6FtmcJXj3W4rHSA2LGI1nW6vszPRDCE9BL/2cs5ja16qAeoy7pi6JxbpT/mop2Jt9GUnZCqRcEiTwdTiS1DJuLis49H1JlqzDIRD6B1PmaT/9x4DDNTaPlmcLFuP9aadF6XxJNdM+SLTEW5ic/p6uTONYTEB1hbie2cbSh3LT/UsOtWyeLHUSg7/BnkstgIOn4/Tw==" NoCertificadoSAT="30001000000500003456" RfcProvCertif="CVD110412TF6" UUID="AF124DC7-BD75-5EFF-8EDF-28C1E7D43B1D" FechaTimbrado="2024-06-12T00:50:43" SelloSAT="T/p8LJjDW638NrIyF90SwxdYaIUqNNOvYE4hkots+3OADeIguLcxkMnHICIMuw6D9ugI48j0Brex7D0q+THvh6o7RgzJmfsMayJOEbfftLWdubKTqdP9HQ5+MYd3zNL6cBW6u31K0hT8W6kUufi2TI1Ma6jKToXQVpPKjpdMMiXtmXuSRYoKwO+Gk9rjy1zlr6/1ZBq8c7HjZJ7oEJiJwDpP5GWNm9ID2emDj4BO4EzsVpIw31B4yNc031FMi0JOuvhZudVCjAFlakvRQOVf2YflWQNMT+iTexGWRC2XkozqzcoqvjCwyyLIEkrFO1IG9q8yA6JHxPGcRL1QJcfdAw=="/&gt;&lt;/cfdi:Complemento&gt;&lt;/cfdi:Comprobante&gt;</s0:xml><s0:UUID>AF124DC7-BD75-5EFF-8EDF-28C1E7D43B1D</s0:UUID><s0:Fecha>2024-06-12T00:50:43</s0:Fecha><s0:CodEstatus>Comprobante timbrado satisfactoriamente</s0:CodEstatus><s0:SatSeal>T/p8LJjDW638NrIyF90SwxdYaIUqNNOvYE4hkots+3OADeIguLcxkMnHICIMuw6D9ugI48j0Brex7D0q+THvh6o7RgzJmfsMayJOEbfftLWdubKTqdP9HQ5+MYd3zNL6cBW6u31K0hT8W6kUufi2TI1Ma6jKToXQVpPKjpdMMiXtmXuSRYoKwO+Gk9rjy1zlr6/1ZBq8c7HjZJ7oEJiJwDpP5GWNm9ID2emDj4BO4EzsVpIw31B4yNc031FMi0JOuvhZudVCjAFlakvRQOVf2YflWQNMT+iTexGWRC2XkozqzcoqvjCwyyLIEkrFO1IG9q8yA6JHxPGcRL1QJcfdAw==</s0:SatSeal><s0:Incidencias/><s0:NoCertificadoSAT>30001000000500003456</s0:NoCertificadoSAT></tns:sign_stampResult></tns:sign_stampResponse></senv:Body></senv:Envelope>'
        res = finkok.issue(invoice)

        assert verify_result(res.xml, filename="test_finkok_issue.xml")
        assert not res.pdf

        assert mk.called

        assert (
            mk.call_args.kwargs["url"]
            == "https://demo-facturacion.finkok.com/servicios/soap/stamp.wsdl"
        )


def test_finkok_quick_stamp():
    signer = get_signer("eku9003173c9", get_csd=True)
    emisor = cfdi40.Emisor(
        rfc=signer.rfc, nombre=signer.legal_name, regimen_fiscal="601"
    )
    assert emisor["Nombre"] == "ESCUELA KEMPER URGATE"

    receptor = cfdi40.Receptor(
        rfc="ICV060329BY0",
        nombre="INMOBILIARIA CVA",
        uso_cfdi=UsoCFDI.GASTOS_EN_GENERAL,
        domicilio_fiscal_receptor="33826",
        regimen_fiscal_receptor=RegimenFiscal.GENERAL_DE_LEY_PERSONAS_MORALES,
    )

    concepto = cfdi40.Concepto(
        clave_prod_serv="84111506",
        cantidad=Decimal("1.00"),
        clave_unidad="E48",
        descripcion="SERVICIOS DE FACTURACION",
        valor_unitario=Decimal("1250.30"),
        impuestos=cfdi40.Impuestos(
            traslados=cfdi40.Traslado(
                impuesto=Impuesto.IVA,
                tipo_factor=TipoFactor.TASA,
                tasa_o_cuota=Decimal("0.160000"),
            ),
            retenciones=[
                cfdi40.Retencion(
                    impuesto=Impuesto.ISR,
                    tipo_factor=TipoFactor.TASA,
                    tasa_o_cuota=Decimal("0.100000"),
                ),
                cfdi40.Retencion(
                    impuesto=Impuesto.IVA,
                    tipo_factor=TipoFactor.TASA,
                    tasa_o_cuota=Decimal("0.106667"),
                ),
            ],
        ),
        _traslados_incluidos=False,  # indica si el valor unitario incluye los traslados
    )

    invoice = cfdi40.Comprobante(
        emisor=emisor,
        lugar_expedicion="27200",
        receptor=receptor,
        metodo_pago="PPD",
        forma_pago="99",
        serie="T",
        folio="1000",
        conceptos=concepto,
    )

    invoice.sign(signer)
    invoice = invoice.process()

    with mock.patch(f"requests.post") as mk:
        mk.return_value.ok = True
        mk.return_value.content = b'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<senv:Envelope xmlns:plink="http://schemas.xmlsoap.org/ws/2003/05/partner-link/" xmlns:s0="apps.services.soap.core.views" xmlns:s1="https://facturacion.finkok.com/servicios/async" xmlns:s12enc="http://www.w3.org/2003/05/soap-encoding/" xmlns:s12env="http://www.w3.org/2003/05/soap-envelope/" xmlns:senc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:senv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:tns="http://facturacion.finkok.com/stamp" xmlns:wsa="http://schemas.xmlsoap.org/ws/2003/03/addressing" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><senv:Body><tns:quick_stampResponse><tns:quick_stampResult><s0:xml>&lt;?xml version="1.0" encoding="utf-8"?&gt;\n&lt;cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="4.0" Serie="T" Folio="1000" Fecha="2024-06-14T00:23:40" Sello="sx4EUAjHCu7urj4dTrqQjdX8hTD2C75vEcXIBXon0u5D1Yvj92/34pcC9cBijGPWTE/lBzWsOzfGIv9w5adM4FX+lk8wa953iIV4WLVv7u9Fy4OCd9ikZOGY+P4NEFQt+an06V6XC0qP9qikZ83Bd4GbFIiffZq8BdWuFHAkt+nSsfZo9/1yKBOCRJH3SQbSzkqoR64zuLfmQmLLKh9XbWEqbzv5Ztqql2/jhgWDzBzkKW40TeGWRb61rSaIawU59h2yxjKTzjO9G78/Ge+/x7VfmCieyfKRNACIrQwL7+5mQNWszI8eYzaO65ebQOc2MYKDNRzjEp7Vinu+giTbnw==" FormaPago="99" NoCertificado="30001000000500003416" Certificado="MIIFsDCCA5igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0MTYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTE0MzUxWhcNMjcwNTE4MTE0MzUxWjCB1zEnMCUGA1UEAxMeRVNDVUVMQSBLRU1QRVIgVVJHQVRFIFNBIERFIENWMScwJQYDVQQpEx5FU0NVRUxBIEtFTVBFUiBVUkdBVEUgU0EgREUgQ1YxJzAlBgNVBAoTHkVTQ1VFTEEgS0VNUEVSIFVSR0FURSBTQSBERSBDVjElMCMGA1UELRMcRUtVOTAwMzE3M0M5IC8gVkFEQTgwMDkyN0RKMzEeMBwGA1UEBRMVIC8gVkFEQTgwMDkyN0hTUlNSTDA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtmecO6n2GS0zL025gbHGQVxznPDICoXzR2uUngz4DqxVUC/w9cE6FxSiXm2ap8Gcjg7wmcZfm85EBaxCx/0J2u5CqnhzIoGCdhBPuhWQnIh5TLgj/X6uNquwZkKChbNe9aeFirU/JbyN7Egia9oKH9KZUsodiM/pWAH00PCtoKJ9OBcSHMq8Rqa3KKoBcfkg1ZrgueffwRLws9yOcRWLb02sDOPzGIm/jEFicVYt2Hw1qdRE5xmTZ7AGG0UHs+unkGjpCVeJ+BEBn0JPLWVvDKHZAQMj6s5Bku35+d/MyATkpOPsGT/VTnsouxekDfikJD1f7A1ZpJbqDpkJnss3vQIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAFaUgj5PqgvJigNMgtrdXZnbPfVBbukAbW4OGnUhNrA7SRAAfv2BSGk16PI0nBOr7qF2mItmBnjgEwk+DTv8Zr7w5qp7vleC6dIsZFNJoa6ZndrE/f7KO1CYruLXr5gwEkIyGfJ9NwyIagvHHMszzyHiSZIA850fWtbqtythpAliJ2jF35M5pNS+YTkRB+T6L/c6m00ymN3q9lT1rB03YywxrLreRSFZOSrbwWfg34EJbHfbFXpCSVYdJRfiVdvHnewN0r5fUlPtR9stQHyuqewzdkyb5jTTw02D2cUfL57vlPStBj7SEi3uOWvLrsiDnnCIxRMYJ2UA2ktDKHk+zWnsDmaeleSzonv2CHW42yXYPCvWi88oE1DJNYLNkIjua7MxAnkNZbScNw01A6zbLsZ3y8G6eEYnxSTRfwjd8EP4kdiHNJftm7Z4iRU7HOVh79/lRWB+gd171s3d/mI9kte3MRy6V8MMEMCAnMboGpaooYwgAmwclI2XZCczNWXfhaWe0ZS5PmytD/GDpXzkX0oEgY9K/uYo5V77NdZbGAjmyi8cE2B2ogvyaN2XfIInrZPgEffJ4AB7kFA2mwesdLOCh0BLD9itmCve3A1FGR4+stO2ANUoiI3w3Tv2yQSg4bjeDlJ08lXaaFCLW2peEXMXjQUk7fmpb5MNuOUTW6BE=" SubTotal="1250.30" Moneda="MXN" Total="1191.95" TipoDeComprobante="I" Exportacion="01" MetodoPago="PPD" LugarExpedicion="27200" xsi:schemaLocation="http://www.sat.gob.mx/cfd/4 http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd"&gt;&lt;cfdi:Emisor Rfc="EKU9003173C9" Nombre="ESCUELA KEMPER URGATE" RegimenFiscal="601"/&gt;&lt;cfdi:Receptor Rfc="ICV060329BY0" Nombre="INMOBILIARIA CVA" DomicilioFiscalReceptor="33826" RegimenFiscalReceptor="601" UsoCFDI="G03"/&gt;&lt;cfdi:Conceptos&gt;&lt;cfdi:Concepto ClaveProdServ="84111506" Cantidad="1.00" ClaveUnidad="E48" Descripcion="SERVICIOS DE FACTURACION" ValorUnitario="1250.30" Importe="1250.30" ObjetoImp="02"&gt;&lt;cfdi:Impuestos&gt;&lt;cfdi:Traslados&gt;&lt;cfdi:Traslado Base="1250.30" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="200.05"/&gt;&lt;/cfdi:Traslados&gt;&lt;cfdi:Retenciones&gt;&lt;cfdi:Retencion Base="1250.30" Impuesto="001" TipoFactor="Tasa" TasaOCuota="0.100000" Importe="125.03"/&gt;&lt;cfdi:Retencion Base="1250.30" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.106667" Importe="133.37"/&gt;&lt;/cfdi:Retenciones&gt;&lt;/cfdi:Impuestos&gt;&lt;/cfdi:Concepto&gt;&lt;/cfdi:Conceptos&gt;&lt;cfdi:Impuestos TotalImpuestosRetenidos="258.40" TotalImpuestosTrasladados="200.05"&gt;&lt;cfdi:Retenciones&gt;&lt;cfdi:Retencion Impuesto="001" Importe="125.03"/&gt;&lt;cfdi:Retencion Impuesto="002" Importe="133.37"/&gt;&lt;/cfdi:Retenciones&gt;&lt;cfdi:Traslados&gt;&lt;cfdi:Traslado Base="1250.30" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="200.05"/&gt;&lt;/cfdi:Traslados&gt;&lt;/cfdi:Impuestos&gt;&lt;cfdi:Complemento&gt;&lt;tfd:TimbreFiscalDigital xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital" xsi:schemaLocation="http://www.sat.gob.mx/TimbreFiscalDigital http://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xsd" Version="1.1" SelloCFD="sx4EUAjHCu7urj4dTrqQjdX8hTD2C75vEcXIBXon0u5D1Yvj92/34pcC9cBijGPWTE/lBzWsOzfGIv9w5adM4FX+lk8wa953iIV4WLVv7u9Fy4OCd9ikZOGY+P4NEFQt+an06V6XC0qP9qikZ83Bd4GbFIiffZq8BdWuFHAkt+nSsfZo9/1yKBOCRJH3SQbSzkqoR64zuLfmQmLLKh9XbWEqbzv5Ztqql2/jhgWDzBzkKW40TeGWRb61rSaIawU59h2yxjKTzjO9G78/Ge+/x7VfmCieyfKRNACIrQwL7+5mQNWszI8eYzaO65ebQOc2MYKDNRzjEp7Vinu+giTbnw==" NoCertificadoSAT="30001000000500003456" RfcProvCertif="CVD110412TF6" UUID="C0AACAF9-9620-5BBD-9D73-4CF5E695B447" FechaTimbrado="2024-06-14T00:23:50" SelloSAT="ZqHDxhhoBeymC76L0CA+wrbVUHE/O2yF0hMLg3KSnKnD23k2qIbSyxggdGrbFc98GI8fOr8tb9cR387KYYKN+2qHIjvrrOJLq6pZI8k7SxCTGGcktMXGgyYHGqOw2dLAR5bb0Szg3lhfVDIlDGAPRJUQHkTfIfPh6Hjf6QkCmm9Kl4k3ucU+MpXNAKdhO3R7Kb7rENVZ2cl3QLb19Yd/qzX0PXaabEZDkqVS1PSeq1j2bdJVQSDvwhiVLp2bulRjdmRGvuDfgz5WALxhXA3Q6pb1sJmbfSnGgDWBvHJ+P1/dzgRHo9CKGFlFt2wE1sRkyD3YfcOuFGCnUdED2sbgdQ=="/&gt;&lt;/cfdi:Complemento&gt;&lt;/cfdi:Comprobante&gt;</s0:xml><s0:UUID>C0AACAF9-9620-5BBD-9D73-4CF5E695B447</s0:UUID><s0:Fecha>2024-06-14T00:23:50</s0:Fecha><s0:CodEstatus>Comprobante timbrado satisfactoriamente</s0:CodEstatus><s0:SatSeal>ZqHDxhhoBeymC76L0CA+wrbVUHE/O2yF0hMLg3KSnKnD23k2qIbSyxggdGrbFc98GI8fOr8tb9cR387KYYKN+2qHIjvrrOJLq6pZI8k7SxCTGGcktMXGgyYHGqOw2dLAR5bb0Szg3lhfVDIlDGAPRJUQHkTfIfPh6Hjf6QkCmm9Kl4k3ucU+MpXNAKdhO3R7Kb7rENVZ2cl3QLb19Yd/qzX0PXaabEZDkqVS1PSeq1j2bdJVQSDvwhiVLp2bulRjdmRGvuDfgz5WALxhXA3Q6pb1sJmbfSnGgDWBvHJ+P1/dzgRHo9CKGFlFt2wE1sRkyD3YfcOuFGCnUdED2sbgdQ==</s0:SatSeal><s0:Incidencias/><s0:NoCertificadoSAT>30001000000500003456</s0:NoCertificadoSAT></tns:quick_stampResult></tns:quick_stampResponse></senv:Body></senv:Envelope>'
        res = finkok.quick_stamp(invoice)

        assert verify_result(res.xml, filename="test_finkok_quick_stamp.xml")
        assert not res.pdf

        assert mk.called

        assert (
            mk.call_args.kwargs["url"]
            == "https://demo-facturacion.finkok.com/servicios/soap/stamp.wsdl"
        )


def test_finkok_stamp():
    signer = get_signer("eku9003173c9", get_csd=True)
    emisor = cfdi40.Emisor(
        rfc=signer.rfc, nombre=signer.legal_name, regimen_fiscal="601"
    )
    assert emisor["Nombre"] == "ESCUELA KEMPER URGATE"

    receptor = cfdi40.Receptor(
        rfc="ICV060329BY0",
        nombre="INMOBILIARIA CVA",
        uso_cfdi=UsoCFDI.GASTOS_EN_GENERAL,
        domicilio_fiscal_receptor="33826",
        regimen_fiscal_receptor=RegimenFiscal.GENERAL_DE_LEY_PERSONAS_MORALES,
    )

    concepto = cfdi40.Concepto(
        clave_prod_serv="84111506",
        cantidad=Decimal("1.00"),
        clave_unidad="E48",
        descripcion="SERVICIOS DE FACTURACION",
        valor_unitario=Decimal("1250.30"),
        impuestos=cfdi40.Impuestos(
            traslados=cfdi40.Traslado(
                impuesto=Impuesto.IVA,
                tipo_factor=TipoFactor.TASA,
                tasa_o_cuota=Decimal("0.160000"),
            ),
            retenciones=[
                cfdi40.Retencion(
                    impuesto=Impuesto.ISR,
                    tipo_factor=TipoFactor.TASA,
                    tasa_o_cuota=Decimal("0.100000"),
                ),
                cfdi40.Retencion(
                    impuesto=Impuesto.IVA,
                    tipo_factor=TipoFactor.TASA,
                    tasa_o_cuota=Decimal("0.106667"),
                ),
            ],
        ),
        _traslados_incluidos=False,  # indica si el valor unitario incluye los traslados
    )

    invoice = cfdi40.Comprobante(
        emisor=emisor,
        lugar_expedicion="27200",
        receptor=receptor,
        metodo_pago="PPD",
        forma_pago="99",
        serie="T",
        folio="1000",
        conceptos=concepto,
    )

    invoice.sign(signer)
    invoice = invoice.process()

    with mock.patch(f"requests.post") as mk:
        mk.return_value.ok = True
        mk.return_value.content = b'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<senv:Envelope xmlns:plink="http://schemas.xmlsoap.org/ws/2003/05/partner-link/" xmlns:s0="apps.services.soap.core.views" xmlns:s1="https://facturacion.finkok.com/servicios/async" xmlns:s12enc="http://www.w3.org/2003/05/soap-encoding/" xmlns:s12env="http://www.w3.org/2003/05/soap-envelope/" xmlns:senc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:senv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:tns="http://facturacion.finkok.com/stamp" xmlns:wsa="http://schemas.xmlsoap.org/ws/2003/03/addressing" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><senv:Body><tns:stampResponse><tns:stampResult><s0:xml>&lt;?xml version="1.0" encoding="utf-8"?&gt;\n&lt;cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="4.0" Serie="T" Folio="1000" Fecha="2024-06-12T02:20:01" Sello="ostBHcr0fwGA85FvvwnPMmtyxTtZhaxID1tx6xBLChdFFIsfknYKSew0/R1kXplYpTLUfI31ZaztljNoiKJ6GIwwefqXlRmQ/L6gveSYjiXu8rfdzp9lVC5DYuVfI5evmh8nW2/washZPMrldl0Nw/YgDquB1ZZXsptxqCHURR2GO/2FK6319mLV0N9u2VwcAK9kgHcewnOZVcsL9f2NYXAzI8XRfHFXYZHjnrEN/YAhwvJUhXWYbKs8+ZBziN8NNp9IHa7s3FChCeR380leeO6Q6Hgnpc2UOo1PWECBujiNAcjYvo72WnOuws5mYmdN2tBdmN8PciVqPwf635je/w==" FormaPago="99" NoCertificado="30001000000500003416" Certificado="MIIFsDCCA5igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0MTYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTE0MzUxWhcNMjcwNTE4MTE0MzUxWjCB1zEnMCUGA1UEAxMeRVNDVUVMQSBLRU1QRVIgVVJHQVRFIFNBIERFIENWMScwJQYDVQQpEx5FU0NVRUxBIEtFTVBFUiBVUkdBVEUgU0EgREUgQ1YxJzAlBgNVBAoTHkVTQ1VFTEEgS0VNUEVSIFVSR0FURSBTQSBERSBDVjElMCMGA1UELRMcRUtVOTAwMzE3M0M5IC8gVkFEQTgwMDkyN0RKMzEeMBwGA1UEBRMVIC8gVkFEQTgwMDkyN0hTUlNSTDA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtmecO6n2GS0zL025gbHGQVxznPDICoXzR2uUngz4DqxVUC/w9cE6FxSiXm2ap8Gcjg7wmcZfm85EBaxCx/0J2u5CqnhzIoGCdhBPuhWQnIh5TLgj/X6uNquwZkKChbNe9aeFirU/JbyN7Egia9oKH9KZUsodiM/pWAH00PCtoKJ9OBcSHMq8Rqa3KKoBcfkg1ZrgueffwRLws9yOcRWLb02sDOPzGIm/jEFicVYt2Hw1qdRE5xmTZ7AGG0UHs+unkGjpCVeJ+BEBn0JPLWVvDKHZAQMj6s5Bku35+d/MyATkpOPsGT/VTnsouxekDfikJD1f7A1ZpJbqDpkJnss3vQIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAFaUgj5PqgvJigNMgtrdXZnbPfVBbukAbW4OGnUhNrA7SRAAfv2BSGk16PI0nBOr7qF2mItmBnjgEwk+DTv8Zr7w5qp7vleC6dIsZFNJoa6ZndrE/f7KO1CYruLXr5gwEkIyGfJ9NwyIagvHHMszzyHiSZIA850fWtbqtythpAliJ2jF35M5pNS+YTkRB+T6L/c6m00ymN3q9lT1rB03YywxrLreRSFZOSrbwWfg34EJbHfbFXpCSVYdJRfiVdvHnewN0r5fUlPtR9stQHyuqewzdkyb5jTTw02D2cUfL57vlPStBj7SEi3uOWvLrsiDnnCIxRMYJ2UA2ktDKHk+zWnsDmaeleSzonv2CHW42yXYPCvWi88oE1DJNYLNkIjua7MxAnkNZbScNw01A6zbLsZ3y8G6eEYnxSTRfwjd8EP4kdiHNJftm7Z4iRU7HOVh79/lRWB+gd171s3d/mI9kte3MRy6V8MMEMCAnMboGpaooYwgAmwclI2XZCczNWXfhaWe0ZS5PmytD/GDpXzkX0oEgY9K/uYo5V77NdZbGAjmyi8cE2B2ogvyaN2XfIInrZPgEffJ4AB7kFA2mwesdLOCh0BLD9itmCve3A1FGR4+stO2ANUoiI3w3Tv2yQSg4bjeDlJ08lXaaFCLW2peEXMXjQUk7fmpb5MNuOUTW6BE=" SubTotal="1250.30" Moneda="MXN" Total="1191.95" TipoDeComprobante="I" Exportacion="01" MetodoPago="PPD" LugarExpedicion="27200" xsi:schemaLocation="http://www.sat.gob.mx/cfd/4 http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd"&gt;&lt;cfdi:Emisor Rfc="EKU9003173C9" Nombre="ESCUELA KEMPER URGATE" RegimenFiscal="601"/&gt;&lt;cfdi:Receptor Rfc="ICV060329BY0" Nombre="INMOBILIARIA CVA" DomicilioFiscalReceptor="33826" RegimenFiscalReceptor="601" UsoCFDI="G03"/&gt;&lt;cfdi:Conceptos&gt;&lt;cfdi:Concepto ClaveProdServ="84111506" Cantidad="1.00" ClaveUnidad="E48" Descripcion="SERVICIOS DE FACTURACION" ValorUnitario="1250.30" Importe="1250.30" ObjetoImp="02"&gt;&lt;cfdi:Impuestos&gt;&lt;cfdi:Traslados&gt;&lt;cfdi:Traslado Base="1250.30" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="200.05"/&gt;&lt;/cfdi:Traslados&gt;&lt;cfdi:Retenciones&gt;&lt;cfdi:Retencion Base="1250.30" Impuesto="001" TipoFactor="Tasa" TasaOCuota="0.100000" Importe="125.03"/&gt;&lt;cfdi:Retencion Base="1250.30" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.106667" Importe="133.37"/&gt;&lt;/cfdi:Retenciones&gt;&lt;/cfdi:Impuestos&gt;&lt;/cfdi:Concepto&gt;&lt;/cfdi:Conceptos&gt;&lt;cfdi:Impuestos TotalImpuestosRetenidos="258.40" TotalImpuestosTrasladados="200.05"&gt;&lt;cfdi:Retenciones&gt;&lt;cfdi:Retencion Impuesto="001" Importe="125.03"/&gt;&lt;cfdi:Retencion Impuesto="002" Importe="133.37"/&gt;&lt;/cfdi:Retenciones&gt;&lt;cfdi:Traslados&gt;&lt;cfdi:Traslado Base="1250.30" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="200.05"/&gt;&lt;/cfdi:Traslados&gt;&lt;/cfdi:Impuestos&gt;&lt;cfdi:Complemento&gt;&lt;tfd:TimbreFiscalDigital xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital" xsi:schemaLocation="http://www.sat.gob.mx/TimbreFiscalDigital http://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xsd" Version="1.1" SelloCFD="ostBHcr0fwGA85FvvwnPMmtyxTtZhaxID1tx6xBLChdFFIsfknYKSew0/R1kXplYpTLUfI31ZaztljNoiKJ6GIwwefqXlRmQ/L6gveSYjiXu8rfdzp9lVC5DYuVfI5evmh8nW2/washZPMrldl0Nw/YgDquB1ZZXsptxqCHURR2GO/2FK6319mLV0N9u2VwcAK9kgHcewnOZVcsL9f2NYXAzI8XRfHFXYZHjnrEN/YAhwvJUhXWYbKs8+ZBziN8NNp9IHa7s3FChCeR380leeO6Q6Hgnpc2UOo1PWECBujiNAcjYvo72WnOuws5mYmdN2tBdmN8PciVqPwf635je/w==" NoCertificadoSAT="30001000000500003456" RfcProvCertif="CVD110412TF6" UUID="1E5A6E1B-9C1B-5319-BFED-123BD143A310" FechaTimbrado="2024-06-12T02:20:02" SelloSAT="OABh90l0f9SLE19tfHsKg5XtpZOUXU8rsmUAxpWUf25xHJrl3Ta+W1+W28iG+tOtNoY26Lja4uCTq9F7QcFAfF7fN3Hfw6k/XYUpLqBlIKi51iq8FYJhbPFW8eQMxVv0bmtNW8JfvAYSe4qv6zyNye1+qvq8hdpankUgwG7HIgjKuxwPDPw8yfrrdcokz82XBFmuM0NaKkg32J5k4e7fiWyfNDxjNI2dt5PvX8RY7OWcx1N3XYmKbPII2/a5+yRfs0TUpt7YD6iWU3F0P8pWPDJonJAt0l07OcsRVd3+M+efqqyzGhaZ0t5tYR83rDgMOnvi1E8Rn55T3v49SbQvvw=="/&gt;&lt;/cfdi:Complemento&gt;&lt;/cfdi:Comprobante&gt;</s0:xml><s0:UUID>1E5A6E1B-9C1B-5319-BFED-123BD143A310</s0:UUID><s0:Fecha>2024-06-12T02:20:02</s0:Fecha><s0:CodEstatus>Comprobante timbrado satisfactoriamente</s0:CodEstatus><s0:SatSeal>OABh90l0f9SLE19tfHsKg5XtpZOUXU8rsmUAxpWUf25xHJrl3Ta+W1+W28iG+tOtNoY26Lja4uCTq9F7QcFAfF7fN3Hfw6k/XYUpLqBlIKi51iq8FYJhbPFW8eQMxVv0bmtNW8JfvAYSe4qv6zyNye1+qvq8hdpankUgwG7HIgjKuxwPDPw8yfrrdcokz82XBFmuM0NaKkg32J5k4e7fiWyfNDxjNI2dt5PvX8RY7OWcx1N3XYmKbPII2/a5+yRfs0TUpt7YD6iWU3F0P8pWPDJonJAt0l07OcsRVd3+M+efqqyzGhaZ0t5tYR83rDgMOnvi1E8Rn55T3v49SbQvvw==</s0:SatSeal><s0:Incidencias/><s0:NoCertificadoSAT>30001000000500003456</s0:NoCertificadoSAT></tns:stampResult></tns:stampResponse></senv:Body></senv:Envelope>'
        res = finkok.stamp(invoice)

        assert verify_result(res.xml, filename="test_finkok_stamp.xml")
        assert not res.pdf

        assert mk.called

        assert (
            mk.call_args.kwargs["url"]
            == "https://demo-facturacion.finkok.com/servicios/soap/stamp.wsdl"
        )