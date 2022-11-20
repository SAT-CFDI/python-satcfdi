import re
from enum import Enum, auto

# Persona Física / Persona Moral
RFC_Regex = "([A-Z&Ñ]{3,4})([0-9]{2})(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])([A-Z0-9]{2}[0-9A])"

RFC_Verify_Chars = "0123456789ABCDEFGHIJKLMN&OPQRSTUVWXYZ Ñ"


class RFCType(Enum):
    FISICA = auto()
    MORAL = auto()


class RFC(str):
    def __new__(cls, value: str, entity_type: RFCType = None):
        value = value.upper()
        self = super().__new__(cls, value)

        match = re.fullmatch(RFC_Regex, value)
        if match:
            if len(match.group(1)) == 3:
                self.type = RFCType.MORAL
            else:
                self.type = RFCType.FISICA
        else:
            raise ValueError("RFC Not Valid")

        if entity_type and self.type != entity_type:
            raise ValueError("RFC Not as Expected ", self.type)

        return self

    def is_generic(self):
        return self in [RFC_Generico_Nacional, RFC_Generico_Extranjero]

    def is_valid(self):
        if self.is_generic():
            return True

        tot = 0
        if self.type == RFCType.MORAL:
            tot += 481

        for i, c in enumerate(self[::-1], start=1):
            tot += RFC_Verify_Chars.index(c) * i

        return tot % 11 == 0

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__qualname__,
            f'{super().__repr__()}'
        )


RFC_Generico_Nacional = RFC("XAXX010101000")
RFC_Generico_Extranjero = RFC("XEXX010101000")
