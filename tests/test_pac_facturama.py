import json
from datetime import date, datetime
from decimal import Decimal
from unittest import mock

from requests.auth import HTTPBasicAuth

from satcfdi.create.cfd import cfdi40, nomina12, pago20, donat11, leyendasFisc10, implocal10, cce20
from satcfdi.create.cfd.catalogos import Impuesto, TipoFactor
from satcfdi.pacs import Accept, CancelReason, Environment
from satcfdi.pacs.facturama import Facturama, FacturamaWeb, cfdi_to_facturama_payload
from .utils import get_signer, verify_result


def _sample_invoice():
    signer = get_signer("xiqb891116qe4")
    invoice = cfdi40.Comprobante(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601",
        ),
        lugar_expedicion="27200",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="URE180429TM6",
            nombre="UNIVERSIDAD ROBOTICA ESPAÑOLA",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="65000",
            regimen_fiscal_receptor="601",
        ),
        metodo_pago="PPD",
        forma_pago="99",
        serie="T",
        folio="1000",
        conceptos=cfdi40.Concepto(
            clave_prod_serv="10101702",
            cantidad=Decimal("1.00"),
            clave_unidad="E48",
            descripcion="SERVICIOS DE RENTA",
            valor_unitario=Decimal("100.00"),
            impuestos=cfdi40.Impuestos(
                traslados=cfdi40.Traslado(
                    impuesto=Impuesto.IVA,
                    tipo_factor=TipoFactor.TASA,
                    tasa_o_cuota=Decimal("0.160000"),
                ),
                retenciones=[
                    cfdi40.Traslado(
                        impuesto=Impuesto.ISR,
                        tipo_factor=TipoFactor.TASA,
                        tasa_o_cuota=Decimal("0.100000"),
                    ),
                ],
            ),
        ),
    )
    return invoice


def test_cfdi_to_facturama_payload():
    payload = cfdi_to_facturama_payload(_sample_invoice())
    verify = verify_result(
        data=json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True),
        filename="test_payload.json",
    )
    assert verify
    assert payload["CfdiType"] == "I"
    assert payload["Issuer"]["Rfc"] == "XIQB891116QE4"
    assert payload["Items"][0]["Taxes"]


def test_facturama_issue():
    pac = Facturama(
        username="user",
        password="password",
        environment=Environment.TEST,
    )
    invoice = _sample_invoice()

    with mock.patch("requests.request") as mk:
        create_response = mock.Mock()
        create_response.ok = True
        create_response.content = b'{"Id":"abc123","Uuid":"6d7434a6-e3f2-47ad-9e4c-08849946afa0"}'
        create_response.headers = {"Content-Type": "application/json"}
        create_response.json = mock.Mock(
            return_value={
                "Id": "abc123",
                "Uuid": "6d7434a6-e3f2-47ad-9e4c-08849946afa0",
            }
        )

        xml_response = mock.Mock()
        xml_response.ok = True
        xml_response.content = b'{"Content":"PD94bWwgdmVyc2lvbj0iMS4wIj8+PGNmZGk+dGVzdDwvY2ZkaT4="}'
        xml_response.headers = {"Content-Type": "application/json"}
        xml_response.json = mock.Mock(
            return_value={
                # base64url of: <?xml version="1.0"?><cfdi>test</cfdi>
                "Content": "PD94bWwgdmVyc2lvbj0iMS4wIj8+PGNmZGk+dGVzdDwvY2ZkaT4=",
            }
        )
        mk.side_effect = [create_response, xml_response]

        res = pac.issue(cfdi=invoice, accept=Accept.XML)

        assert res.document_id == "abc123"
        assert res.xml.startswith(b"<?xml")
        assert mk.call_count == 2
        assert mk.call_args_list[0].kwargs["auth"] == HTTPBasicAuth("user", "password")
        assert mk.call_args_list[0].kwargs["url"].endswith("api-lite/3/cfdis")

        # Normalize volatile headers for golden file
        for call in mk.call_args_list:
            call.kwargs["headers"]["User-Agent"] = "this is a test"
            call.kwargs["auth"] = "Basic abc"

        args = json.dumps(
            [c.kwargs for c in mk.call_args_list],
            indent=2,
            default=str,
            ensure_ascii=False,
            sort_keys=True,
        )
        verify = verify_result(data=args, filename="test_issue.json")
        assert verify


