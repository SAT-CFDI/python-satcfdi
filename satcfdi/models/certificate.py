# -*- coding: utf-8 -*-
import base64
from enum import Enum, auto
from typing import Literal

from OpenSSL import crypto
from OpenSSL.crypto import X509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import PublicFormat, Encoding
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from .curp import CURP
from .rfc import RFC, RFCType
from ..exceptions import CFDIError

REGIMEN_SOCIETARIOS = {
    'AC': 'AC - Asociación civil',
    'S DE CV': 'Sociedad de capital variable',
    'S DE RL DE CV': 'Sociedad de responsabilidad limitada de capital variable',
    'S DE RL': 'Sociedad de responsabilidad limitada',
    'S EN C DE CV': 'Sociedad en comandita simple de capital variable',
    'S EN C POR A DE CV': 'Sociedad en comandita por acciones de capital variable',
    'S EN C POR A': 'Sociedad en comandita por acciones',
    'S EN C': 'Sociedad en comandita simple',
    'S EN NC DE CV': 'Sociedad en nombre colectivo de capital variable',
    'S EN NC': 'Sociedad en nombre colectivo',
    'SA DE CV': 'Sociedad anónima de capital variable',
    'SA': 'Sociedad anónima',
    'SAB DE CV': 'Sociedad anómina bursátil de capital variable',
    'SAB': 'Sociedad anómina bursátil',
    'SAPI DE CV': 'Sociedad anónima promotora de inversión de capital variable',
    'SAPI': 'Sociedad anónima promotora de inversión',
    'SAPIB': 'Sociedad anónima promotora de inversión bursátil',
    'SAS DE CV': 'Sociedad por acciones simplificada de capital variable',
    'SAS': 'Sociedad por acciones simplificada',
    'SC DE CV': 'Sociedad civil de capital variable',
    'SC': 'Sociedad civil',
}


class CertificateType(Enum):
    Fiel = auto()
    CSD = auto()


class Certificate:
    def __init__(self, certificate: X509):
        self.certificate = certificate

    @classmethod
    def load_certificate(cls, certificate: bytes, encoding: Encoding = Encoding.DER) -> 'Certificate':
        if encoding == Encoding.PEM:
            t = crypto.FILETYPE_PEM
        elif encoding == Encoding.DER:
            t = crypto.FILETYPE_ASN1
        else:
            raise CFDIError(f"Invalid encoding {encoding}")
        return cls(crypto.load_certificate(t, certificate))

    def fingerprint(self, algorithm=hashes.SHA1()) -> bytes:
        return self.certificate.to_cryptography().fingerprint(algorithm=algorithm)

    def certificate_bytes(self, encoding: Encoding = Encoding.DER) -> bytes:
        return self.certificate.to_cryptography().public_bytes(
            encoding=encoding
        )

    def certificate_base64(self) -> str:
        """Returns the certificate in base64 encoding
        Returns:
            str: The certificate in base64 encoding
        """
        cert = self.certificate_bytes()
        return base64.b64encode(cert).decode()

    def issuer(self) -> str:
        d = self.certificate.get_issuer().get_components()
        return ','.join(f'{k.decode()}={v.decode()}' for k, v in reversed(d))

    def subject(self) -> str:
        d = self.certificate.get_subject().get_components()
        return ','.join(f'{k.decode()}={v.decode()}' for k, v in reversed(d))

    @property
    def type(self):
        if self.certificate.get_extension_count() == 4:
            return CertificateType.Fiel
        if self.certificate.get_extension_count() == 2:
            return CertificateType.CSD
        return None

    @property
    def serial_number(self) -> int:
        return self.certificate.get_serial_number()

    # useful data
    @property
    def legal_name(self) -> str | None:
        try:
            at = self.certificate.get_subject().O
            if self.rfc.type == RFCType.MORAL:
                for r in REGIMEN_SOCIETARIOS:
                    if at.endswith(" " + r):
                        return at[:-len(r) - 1]
            return at
        except AttributeError:
            return None

    @property
    def rfc(self) -> RFC | None:
        try:
            at = self.certificate.get_subject().x500UniqueIdentifier
            at = at.split("/")[0].strip()
            return RFC(at)
        except AttributeError:
            return None

    @property
    def rfc_representante(self) -> RFC | None:
        try:
            at = self.certificate.get_subject().x500UniqueIdentifier
            at = at.split("/")[1].strip()
            return RFC(at)
        except AttributeError:
            return None

    @property
    def curp(self) -> CURP | None:
        try:
            at = self.certificate.get_subject().serialNumber
            at = at.split("/")[0].strip()
            return CURP(at) if at else None
        except AttributeError:
            return None

    @property
    def curp_representante(self) -> CURP | None:
        try:
            at = self.certificate.get_subject().serialNumber
            at = at.split("/")[1].strip()
            return CURP(at)
        except AttributeError:
            return None

    @property
    def branch_name(self) -> str | None:
        try:
            return self.certificate.get_subject().OU
        except AttributeError:
            return None

    @property
    def rfc_pac(self) -> RFC:
        if nom_suc := self.branch_name:
            if nom_suc.startswith("PAC"):
                return RFC(nom_suc[3:15])
            if nom_suc.startswith("MEGAPAC"):
                return RFC(nom_suc[7:19])
        raise CFDIError("Certificado no es PAC")

    @property
    def email(self) -> str | None:
        try:
            return self.certificate.get_subject().emailAddress
        except AttributeError:
            return None

    @property
    def certificate_number(self) -> str:
        return f'{self.certificate.get_serial_number():x}'[1::2]

    def public_key(self) -> rsa.RSAPublicKey:
        return self.certificate.get_pubkey().to_cryptography_key()

    def public_key_bytes(self, encoding: serialization.Encoding = serialization.Encoding.DER) -> bytes:
        return self.public_key().public_bytes(
            encoding=encoding,
            format=PublicFormat.SubjectPublicKeyInfo
        )

    def _verify(self, data, signature, algorithm) -> bool:
        try:
            self.public_key().verify(
                signature=signature,
                data=data,
                padding=padding.PKCS1v15(),
                algorithm=algorithm
            )
            return True
        except InvalidSignature:
            return False

    def verify_sha1(self, data: bytes, signature: bytes) -> bool:
        return self._verify(
            data=data,
            signature=signature,
            algorithm=hashes.SHA1()
        )

    def verify_sha256(self, data: bytes, signature: bytes) -> bool:
        return self._verify(
            data=data,
            signature=signature,
            algorithm=hashes.SHA256()
        )

    def encrypt(self, data: bytes):
        return self.public_key().encrypt(
            plaintext=data,
            padding=padding.PKCS1v15()
        )
