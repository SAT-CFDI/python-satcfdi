import os
import zipfile
from collections.abc import Iterable
from datetime import datetime

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from pytz import utc

current_dir = os.path.dirname(__file__)


class CertificateStore:
    def __init__(self, trusted_certificates: Iterable):
        self._trusted_certificates = {
            cert.subject.public_bytes(): cert for cert in trusted_certificates
        }

    def issuer_certificate(self, cert):
        return self._trusted_certificates[cert.issuer.public_bytes()]

    def verify_certificate(self, issued_cert, at: datetime):
        """Verifies issued_cert.

        Args:
            issued_cert: The issued certificate.

        Returns:
            True if certificate was issued by a trusted certificate
            :param issued_cert: issued certificate to validate
            :param at: date at witch to do the validation
        """
        if at.tzinfo:
            at = at.astimezone(tz=utc).replace(tzinfo=None)

        def validate_date(cert):
            if not cert.not_valid_before <= at <= cert.not_valid_after:
                raise ValueError("Date Not Valid")

        try:
            validate_date(issued_cert)
            signing_cert = self.issuer_certificate(issued_cert)
            validate_date(signing_cert)

            signing_cert.public_key().verify(
                signature=issued_cert.signature,
                data=issued_cert.tbs_certificate_bytes,
                padding=padding.PKCS1v15(),
                algorithm=issued_cert.signature_hash_algorithm
            )

            # Assume the parent certificates have been already validated, only checking dates
            while True:
                parent_cert = self.issuer_certificate(signing_cert)
                if parent_cert == signing_cert:
                    return True
                validate_date(parent_cert)
                signing_cert = parent_cert

        except (IndexError, InvalidSignature, ValueError) as ex:
            return False

    @classmethod
    def create(cls, certs_zip):
        """
        Creates a Certificate Store from the certificates in a zip file
        :param certs_zip:
        :return: CertificateStore
        """
        with zipfile.ZipFile(certs_zip, "r") as zf:
            return cls(
                trusted_certificates=
                (x509.load_der_x509_certificate(zf.read(fileinfo)) for fileinfo in zf.infolist())
            )