def test_facturama_stamp_not_supported():
    pac = Facturama("user", "password", Environment.TEST)
    try:
        pac.stamp(_sample_invoice())
        assert False, "expected NotImplementedError"
    except NotImplementedError as exc:
        assert "issue()" in str(exc)


def test_facturama_recover_and_cancel():
    pac = Facturama("user", "password", Environment.TEST)

    with mock.patch("requests.request") as mk:
        xml_response = mock.Mock()
        xml_response.ok = True
        xml_response.content = b'{"Content":"PD94bWwgdmVyc2lvbj0iMS4wIj8+PGNmZGk+dGVzdDwvY2ZkaT4="}'
        xml_response.headers = {"Content-Type": "application/json"}
        xml_response.json = mock.Mock(
            return_value={"Content": "PD94bWwgdmVyc2lvbj0iMS4wIj8+PGNmZGk+dGVzdDwvY2ZkaT4="}
        )

        cancel_response = mock.Mock()
        cancel_response.ok = True
        cancel_response.content = b'{"Status":"canceled"}'
        cancel_response.headers = {"Content-Type": "application/json"}
        cancel_response.json = mock.Mock(return_value={"Status": "canceled"})

        mk.side_effect = [xml_response, cancel_response]

        recovered = pac.recover("abc123", accept=Accept.XML)
        assert recovered.document_id == "abc123"
        assert recovered.xml.startswith(b"<?xml")

        from satcfdi.cfdi import CFDI

        cfdi = CFDI(
            {
                "Emisor": {"Rfc": "XIQB891116QE4"},
                "Complemento": {
                    "TimbreFiscalDigital": {
                        "UUID": "6D7434A6-E3F2-47AD-9E4C-08849946AFA0"
                    }
                },
            }
        )
        ack = pac.cancel(
            cfdi=cfdi,
            reason=CancelReason.COMPROBANTE_EMITIDO_CON_ERRORES_SIN_RELACION,
            document_id="abc123",
        )
        assert ack.code == "canceled"
        assert mk.call_args_list[1].kwargs["params"]["motive"] == "02"


def test_facturama_upload_csd():
    pac = Facturama("user", "password", Environment.TEST)
    with mock.patch("requests.request") as mk:
        mk.return_value.ok = True
        mk.return_value.content = b'{"Rfc":"XIQB891116QE4"}'
        mk.return_value.headers = {"Content-Type": "application/json"}
        mk.return_value.json = mock.Mock(return_value={"Rfc": "XIQB891116QE4"})

        pac.upload_csd(
            rfc="xiqb891116qe4",
            certificate=b"CER",
            key=b"KEY",
            password="secret",
        )
        assert mk.called
        body = mk.call_args.kwargs["json"]
        assert body["Rfc"] == "XIQB891116QE4"
        assert body["Certificate"]
        assert body["PrivateKey"]
        assert body["PrivateKeyPassword"] == "secret"
        assert mk.call_args.kwargs["url"].endswith("api-lite/csds")


