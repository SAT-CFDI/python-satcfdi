from cryptography import x509


class CertificateSigningRequest:
    def __init__(self, request: x509.CertificateSigningRequest):
        self.request = request

    @classmethod
    def load(cls, request: bytes) -> 'CertificateSigningRequest':
        return cls(x509.load_der_x509_csr(request))
