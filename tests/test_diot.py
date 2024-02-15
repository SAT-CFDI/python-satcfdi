import os
from binascii import unhexlify
from datetime import datetime, date
from io import BytesIO
from unittest import mock
from zipfile import ZipInfo

from satcfdi import render
from satcfdi.diot.code import Periodo, TipoOperacion, TipoTercero, Pais
from satcfdi.diot import DatosIdentificacion, DatosComplementaria, ProveedorTercero, DIOT
from tests.utils import get_signer, verify_result

current_dir = os.path.dirname(__file__)
module = 'satcfdi'


def test_encrypt_signature():
    signer = get_signer('cacx7605101p8')
    key = b'\x9e@@hL\xcd\xf2\x9eR\xe6JC\xc8\xba\x8a\xf1C\xec\rE*\x16 4'

    # from DIOT project try 1
    sig = "1a7f1f4d8ef5091a4dc797a80327756110878b08555d84761475e444ad4effe855b44aafb7c47a3627d21f34d40a59fe103d53eda40721d8196d745ce39a6bce97e064a3725840dcf340f7c9ad84f8ab891198f25bf81802f0e8363d4ce02c78268ce75bda284d0771bde7cdf6b6c76adbc607823d54edfa8f9e5385ee8ffa406e14811738781678faff32d0d6b9c843e38ba7a29b8b2414930a200d0512ee69ca693ba341b9462476fbaa085d56178915c03d9bc61ae37d8609fe75c87659e687bd0ca56bcf5a52e2b74fbb67bcd1761ee8360cddb82470a2106a30a9299a7415ccc12a5f37d5b5732e84fd21aba7b3caba49eb913925c9869ca643df1dba8c"
    sig = unhexlify(sig)
    res = signer.decrypt(sig)
    assert res == key

    # from DIOT project try 2
    sig = "768cce9ca1955dbe4b9e768413e37d23f0b1c3e2d3d313278053f2c66aae14d7ecaacdf4a942dff564489156dfb805a3713b7ad48f230762acb493840a1236e445844ba41ca299d715a63dca227f86679322a4864aa30a28b9f43200c83748816900e9b06f224d3ba3bae284ec9916c752da12f0bb189ef1eb64f71bae6ced280f3009798002dcae9129c5105efef1179d93a434c8ebd6144a0f5721deea7c864ed273b8410e2dbdc1d0e684f49c37d58a3311a673ff347f59115ecdf6ba5d05b5e2d2caa45f1e0d2a842057467ed8069de8f79e6abe449c7f1a3222d873d859ad6e6f9608342e1dc709c8b50cb67a07016c75230495938b15e174e0277ac9f1"
    sig = unhexlify(sig)
    res = signer.decrypt(sig)
    assert res == key

    enc_key = signer.encrypt(data=key)
    dec_key = signer.decrypt(data=enc_key)

    assert dec_key == key


def test_create_filename():
    rfc = 'XIQB891116QE4'
    with mock.patch(f'{module}.diot.datetime') as m:
        m.now = mock.Mock(return_value=datetime(2022, 11, 8, 11, 40))
        diot = DIOT(
            datos_identificacion=DatosIdentificacion(
                rfc=rfc,
                ejercicio=2022,
            ),
            periodo=Periodo.OCTUBRE,
            proveedores=[]
        )
        assert diot.filename() == 'XIQB891116QE40DOTAAM1MCMB811401'

    with mock.patch(f'{module}.diot.datetime') as m:
        p = ProveedorTercero(
            tipo_tercero=TipoTercero.PROVEEDOR_GLOBAL,
            tipo_operacion=TipoOperacion.OTROS
        )
        m.now = mock.Mock(return_value=datetime(2022, 11, 8, 13, 20))
        diot = DIOT(
            datos_identificacion=DatosIdentificacion(
                rfc=rfc,
                ejercicio=2022,
            ),
            periodo=Periodo.OCTUBRE,
            proveedores=[p for _ in range(40001)]
        )
        assert diot.filename() == 'XIQB891116QE40DOTAAM1MCMB813202'

    rfc = "OÑO120726RX3"
    with mock.patch(f'{module}.diot.datetime') as m:
        m.now = mock.Mock(return_value=datetime(2022, 11, 8, 17, 18))
        diot = DIOT(
            datos_identificacion=DatosIdentificacion(
                rfc=rfc,
                ejercicio=2022,
            ),
            periodo=Periodo.OCTUBRE,
            proveedores=[]
        )
        assert diot.filename() == '_OÑO120726RX30DOTAAM1MCMB817181'