def test_cfdi_to_facturama_payload_pago():
    signer = get_signer("xiqb891116qe4")
    invoice = cfdi40.Comprobante.pago(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601",
        ),
        lugar_expedicion="27200",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="URE180429TM6",
            nombre="UNIVERSIDAD ROBOTICA ESPAÑOLA",
            uso_cfdi="CP01",
            domicilio_fiscal_receptor="65000",
            regimen_fiscal_receptor="601",
        ),
        serie="P",
        folio="10",
        complemento_pago=pago20.Pagos(
            pago=pago20.Pago(
                fecha_pago=datetime.fromisoformat("2022-04-10T12:00:00"),
                forma_de_pago_p="03",
                moneda_p="MXN",
                monto=Decimal("1500.00"),
                tipo_cambio_p=1,
                docto_relacionado=(
                    docto := pago20.DoctoRelacionado(
                        id_documento="C94C8AF3-C774-4D4C-802E-781411934A6E",
                        moneda_dr="MXN",
                        num_parcialidad=1,
                        imp_saldo_ant=Decimal("2000.00"),
                        imp_pagado=Decimal("1500.00"),
                        objeto_imp_dr="01",
                        serie="BQ",
                        folio="2205",
                    )
                ),
            )
        ),
    )
    docto["MetodoDePagoDR"] = "PPD"

    payload = cfdi_to_facturama_payload(invoice)
    verify = verify_result(
        data=json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True),
        filename="test_payload_pago.json",
    )
    assert verify
    assert payload["CfdiType"] == "P"
    assert "Items" not in payload
    assert payload["Complemento"]["Payments"][0]["Amount"] == 1500.0
    assert payload["Complemento"]["Payments"][0]["RelatedDocuments"][0]["Uuid"] == (
        "C94C8AF3-C774-4D4C-802E-781411934A6E"
    )


def test_cfdi_to_facturama_payload_nomina():
    signer = get_signer("xiqb891116qe4")
    invoice = cfdi40.Comprobante.nomina(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601",
        ),
        lugar_expedicion="27200",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="FUNK671228PH6",
            nombre="KARLA FUENTE NOLASCO",
            uso_cfdi="CN01",
            domicilio_fiscal_receptor="83200",
            regimen_fiscal_receptor="605",
        ),
        serie="N",
        folio="1",
        complemento_nomina=nomina12.Nomina(
            tipo_nomina="O",
            fecha_pago=date(2019, 9, 6),
            fecha_inicial_pago=date(2019, 8, 22),
            fecha_final_pago=date(2019, 9, 6),
            num_dias_pagados=Decimal("15"),
            emisor=nomina12.Emisor(registro_patronal="B5510768108"),
            receptor=nomina12.Receptor(
                curp="GAMA800912MSPRRD05",
                num_seguridad_social="92919084431",
                tipo_contrato="01",
                tipo_regimen="02",
                num_empleado="006",
                periodicidad_pago="04",
                clave_ent_fed="SLP",
                sindicalizado="No",
                tipo_jornada="01",
                riesgo_puesto="1",
                salario_diario_integrado=Decimal("50.00"),
                fecha_inicio_rel_laboral=date(2019, 1, 1),
            ),
            percepciones=nomina12.Percepciones(
                percepcion=nomina12.Percepcion(
                    tipo_percepcion="046",
                    clave="046",
                    concepto="ASIMILIADOS A SALARIOS",
                    importe_gravado=Decimal("3621.18"),
                    importe_exento=Decimal("0"),
                )
            ),
            deducciones=nomina12.Deducciones(
                deduccion=nomina12.Deduccion(
                    tipo_deduccion="002",
                    clave="002",
                    concepto="ISR",
                    importe=Decimal("272.60"),
                )
            ),
            otros_pagos=nomina12.OtroPago(
                tipo_otro_pago="002",
                clave="000",
                concepto="Subsidio",
                importe=Decimal("10"),
                subsidio_al_empleo=Decimal("10"),
            ),
        ),
    )
    payload = cfdi_to_facturama_payload(invoice)
    verify = verify_result(
        data=json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True),
        filename="test_payload_nomina.json",
    )
    assert verify
    assert payload["CfdiType"] == "N"
    assert payload["Complemento"]["Payroll"]["Type"] == "O"
    assert payload["Complemento"]["Payroll"]["Employee"]["Curp"] == "GAMA800912MSPRRD05"
    assert payload["Complemento"]["Payroll"]["OtherPayments"][0]["EmploymentSubsidy"]["Amount"] == 10.0


