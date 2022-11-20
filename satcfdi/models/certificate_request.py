from OpenSSL.crypto import FILETYPE_ASN1
from cryptography import x509
from OpenSSL import crypto


class CertificateSigningRequest:
    def __init__(self, request: x509.CertificateSigningRequest):
        self.request = request

    @classmethod
    def load(cls, request: bytes) -> 'CertificateSigningRequest':
        return cls(x509.load_der_x509_csr(request))

    @classmethod
    def load2(cls, request: bytes):
        return crypto.load_certificate_request(FILETYPE_ASN1, request)