xiqb891116qe4_issuer = DatosIdentificacion(
    rfc='xiqb891116qe4',
    ejercicio=2022,
    curp='xiqb891116mgrmzr05',
    nombre='BERENICE',
    apellido_paterno='XIMO',
    apellido_materno='QUEZADA'
)


def test_create_declaracion_diot():
    text_file = "XIQB891116QE40DOTAAM1MCMB811401"
    diot = DIOT(
        datos_identificacion=xiqb891116qe4_issuer,
        periodo=Periodo.OCTUBRE
    )
    # Verify TXT
    original_txt_data = open(os.path.join(current_dir, 'diot', f'{text_file}.txt'), 'rb').read()
    with BytesIO() as b:
        diot.plain_write(target=b)
        assert original_txt_data == b.getvalue()

    # Verify FILENAME
    with mock.patch(f'{module}.diot.datetime') as m:
        m.now = mock.Mock(return_value=datetime(2022, 11, 8, 11, 40))
        tmp_filename = diot.filename()
        assert tmp_filename == text_file

    # Verify ZIP
    def zi(filename):
        return ZipInfo(
            filename=filename,
            date_time=(2022, 11, 8, 11, 41, 8)  # time.localtime(time.time())[:6]
        )

    with mock.patch(f'{module}.zip.ZipInfo', zi) as m:
        my_zip = diot._zip_bytes(tmp_filename)

        original_zip_data = open(os.path.join(current_dir, 'diot', f'{text_file}.zpi'), 'rb').read()
        assert my_zip == original_zip_data

        # Verify DEC
        def encrypt(_, data):
            return b'HB\x9cWQ\xbf\x975i\xfd\xcbH\x1c\xacD\x00pp\'%\xf3"\xa7\x802O\xcagG\x8c6\x07\xa7n9\xe6\x10*P\xd1\x9d\xf8,\x7f\x84T%\x9eR\xea\xab\x00\xeeX7\x00\x87\xfe\xb5\xf7\x9d\xc4\xa2\xbcu\xa4\x13SX\xee\xe6\xfeSv\x16\xcc\xb2y\xbd4nD\xb0\xbd\x10^y\x9f/PZ\x9b\xd1\xc0\x98\x84\xb6\x90\xc1"\xe0\xb9\x83y\x92\x85\x832\x98C\xd0\xe8\x81P\x0b\xde\x14\xaa\x19_\x0c\xf0\xf2\xec\xdc\x9f\x06i'

        def rand(dig):
            if dig == 8:
                return b'p*A\xe4\xcb\x88\xa3\x8f'
            if dig == 24:
                return b'\x9e@@hL\xcd\xf2\x9eR\xe6JC\xc8\xba\x8a\xf1C\xec\rE*\x16 4'

        with mock.patch(f'{module}.models.Certificate.encrypt', encrypt), mock.patch('os.urandom', rand):
            dec_data = diot._encrypted_bytes(tmp_filename)
            assert dec_data == open(os.path.join(current_dir, 'diot', f'{text_file}.dec'), 'rb').read()

            with mock.patch(f'{module}.diot.datetime') as m:
                m.now = mock.Mock(return_value=datetime(2022, 11, 8, 11, 40))

                res_filename = diot.generate_package(
                    os.path.join(current_dir, 'test_diot')
                )
                assert dec_data == open(os.path.join(current_dir, 'test_diot', f'{text_file}.dec'), 'rb').read()
                assert os.path.basename(res_filename) == f'{text_file}.dec'


def test_create_declaracion_diot_complementary():
    diot_file = "XIQB891116QE40DOTAAM1MCMB816201"
    diot = DIOT(
        datos_identificacion=xiqb891116qe4_issuer,
        periodo=Periodo.MARZO_ABRIL,
        complementaria=DatosComplementaria(
            folio_anterior="6565",
            fecha_presentacion_anterior=date(2022, 11, 7)
        )
    )
    reference_data = open(os.path.join(current_dir, 'diot', f'{diot_file}.txt'), 'rb').read()
    assert reference_data == diot.plain_bytes()


def test_create_declaracion_diot_complementary2():
    diot_file = "XIQB891116QE40DOTAAM1MCMB901581"
    diot = DIOT(
        datos_identificacion=xiqb891116qe4_issuer,
        periodo=Periodo.ENERO,
        complementaria=DatosComplementaria(
            folio_anterior="4567",
            fecha_presentacion_anterior=date(2022, 2, 13)
        )
    )
    reference_data = open(os.path.join(current_dir, 'diot', f'{diot_file}.txt'), 'rb').read()
    assert reference_data == diot.plain_bytes()


