from datetime import datetime

from satcfdi.create.cancela import cancelacion, cancelacionretencion
from tests.utils import verify_result, get_signer, XElementPrettyPrinter


def verify_invoice(invoice, path):
    pp = XElementPrettyPrinter()
    verify = verify_result(data=pp.pformat(invoice), filename=f"{path}.py")
    assert verify

    verify = verify_result(data=invoice.xml_bytes(pretty_print=True), filename=f"{path}.xml")
    assert verify


def test_create_cancelacion():
    signer = get_signer('emisor2021')

    can = cancelacion.Cancelacion(
        emisor=signer,
        fecha=datetime.fromisoformat("2022-01-29T15:45:12"),
        folios=[
            cancelacion.Folio(
                uuid="E3BA5811-FD07-4B9C-84B4-B146D7560575",
                motivo="01",
                folio_sustitucion="20D816A0-BA64-4DF4-BE87-AA55E62F992F"
            ),
            cancelacion.Folio(
                uuid="29880559-5057-4871-9572-A222FD10BD97",
                motivo="02",
            )
        ]
    )

    verify_invoice(can, "cancelacion")


def test_create_cancelacion_retencion():
    signer = get_signer('emisor2021')

    can = cancelacionretencion.Cancelacion(
        emisor=signer,
        fecha=datetime.fromisoformat("2022-01-29T15:45:12"),
        folios=[
            cancelacionretencion.Folio(
                uuid="E3BA5811-FD07-4B9C-84B4-B146D7560575",
                motivo="01",
                folio_sustitucion="20D816A0-BA64-4DF4-BE87-AA55E62F992F"
            ),
            cancelacionretencion.Folio(
                uuid="29880559-5057-4871-9572-A222FD10BD97",
                motivo="02",
            )
        ]
    )

    verify_invoice(can, "cancelacionretencion")
