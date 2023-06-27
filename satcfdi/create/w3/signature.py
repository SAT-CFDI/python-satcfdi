import base64
import hashlib

from lxml import etree

from .ds import SignatureValueType, KeyInfoType, CanonicalizationMethodType, SignatureMethodType, ReferenceType, TransformsType, TransformType, \
    DigestMethodType, X509DataType, X509IssuerSerialType, SignedInfo, Signature
from .. import Signer
from ...xelement import XElement


def _tobytes(element: etree.Element, exclusive=True) -> bytes:
    return etree.tostring(element, method='c14n', exclusive=exclusive)


def _digest(element: etree.Element, exclusive=True) -> str:
    element_digest = hashlib.sha1(
        _tobytes(element, exclusive)
    ).digest()
    return base64.b64encode(element_digest).decode()


def signature_c14n_sha1(signer: Signer, element: etree.Element, nsmap=None) -> XElement:
    digest = _digest(element, exclusive=False)

    signed_info = SignedInfo(
        canonicalization_method=CanonicalizationMethodType(
            algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
        ),
        signature_method=SignatureMethodType(
            algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"
        ),
        reference=ReferenceType(
            uri="",
            transforms=TransformsType(
                transform=TransformType(
                    algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"
                )
            ),
            digest_method=DigestMethodType(
                algorithm="http://www.w3.org/2000/09/xmldsig#sha1"
            ),
            digest_value=digest
        )
    )
    signed_info["_nsmap"] = nsmap

    signature = Signature(
        signed_info=signed_info,
        signature_value=SignatureValueType(
            signer.sign_sha1(
                _tobytes(signed_info.to_xml(), exclusive=False)
            )
        ),
        key_info=KeyInfoType(
            x509data=X509DataType(
                x509issuer_serial=X509IssuerSerialType(
                    x509issuer_name=signer.issuer(),
                    x509serial_number=signer.serial_number
                ),
                x509certificate=signer.certificate_base64()
            )
        )
    )
    signature["_nsmap"] = nsmap
    return signature