def test_create_declaracion_diot_trimestral():
    diot_file = "XIQB891116QE40DOTAAM1MCMB816531"
    diot = DIOT(
        datos_identificacion=xiqb891116qe4_issuer,
        periodo=Periodo.JULIO_SEPTIEMBRE
    )
    reference_data = open(os.path.join(current_dir, 'diot', f'{diot_file}.txt'), 'rb').read()
    assert reference_data == diot.plain_bytes()


ono120726rx3_issue = DatosIdentificacion(
    rfc="OÑO120726RX3",
    razon_social="ORGANICOS ÑAVEZ OSORIO S.A DE C.V",
    ejercicio=2022,
)


def test_create_declaracion_diot_moral():
    diot_file = "_OÑO120726RX30DOTAAM1MCMB817181"
    diot = DIOT(
        datos_identificacion=ono120726rx3_issue,
        periodo=Periodo.MAYO_AGOSTO
    )
    reference_data = open(os.path.join(current_dir, 'diot', f'{diot_file}.txt'), 'rb').read()
    assert reference_data == diot.plain_bytes()


def test_create_declaracion_diot_moral_da():
    diot_file = "_OÑO120726RX30DOTAAM1MCMB820181"
    diot = DIOT(
        datos_identificacion=ono120726rx3_issue,
        periodo=Periodo.OCTUBRE,
        proveedores=[
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_NACIONAL,
                tipo_operacion=TipoOperacion.PRESTACION_DE_SERVICIOS_PROFESIONALES,
                rfc="LIÑI920228KS8",
                iva16=52000,
                iva16_na=48521,
                iva_rfn=42000,
                iva_rfn_na=32000,
                iva0=31000,
                iva_exento=21000,
                retenido=11000,
                devoluciones=10000
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_NACIONAL,
                tipo_operacion=TipoOperacion.ARRENDAMIENTO_DE_INMUEBLES,
                rfc="IVD920810GU2",
                iva16=987,
                iva16_na=876,
                iva_rfn=765,
                iva_rfn_na=654,
                iva0=324,
                iva_exento=251,
                retenido=125,
                devoluciones=444
            ),
        ]
    )
    reference_data = open(os.path.join(current_dir, 'diot', f'{diot_file}.txt'), 'rb').read()
    assert reference_data == diot.plain_bytes()


def test_create_declaracion_diot_moral_full():
    diot_file = "_OÑO120726RX30DOTAAL1LCMB823021"
    diot = DIOT(
        datos_identificacion=DatosIdentificacion(
            rfc="OÑO120726RX3",
            razon_social="ORGANICOS ÑAVEZ OSORIO S.A DE C.V",
            ejercicio=2021,
        ),
        periodo=Periodo.JULIO_SEPTIEMBRE,
        proveedores=[
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_EXTRANJERO,
                tipo_operacion=TipoOperacion.OTROS,
                id_fiscal="1254TAXID",
                nombre_extranjero="NOMBREEXTRANJERO",
                pais=Pais.ANTIGUA_Y_BERMUDA,
                nacionalidad="BERMUDO",
                iva16=456,
                iva16_na=752,
                iva_rfn=782,
                iva_rfn_na=456,
                iva_import16=123,
                iva_import16_na=475,
                iva_import_exento=7575,
                iva0=45213,
                iva_exento=1247,
                retenido=235,
                devoluciones=786
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_GLOBAL,
                tipo_operacion=TipoOperacion.ARRENDAMIENTO_DE_INMUEBLES,
                iva16=9874,
                iva16_na=8521,
                iva_rfn=7632,
                iva_rfn_na=6541,
                iva_import16=5241,
                iva_import16_na=4123,
                iva_import_exento=3562,
                iva0=2415,
                iva_exento=1235,
                retenido=985,
                devoluciones=874
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_NACIONAL,
                tipo_operacion=TipoOperacion.OTROS,
                rfc="L&O950913MSA",
                iva16=96208900,
                iva16_na=85100,
                iva_rfn=74300,
                iva_rfn_na=67600,
                iva0=58900,
                iva_exento=47700,
                retenido=36400,
                devoluciones=24864
            ),
        ]
    )
    reference_data = open(os.path.join(current_dir, 'diot', f'{diot_file}.txt'), 'rb').read()
    assert reference_data == diot.plain_bytes()


def verify_invoice(invoice, path):
    verify = verify_result(data=render.html_str(invoice), filename=f"{path}.html")
    assert verify


