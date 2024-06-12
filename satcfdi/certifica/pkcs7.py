import os
from datetime import datetime, UTC

from ..ans1e import Ans1Encoder, Numbers, Classes, to_utc_time
from ..models import Signer

current_dir = os.path.dirname(__file__)

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def create_pkcs7(data, signer: Signer, hash_algorithm):
    cert_bytes = signer.certificate_bytes()
    issuer_der = signer.certificate.get_issuer().der()
    serial = signer.certificate.get_serial_number()

    hash_object = hashes.Hash(hash_algorithm)
    hash_object.update(data)
    digest = hash_object.finalize()

    utctime = to_utc_time(datetime.now(UTC).replace(tzinfo=None))

    e = Ans1Encoder()
    with e.seq():
        e.oid("1.2.840.113549.1.9.3")
        with e.set():
            e.oid("1.2.840.113549.1.7.1")
    with e.seq():
        e.oid("1.2.840.113549.1.9.5")
        with e.set():
            e(utctime, nr=Numbers.UTCTime)
    with e.seq():
        e.oid("1.2.840.113549.1.9.4")
        with e.set():
            e(digest, nr=Numbers.OctetString)
    signed_attributes = e.output()

    e = Ans1Encoder()
    with e.set():
        e.write(signed_attributes)
    signing_data = e.output()

    signature = signer.key.sign(
        data=signing_data,
        padding=padding.PKCS1v15(),
        algorithm=hash_algorithm
    )

    e = Ans1Encoder()
    with e.seq():
        e.oid('1.2.840.113549.1.7.2')
        with e.enter(nr=0, cls=Classes.Context):
            with e.seq():
                e(1, nr=Numbers.Integer)
                with e.set():
                    with e.seq():
                        e.oid('1.3.14.3.2.26')
                        e(nr=Numbers.Null)
                with e.seq():
                    e.oid("1.2.840.113549.1.7.1")
                    with e.enter(nr=0, cls=Classes.Context):
                        e(data, nr=Numbers.OctetString)
                with e.enter(nr=0, cls=Classes.Context):
                    e.write(cert_bytes)
                with e.set():
                    with e.seq():
                        e(1, nr=Numbers.Integer)
                        with e.seq():
                            e.write(issuer_der)
                            e(serial, nr=Numbers.Integer)
                        with e.seq():
                            e.oid('1.3.14.3.2.26')
                            e(nr=Numbers.Null)
                        with e.enter(nr=0, cls=Classes.Context):
                            e.write(signed_attributes)
                        with e.seq():
                            e.oid('1.2.840.113549.1.1.1')
                            e(nr=Numbers.Null)
                        e(signature, nr=Numbers.OctetString)

    return e.output()
