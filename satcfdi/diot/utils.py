import os
from io import BytesIO

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from ..models import RFC, RFCType, Code

BUFFER_SIZE = 65536


def encrypt_triple_des(data: BytesIO):
    pl = 8 - data.tell() % 8
    data.write(bytes([pl for _ in range(pl)]))
    data.seek(0)

    key = os.urandom(24)
    iv = os.urandom(8)

    cipher = Cipher(
        algorithm=algorithms.TripleDES(key),
        mode=modes.CBC(iv)
    )
    encryptor = cipher.encryptor()

    out = BytesIO()
    while True:
        buf = data.read(BUFFER_SIZE)
        if buf:
            out.write(encryptor.update(buf))
        else:
            out.write(encryptor.finalize())
            break

    return "1.2.840.113549.3.7", key, iv, out


class DIOTWriter:
    def __init__(self, stream):
        self.io = stream

    def __call__(self, clave, b, c, valor):
        self.io.write(
            f"{clave}|{b}|{c}|{valor}|\r\n".encode('windows-1252')
        )

    def end(self):
        self.io.write(b"EOF\r\n")


def _format_rfc(rfc: RFC):
    if rfc.type == RFCType.FISICA:
        return str(rfc)
    return " " + rfc


def period_code(period: str):
    period = int(period)
    if period <= 12:
        return "1"
    if period <= 18:
        return "2"
    if period <= 22:
        return "3"
    if period <= 25:
        return "4"
    return "5"


def catalog_code(catalog, value):
    if value is None:
        return None
    return Code(value, catalog[value])