def test_cfdi_to_facturama_payload_traslado():
    signer = get_signer("xiqb891116qe4")
    invoice = cfdi40.Comprobante(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601",
        ),
        lugar_expedicion="27200",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="URE180429TM6",
            nombre="UNIVERSIDAD ROBOTICA ESPAÑOLA",
            uso_cfdi="S01",
            domicilio_fiscal_receptor="65000",
            regimen_fiscal_receptor="601",
        ),
        tipo_de_comprobante="T",
        serie="TR",
        folio="1",
        conceptos=cfdi40.Concepto(
            clave_prod_serv="24111506",
            cantidad=Decimal("1"),
            clave_unidad="H87",
            descripcion="MERCANCIA EN TRASLADO",
            valor_unitario=Decimal("0"),
            objeto_imp="01",
        ),
    )
    payload = cfdi_to_facturama_payload(invoice)
    assert payload["CfdiType"] == "T"
    assert payload["Items"][0]["ProductCode"] == "24111506"


def _sample_carta_porte_traslado():
    from satcfdi.create.cfd import cartaporte31 as cp

    signer = get_signer("xiqb891116qe4")
    carta = cp.CartaPorte(
        id_ccp="CCCBB0A0-A0A0-0A00-000A-0A0A000A000A",
        transp_internac="No",
        total_dist_rec=Decimal("120.5"),
        ubicaciones=[
            cp.Ubicacion(
                tipo_ubicacion="Origen",
                rfc_remitente_destinatario=signer.rfc,
                fecha_hora_salida_llegada=datetime.fromisoformat("2022-05-16T15:15:00"),
                id_ubicacion="OR000001",
                domicilio=cp.Domicilio(
                    estado="SLP",
                    pais="MEX",
                    codigo_postal="78000",
                    municipio="028",
                    localidad="05",
                ),
            ),
            cp.Ubicacion(
                tipo_ubicacion="Destino",
                rfc_remitente_destinatario="URE180429TM6",
                fecha_hora_salida_llegada=datetime.fromisoformat("2022-05-16T18:15:00"),
                id_ubicacion="DE000001",
                distancia_recorrida=Decimal("120.5"),
                domicilio=cp.Domicilio(
                    estado="SLP",
                    pais="MEX",
                    codigo_postal="78000",
                    municipio="028",
                    localidad="05",
                ),
            ),
        ],
        mercancias=cp.Mercancias(
            peso_bruto_total=Decimal("1"),
            unidad_peso="KGM",
            num_total_mercancias=1,
            mercancia=cp.Mercancia(
                bienes_transp="11121900",
                descripcion="Accesorios de equipo de telefonía",
                cantidad=Decimal("1"),
                clave_unidad="XBX",
                peso_en_kg=Decimal("1"),
                material_peligroso="No",
                cantidad_transporta=cp.CantidadTransporta(
                    cantidad=Decimal("1"),
                    id_origen="OR000001",
                    id_destino="DE000001",
                ),
            ),
            autotransporte=cp.Autotransporte(
                perm_sct="TPAF01",
                num_permiso_sct="NumPermisoSCT1",
                identificacion_vehicular=cp.IdentificacionVehicular(
                    config_vehicular="VL",
                    peso_bruto_vehicular=Decimal("1"),
                    placa_vm="ABC1234",
                    anio_modelo_vm=2020,
                ),
                seguros=cp.Seguros(
                    asegura_resp_civil="AseguraRespCivil",
                    poliza_resp_civil="123456789",
                ),
                remolques=cp.Remolque(sub_tipo_rem="CTR004", placa="VL45K98"),
            ),
        ),
        figura_transporte=cp.TiposFigura(
            tipo_figura="01",
            nombre_figura="Operador Uno",
            rfc_figura="EKU9003173C9",
            num_licencia="NumLicencia1",
            domicilio=cp.Domicilio(
                estado="SLP",
                pais="MEX",
                codigo_postal="78000",
                calle="Calle1",
                numero_exterior="100",
            ),
        ),
    )
    return cfdi40.Comprobante(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601",
        ),
        lugar_expedicion="78000",
        fecha=datetime.fromisoformat("2022-05-16T15:00:00"),
        receptor=cfdi40.Receptor(
            rfc="URE180429TM6",
            nombre="UNIVERSIDAD ROBOTICA ESPAÑOLA",
            uso_cfdi="S01",
            domicilio_fiscal_receptor="65000",
            regimen_fiscal_receptor="601",
        ),
        tipo_de_comprobante="T",
        exportacion="01",
        serie="CP",
        folio="1",
        conceptos=cfdi40.Concepto(
            clave_prod_serv="24111506",
            cantidad=Decimal("1"),
            clave_unidad="H87",
            descripcion="MERCANCIA EN TRASLADO",
            valor_unitario=Decimal("0"),
            objeto_imp="01",
        ),
        complemento=carta,
    )


