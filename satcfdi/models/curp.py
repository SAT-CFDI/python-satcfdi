import re

CURP_Regex = "[A-Z][AEIOUX][A-Z]{2}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[MH]([ABCMTZ]S|[BCJMOT]C|[CNPST]L|[GNQ]T|[GQS]R|C[MH]|[MY]N|[DH]G|NE|VZ|DF|SP)[BCDFGHJ-NP-TV-Z]{3}[0-9A-Z][0-9]"
CURP_Verify_Chars = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"


class CURP(str):
    def __new__(cls, value):
        value = value.upper()
        match = re.fullmatch(CURP_Regex, value)
        if match:
            self = super().__new__(cls, value)
            self.estado = match.group(3)
            return self
        else:
            raise ValueError("CURP Not Valid")

    def is_valid(self):
        tot = 0

        for i, c in enumerate(self[::-1], start=1):
            tot += CURP_Verify_Chars.index(c) * i

        return tot % 10 == 0

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__qualname__,
            f'{super().__repr__()}'
        )
