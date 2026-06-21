from cryptography import x509

# Characters allowed in an ASN.1 PrintableString (X.680).
_PRINTABLE_STRING_CHARS = set(
    b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 '()+,-./:=?"
)
_TAG_PRINTABLE_STRING = 0x13
_TAG_UTF8_STRING = 0x0C
_TAG_CONSTRUCTED = 0x20


def _encode_length(length: int) -> bytes:
    if length < 0x80:
        return bytes([length])
    encoded = length.to_bytes((length.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(encoded)]) + encoded


def _sanitize_der(buffer: bytes, start: int, end: int) -> bytes:
    """Re-encode a DER region, converting malformed PrintableStrings.

    The SAT issues certificate requests where fields such as the RFC are tagged
    as PrintableString but contain characters that are not valid in that string
    type (e.g. ``Ñ`` or ``&``). Strict ASN.1 parsers reject these, so the
    offending values are re-encoded as latin-1 decoded UTF8Strings.
    """
    out = bytearray()
    i = start
    while i < end:
        tag = buffer[i]
        j = i + 1
        length = buffer[j]
        j += 1
        if length & 0x80:
            num_bytes = length & 0x7F
            length = int.from_bytes(buffer[j:j + num_bytes], "big")
            j += num_bytes
        content_start = j
        content_end = j + length

        if tag & _TAG_CONSTRUCTED:
            inner = _sanitize_der(buffer, content_start, content_end)
            out += bytes([tag]) + _encode_length(len(inner)) + inner
        else:
            data = buffer[content_start:content_end]
            if tag == _TAG_PRINTABLE_STRING and any(b not in _PRINTABLE_STRING_CHARS for b in data):
                data = bytes(data).decode("latin-1").encode("utf-8")
                tag = _TAG_UTF8_STRING
            out += bytes([tag]) + _encode_length(len(data)) + bytes(data)

        i = content_end
    return bytes(out)


class CertificateSigningRequest:
    def __init__(self, request: x509.CertificateSigningRequest):
        self.request = request

    @classmethod
    def load(cls, request: bytes) -> 'CertificateSigningRequest':
        try:
            return cls(x509.load_der_x509_csr(request))
        except ValueError:
            sanitized = _sanitize_der(request, 0, len(request))
            return cls(x509.load_der_x509_csr(sanitized))
