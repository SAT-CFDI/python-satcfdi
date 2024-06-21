# -*- coding: utf-8 -*-
import base64
from typing import Literal

from OpenSSL import crypto
from OpenSSL.crypto import X509
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import Encoding, pkcs12, PrivateFormat, BestAvailableEncryption, NoEncryption, PublicFormat, load_der_private_key

from .certificate import Certificate
from ..exceptions import CFDIError


class Signer(Certificate):
    def __init__(self, certificate: X509, key: rsa.RSAPrivateKey, check=True):
        super().__init__(certificate)
        self.key = key

        if check:
            res = _compare_public_keys(self.key.public_key(), self.public_key())
            if not res:
                raise CFDIError("Private Key does not match certificate")

    @classmethod
    def load(cls, certificate: bytes, key: bytes, password: str | bytes = None, check=True) -> 'Signer':
        if isinstance(password, str):
            password = password.encode()

        return cls(
            # certificate=x509.load_der_x509_certificate(certificate),
            certificate=crypto.load_certificate(crypto.FILETYPE_ASN1, certificate),
            key=load_der_private_key(
                data=key,
                password=password
            ),
            check=check
        )

    @classmethod
    def load_pkcs12(cls, data: bytes, password: str | bytes = None) -> 'Signer':
        if isinstance(password, str):
            password = password.encode()

        key, certificate, _ = pkcs12.load_key_and_certificates(data=data, password=password)
        if certificate is None:
            raise CFDIError("Certificate is missing")

        return cls(
            certificate=crypto.X509.from_cryptography(certificate),
            key=key,
            check=False  # pcks12 allready checks
        )

    def _sign(self, data, algorithm) -> str:
        signature = self.key.sign(
            data=data,
            padding=padding.PKCS1v15(),
            algorithm=algorithm
        )

        return base64.b64encode(
            signature
        ).decode()

    def sign_sha1(self, data) -> str:
        return self._sign(
            data=data,
            algorithm=hashes.SHA1()
        )

    def sign_sha256(self, data) -> str:
        return self._sign(
            data=data,
            algorithm=hashes.SHA256()
        )

    def key_bytes(
        self, password: str | bytes = None, encoding: Encoding = Encoding.DER
    ) -> bytes:
        """Returns the private key in bytes
        Args:
            password (str | bytes, optional): The password to decrypt the private key. Defaults to None.
            encoding (cryptography.hazmat.primitives.serialization.Encoding, optional): The encoding format of the private key. Defaults to "DER".
        Returns:
            bytes: The private key in bytes
        """
        if isinstance(password, str):
            password = password.encode()

        return self.key.private_bytes(
            encoding=encoding,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=(
                BestAvailableEncryption(password) if password else NoEncryption()
            ),
        )

    def pcks12_bytes(self, password: str | bytes = None) -> bytes:
        if isinstance(password, str):
            password = password.encode()

        return pkcs12.serialize_key_and_certificates(
            name=self.rfc.encode(),
            key=self.key,
            cert=self.certificate.to_cryptography(),
            cas=None,
            encryption_algorithm=BestAvailableEncryption(password) if password else NoEncryption()
        )

    def decrypt(self, data: bytes):
        return self.key.decrypt(
            ciphertext=data,
            padding=padding.PKCS1v15()
        )


def _compare_public_keys(public_key_a, public_key_b):
    def key_bytes(k):
        return k.public_bytes(
            encoding=Encoding.DER,
            format=PublicFormat.SubjectPublicKeyInfo
        )

    return key_bytes(public_key_a) == key_bytes(public_key_b)
