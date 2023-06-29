import io
from enum import IntEnum

__all__ = [
    'Numbers',
    'Types',
    'Classes',
    'Ans1Encoder'
]


class Numbers(IntEnum):
    Boolean = 1
    Integer = 2
    BitString = 3
    OctetString = 4
    Null = 5
    ObjectIdentifier = 6
    ObjectDescriptor = 7
    InstanceOf = 8
    Real = 9
    Enumerated = 10
    EmbeddedPdv = 11
    UTF8String = 12
    RelativeOid = 13
    Sequence = 16
    Set = 17
    NumericString = 18
    PrintableString = 19
    T61String = 20
    IA5String = 22
    UTCTime = 23
    GeneralizedTime = 24
    GraphicString = 25
    VisibleString = 26
    GeneralString = 27
    UniversalString = 28
    CharacterString = 29
    BMPString = 30


class Types(IntEnum):
    Primitive = 0
    Constructed = 32


class Classes(IntEnum):
    Universal = 0
    Application = 64
    Context = 128
    Private = 192


class BytesChain(list):
    __slots__ = ['length', 'parent']

    def __init__(self, parent=None):
        super().__init__()
        self.length = 0
        self.parent = parent

    def append(self, data):
        super().append(data)
        self.length += len(data)

    def write(self, target):
        for v in self:
            if isinstance(v, bytes):
                target.write(v)
            else:
                v.write(target)

    def __len__(self):
        return self.length


def _encode_object_identifier(oid: str) -> bytes:
    cmps = [int(i) for i in oid.split('.')]
    if len(cmps) < 2 or cmps[0] > 39 or cmps[1] > 39:
        raise ValueError('Illegal object identifier')
    return b"".join(
        _number_7bit(n) for n in (40 * cmps[0] + cmps[1], *cmps[2:])
    )


def _number_7bit(n: int) -> bytes:
    values = [n & 127]
    while n := n >> 7:
        values.append(128 | n & 127)
    return bytes(reversed(values))


def _encode_octet_string(value) -> bytes:
    return value.encode() if isinstance(value, str) else value


def _encode_integer(value: int) -> bytes:
    ln = value if value > 0 else value + 1
    return value.to_bytes(ln.bit_length() // 8 + 1, 'big', signed=True)


_encode_fn = {
    Numbers.Integer: _encode_integer,
    Numbers.Enumerated: _encode_integer,
    Numbers.OctetString: _encode_octet_string,
    Numbers.PrintableString: _encode_octet_string,
    Numbers.UTF8String: _encode_octet_string,
    Numbers.IA5String: _encode_octet_string,
    Numbers.BMPString: _encode_octet_string,
    Numbers.UTCTime: _encode_octet_string,
    Numbers.GeneralizedTime: _encode_octet_string,
    Numbers.BitString: lambda v: b'\x00' + v,
    Numbers.Boolean: lambda v: b'\xff' if v else b'\x00',
    Numbers.Null: lambda v: b'',
    Numbers.ObjectIdentifier: _encode_object_identifier
}


def to_utc_time(dt):
    return dt.strftime('%y%m%d%H%M%SZ')


class Ans1Encoder:
    __slots__ = ['_chain']

    def __init__(self):
        self._chain = BytesChain()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.leave()

    def __call__(self, value=None, nr=None, cls=Classes.Universal):
        if nr is None:
            match value:
                case bool():
                    nr = Numbers.Boolean
                case int():
                    nr = Numbers.Integer
                case str():
                    nr = Numbers.UTF8String
                case bytes():
                    nr = Numbers.OctetString
                case None:
                    nr = Numbers.Null
                case _:
                    raise ValueError('Please specify a tag number (nr)')

        self._write_tag(nr, cls)
        if fn := _encode_fn.get(nr):
            value = fn(value)
        self._write_len(len(value))
        self.write(value)

    def oid(self, value: str, cls=Classes.Universal):
        self.__call__(value, nr=Numbers.ObjectIdentifier, cls=cls)

    def enter(self, nr, cls=Classes.Universal):
        self._write_tag(nr, Types.Constructed | cls)
        self._chain = BytesChain(parent=self._chain)
        return self

    def set(self, cls=Classes.Universal):
        return self.enter(Numbers.Set, cls)

    def seq(self, cls=Classes.Universal):
        return self.enter(Numbers.Sequence, cls)

    def write(self, s: bytes | BytesChain):
        self._chain.append(s)

    def leave(self):
        l_chain = self._chain
        self._chain = l_chain.parent
        l_chain.parent = None  # weak ref
        self._write_len(len(l_chain))
        self.write(l_chain)

    def stream(self, target):
        assert self._chain.parent is None
        self._chain.write(target)

    def output(self) -> bytes:
        with io.BytesIO() as b:
            self.stream(b)
            return b.getvalue()

    def _write_len(self, length: int):
        if length < 128:
            self.write(bytes([length]))
        else:
            ln = (length.bit_length() + 7) // 8
            self.write(bytes([128 | ln]))
            self.write(length.to_bytes(ln, 'big'))

    def _write_tag(self, nr: int, typ_cls: int):
        if nr < 31:
            self.write(bytes([nr | typ_cls]))
        else:
            self.write(bytes([31 | typ_cls]))
            self.write(_number_7bit(nr))