def test_cfdi_to_facturama_payload_carta_porte():
    payload = cfdi_to_facturama_payload(_sample_carta_porte_traslado())
    verify = verify_result(
        data=json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True),
        filename="test_payload_carta_porte.json",
    )
    assert verify
    assert payload["CfdiType"] == "T"
    assert payload["NameId"] == "36"
    cp = payload["Complemento"]["CartaPorte31"]
    assert cp["TranspInternac"] == "No"
    assert cp["IdCCP"] == "CCCBB0A0-A0A0-0A00-000A-0A0A000A000A"
    assert len(cp["Ubicaciones"]) == 2
    assert cp["Ubicaciones"][0]["FechaHoraSalidaLlegada"] == "2022-05-16 15:15:00"
    assert cp["Mercancias"]["Autotransporte"]["PermSCT"] == "TPAF01"
    assert cp["Mercancias"]["Autotransporte"]["Remolques"][0]["Placa"] == "VL45K98"
    assert cp["Mercancias"]["Mercancia"][0]["CantidadTransporta"][0]["IDOrigen"] == (
        "OR000001"
    )
    assert cp["FiguraTransporte"][0]["TipoFigura"] == "01"
    assert cp["FiguraTransporte"][0]["NumLicencia"] == "NumLicencia1"


def test_cfdi_to_facturama_payload_carta_porte_nested_key():
    """Complemento as dict with CartaPorte key (XML-parsed shape)."""
    invoice = _sample_carta_porte_traslado()
    carta = invoice["Complemento"]
    invoice["Complemento"] = {"CartaPorte": carta}
    payload = cfdi_to_facturama_payload(invoice)
    assert payload["NameId"] == "36"
    assert payload["Complemento"]["CartaPorte31"]["TranspInternac"] == "No"
    assert payload["Complemento"]["CartaPorte31"]["Mercancias"]["NumTotalMercancias"] == 1


def test_cfdi_to_facturama_payload_carta_porte_partes_transporte():
    from satcfdi.create.cfd import cartaporte31 as cp

    invoice = _sample_carta_porte_traslado()
    invoice["Complemento"]["FiguraTransporte"] = cp.TiposFigura(
        tipo_figura="02",
        nombre_figura="Propietario",
        rfc_figura="EKU9003173C9",
        partes_transporte=["PT01", "PT02"],
    )
    payload = cfdi_to_facturama_payload(invoice)
    figura = payload["Complemento"]["CartaPorte31"]["FiguraTransporte"][0]
    assert figura["PartesTransporte"] == [
        {"ParteTransporte": "PT01"},
        {"ParteTransporte": "PT02"},
    ]