def test_create_declaracion_diot_moral_full_2():
    diot_file = "_OÑO120726RX30DOTAAL1LCMB901151"
    diot = DIOT(
        datos_identificacion=DatosIdentificacion(
            rfc="OÑO120726RX3",
            razon_social="ORGANICOS ÑAVEZ OSORIO S.A DE C.V",
            ejercicio=2021,
        ),
        periodo=Periodo.JULIO_SEPTIEMBRE,
        proveedores=[
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_EXTRANJERO,
                tipo_operacion=TipoOperacion.OTROS,
                id_fiscal="1254TAXID",
                nombre_extranjero="NOMBREEXTRANJERO",
                pais=Pais.ANTIGUA_Y_BERMUDA,
                nacionalidad="BERMUDO",
                iva16=456,
                iva16_na=752,
                iva_rfn=782,
                iva_rfn_na=456,
                iva_import16=123,
                iva_import16_na=475,
                iva_import_exento=7575,
                iva0=45213,
                iva_exento=1247,
                retenido=235,
                devoluciones=786
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_GLOBAL,
                tipo_operacion=TipoOperacion.ARRENDAMIENTO_DE_INMUEBLES,
                iva16=9874,
                iva16_na=8521,
                iva_rfn=7632,
                iva_rfn_na=6541,
                iva_import16=5241,
                iva_import16_na=4123,
                iva_import_exento=3562,
                iva0=2415,
                iva_exento=1235,
                retenido=985,
                devoluciones=874
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_NACIONAL,
                tipo_operacion=TipoOperacion.OTROS,
                rfc="L&O950913MSA",
                iva16=96208900,
                iva16_na=85100,
                iva_rfn=74300,
                iva_rfn_na=67600,
                iva0=58900,
                iva_exento=47700,
                retenido=36400,
                devoluciones=24864
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_GLOBAL,
                tipo_operacion=TipoOperacion.PRESTACION_DE_SERVICIOS_PROFESIONALES,
                iva16=77757987856,
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_NACIONAL,
                tipo_operacion=TipoOperacion.PRESTACION_DE_SERVICIOS_PROFESIONALES,
                rfc="IXS7607092R5",
                iva16_na=500,
                iva_rfn=0
            )
        ]
    )
    reference_data = open(os.path.join(current_dir, 'diot', f'{diot_file}.txt'), 'rb').read()
    assert reference_data == diot.plain_bytes()

    verify_invoice(diot, 'test_create_declaracion_diot_moral_full_2')


def test_create_declaracion_diot_moral_full_2_comp():
    diot = DIOT(
        datos_identificacion=DatosIdentificacion(
            rfc="OÑO120726RX3",
            razon_social="ORGANICOS ÑAVEZ OSORIO S.A DE C.V",
            ejercicio=2021,
        ),
        periodo=Periodo.JULIO_SEPTIEMBRE,
        complementaria=DatosComplementaria(
            folio_anterior="12313",
            fecha_presentacion_anterior=date(2021, 5, 10)
        ),
        proveedores=[
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_EXTRANJERO,
                tipo_operacion=TipoOperacion.OTROS,
                id_fiscal="1254TAXID",
                nombre_extranjero="NOMBREEXTRANJERO",
                pais=Pais.ANTIGUA_Y_BERMUDA,
                nacionalidad="BERMUDO",
                iva16=456,
                iva16_na=752,
                iva_rfn=782,
                iva_rfn_na=456,
                iva_import16=123,
                iva_import16_na=475,
                iva_import_exento=7575,
                iva0=45213,
                iva_exento=1247,
                retenido=235,
                devoluciones=786
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_GLOBAL,
                tipo_operacion=TipoOperacion.ARRENDAMIENTO_DE_INMUEBLES,
                iva16=9874,
                iva16_na=8521,
                iva_rfn=7632,
                iva_rfn_na=6541,
                iva_import16=5241,
                iva_import16_na=4123,
                iva_import_exento=3562,
                iva0=2415,
                iva_exento=1235,
                retenido=985,
                devoluciones=874
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_NACIONAL,
                tipo_operacion=TipoOperacion.OTROS,
                rfc="L&O950913MSA",
                iva16=96208900,
                iva16_na=85100,
                iva_rfn=74300,
                iva_rfn_na=67600,
                iva0=58900,
                iva_exento=47700,
                retenido=36400,
                devoluciones=24864
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_GLOBAL,
                tipo_operacion=TipoOperacion.PRESTACION_DE_SERVICIOS_PROFESIONALES,
                iva16=77757987856,
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_NACIONAL,
                tipo_operacion=TipoOperacion.PRESTACION_DE_SERVICIOS_PROFESIONALES,
                rfc="IXS7607092R5",
                iva16_na=500,
                iva_rfn=0
            )
        ]
    )

    verify_invoice(diot, 'test_create_declaracion_diot_moral_full_2_comp')