def test_cfdi_to_facturama_payload_donation():
    signer = get_signer("xiqb891116qe4")
    invoice = cfdi40.Comprobante(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601",
        ),
        lugar_expedicion="51873",
        fecha=datetime.fromisoformat("2019-06-19T13:45:00"),
        receptor=cfdi40.Receptor(
            rfc="MISC491214B86",
            nombre="CECILIA MIRANDA SANCHEZ",
            uso_cfdi="D04",
            domicilio_fiscal_receptor="65010",
            regimen_fiscal_receptor="605",
        ),
        forma_pago="12",
        metodo_pago="PUE",
        serie="D",
        folio="94",
        conceptos=cfdi40.Concepto(
            clave_prod_serv="20102000",
            cantidad=Decimal("3"),
            clave_unidad="EA",
            descripcion="Cobija de lana y algodon",
            valor_unitario=Decimal("1000"),
            objeto_imp="01",
        ),
        complemento=donat11.Donatarias(
            no_autorizacion="B400-05-08-2014-005",
            fecha_autorizacion=date(2019, 1, 30),
            leyenda="El comprobante es un donativo",
        ),
    )
    payload = cfdi_to_facturama_payload(invoice)
    verify = verify_result(
        data=json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True),
        filename="test_payload_donation.json",
    )
    assert verify
    assert payload["NameId"] == "9"
    assert payload["Complemento"]["Donation"] == {
        "AuthorizationDate": "30/01/2019",
        "AuthorizationNumber": "B400-05-08-2014-005",
        "Legend": "El comprobante es un donativo",
    }


def test_cfdi_to_facturama_payload_tax_legends():
    signer = get_signer("xiqb891116qe4")
    invoice = cfdi40.Comprobante(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601",
        ),
        lugar_expedicion="78116",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="URE180429TM6",
            nombre="UNIVERSIDAD ROBOTICA ESPAÑOLA",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="65000",
            regimen_fiscal_receptor="601",
        ),
        forma_pago="01",
        metodo_pago="PUE",
        conceptos=cfdi40.Concepto(
            clave_prod_serv="20102001",
            cantidad=Decimal("1"),
            clave_unidad="E48",
            descripcion="Servicio",
            valor_unitario=Decimal("100"),
            objeto_imp="01",
        ),
        complemento=leyendasFisc10.LeyendasFiscales(
            leyenda=leyendasFisc10.Leyenda(
                texto_leyenda="EXPORTADOR #####",
                disposicion_fiscal="ISR",
                norma="Art22",
            )
        ),
    )
    payload = cfdi_to_facturama_payload(invoice)
    assert payload["Complemento"]["TaxLegends"]["Legends"] == [
        {"TaxProvision": "ISR", "Norm": "Art22", "Text": "EXPORTADOR #####"}
    ]


def test_cfdi_to_facturama_payload_impuestos_locales():
    signer = get_signer("xiqb891116qe4")
    invoice = cfdi40.Comprobante(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601",
        ),
        lugar_expedicion="27200",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="URE180429TM6",
            nombre="UNIVERSIDAD ROBOTICA ESPAÑOLA",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="65000",
            regimen_fiscal_receptor="601",
        ),
        forma_pago="01",
        metodo_pago="PUE",
        conceptos=cfdi40.Concepto(
            clave_prod_serv="90111501",
            cantidad=Decimal("1"),
            clave_unidad="E48",
            descripcion="Hospedaje",
            valor_unitario=Decimal("1000"),
            impuestos=cfdi40.Impuestos(
                traslados=cfdi40.Traslado(
                    impuesto=Impuesto.IVA,
                    tipo_factor=TipoFactor.TASA,
                    tasa_o_cuota=Decimal("0.160000"),
                ),
            ),
        ),
        complemento=implocal10.ImpuestosLocales(
            total_de_retenciones=Decimal("0"),
            total_de_traslados=Decimal("40"),
            traslados_locales=implocal10.TrasladosLocales(
                imp_loc_trasladado="IMPUESTO DE HOSPEDAJE",
                tasa_de_traslado=Decimal("4.00"),
                importe=Decimal("40.00"),
            ),
        ),
    )
    payload = cfdi_to_facturama_payload(invoice)
    taxes = payload["Items"][0]["Taxes"]
    assert taxes[0]["IsFederalTax"] is True
    assert taxes[0]["Name"] == "IVA"
    assert taxes[1] == {
        "Name": "IMPUESTO DE HOSPEDAJE",
        "Rate": 4.0,
        "Total": 40.0,
        "Base": 0.0,
        "IsRetention": False,
        "IsQuota": False,
        "IsFederalTax": False,
    }
    assert payload["Items"][0]["Total"] == 1200.0  # 1000 + 160 IVA + 40 local


def test_cfdi_to_facturama_payload_foreign_trade_requires_web():
    signer = get_signer("xiqb891116qe4")
    cce = cce20.ComercioExterior(
        clave_de_pedimento="A1",
        certificado_origen=0,
        tipo_cambio_usd=Decimal("18.78"),
        total_usd=Decimal("100"),
        mercancias=cce20.Mercancia(
            no_identificacion="CX-000988",
            valor_dolares=Decimal("100"),
            fraccion_arancelaria="94059102",
            cantidad_aduana=Decimal("1"),
            unidad_aduana="01",
            valor_unitario_aduana=Decimal("100"),
        ),
        emisor=cce20.Emisor(
            domicilio=cce20.Domicilio(
                calle="Canada de Gomez",
                estado="SLP",
                pais="MEX",
                codigo_postal="78216",
                numero_exterior="110",
                municipio="028",
            )
        ),
        receptor=cce20.Receptor(
            num_reg_id_trib="123456789",
            domicilio=cce20.Domicilio(
                calle="Main St",
                estado="TX",
                pais="USA",
                codigo_postal="75001",
                numero_exterior="1",
            ),
        ),
        incoterm="CFR",
    )
    invoice = cfdi40.Comprobante(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601",
        ),
        lugar_expedicion="78116",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="XEXX010101000",
            nombre="JOSE ALBERTO LOPEZ",
            uso_cfdi="S01",
            domicilio_fiscal_receptor="78116",
            regimen_fiscal_receptor="616",
            residencia_fiscal="USA",
            num_reg_id_trib="123456789",
        ),
        forma_pago="01",
        metodo_pago="PUE",
        exportacion="02",
        conceptos=cfdi40.Concepto(
            clave_prod_serv="41106300",
            no_identificacion="CX-000988",
            cantidad=Decimal("1"),
            clave_unidad="EA",
            descripcion="ABACO",
            valor_unitario=Decimal("100"),
            objeto_imp="02",
            impuestos=cfdi40.Impuestos(
                traslados=cfdi40.Traslado(
                    impuesto=Impuesto.IVA,
                    tipo_factor=TipoFactor.TASA,
                    tasa_o_cuota=Decimal("0.160000"),
                ),
            ),
        ),
        complemento=cce,
    )
    try:
        cfdi_to_facturama_payload(invoice)
        assert False, "expected NotImplementedError"
    except NotImplementedError as exc:
        assert "FacturamaWeb" in str(exc)

    payload = cfdi_to_facturama_payload(invoice, allow_foreign_trade=True)
    verify = verify_result(
        data=json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True),
        filename="test_payload_foreign_trade.json",
    )
    assert verify
    assert payload["NameId"] == "26"
    assert payload["Receiver"]["TaxRegistrationNumber"] == "123456789"
    assert payload["Receiver"]["TaxResidence"] == "USA"
    ft = payload["Complemento"]["ForeignTrade"]
    assert ft["RequestCode"] == "A1"
    assert ft["OriginCertificate"] is False
    assert ft["Commodity"][0]["IdentificationNumber"] == "CX-000988"
    assert ft["Issuer"]["Address"]["ZipCode"] == "78216"


def test_facturama_web_issue_uses_api3():
    pac = FacturamaWeb("user", "password", Environment.TEST)
    invoice = _sample_invoice()
    with mock.patch("requests.request") as mk:
        create_response = mock.Mock()
        create_response.ok = True
        create_response.content = b'{"Id":"web123"}'
        create_response.headers = {"Content-Type": "application/json"}
        create_response.json = mock.Mock(return_value={"Id": "web123"})

        xml_response = mock.Mock()
        xml_response.ok = True
        xml_response.content = b'{"Content":"PD94bWwgdmVyc2lvbj0iMS4wIj8+PGNmZGk+dGVzdDwvY2ZkaT4="}'
        xml_response.headers = {"Content-Type": "application/json"}
        xml_response.json = mock.Mock(
            return_value={"Content": "PD94bWwgdmVyc2lvbj0iMS4wIj8+PGNmZGk+dGVzdDwvY2ZkaT4="}
        )
        mk.side_effect = [create_response, xml_response]

        res = pac.issue(cfdi=invoice, accept=Accept.XML)
        assert res.document_id == "web123"
        assert mk.call_args_list[0].kwargs["url"].endswith("api/3/cfdis")
        assert "issued/" in mk.call_args_list[1].kwargs["url"]
        assert "issuedLite" not in mk.call_args_list[1].kwargs["url"]


def test_facturama_web_csd_not_supported():
    pac = FacturamaWeb("user", "password", Environment.TEST)
    try:
        pac.upload_csd("XIQB891116QE4", b"CER", b"KEY", "secret")
        assert False, "expected NotImplementedError"
    except NotImplementedError as exc:
        assert "FacturamaWeb" in str(exc) or "fiscal profile" in str(exc)


def test_facturama_send_email():
    pac = Facturama("user", "password", Environment.TEST)
    with mock.patch("requests.request") as mk:
        mk.return_value.ok = True
        mk.return_value.content = b'{"success":true}'
        mk.return_value.headers = {"Content-Type": "application/json"}
        mk.return_value.json = mock.Mock(return_value={"success": True})
        pac.send_email("abc123", "test@example.com")
        assert mk.call_args.kwargs["params"]["cfdiId"] == "abc123"
        assert mk.call_args.kwargs["params"]["email"] == "test@example.com"
        assert mk.call_args.kwargs["params"]["cfdiType"] == "issuedLite"


def test_facturama_cancel_by_uuid():
    pac = Facturama("user", "password", Environment.TEST)
    from satcfdi.cfdi import CFDI

    cfdi = CFDI(
        {
            "Emisor": {"Rfc": "XIQB891116QE4"},
            "Complemento": {
                "TimbreFiscalDigital": {
                    "UUID": "6D7434A6-E3F2-47AD-9E4C-08849946AFA0"
                }
            },
        }
    )

    with mock.patch("requests.request") as mk:
        list_response = mock.Mock()
        list_response.ok = True
        list_response.content = b"[]"
        list_response.headers = {"Content-Type": "application/json"}
        list_response.json = mock.Mock(
            return_value=[
                {
                    "Id": "abc123",
                    "Uuid": "6D7434A6-E3F2-47AD-9E4C-08849946AFA0",
                }
            ]
        )

        cancel_response = mock.Mock()
        cancel_response.ok = True
        cancel_response.content = b'{"Status":"canceled"}'
        cancel_response.headers = {"Content-Type": "application/json"}
        cancel_response.json = mock.Mock(return_value={"Status": "canceled"})

        mk.side_effect = [list_response, cancel_response]

        ack = pac.cancel(
            cfdi=cfdi,
            reason=CancelReason.NO_SE_LLEVO_A_CABO_LA_OPERACION,
        )
        assert ack.code == "canceled"
        assert mk.call_args_list[0].kwargs["params"]["keyword"] == (
            "6D7434A6-E3F2-47AD-9E4C-08849946AFA0"
        )
        assert mk.call_args_list[1].kwargs["url"].endswith("api-lite/cfdis/abc123")
        assert mk.call_args_list[1].kwargs["params"]["motive"] == "03"
