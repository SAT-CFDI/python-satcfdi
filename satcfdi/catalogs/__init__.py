import os
import pickle
import sqlite3

from ..models import Code

current_dir = os.path.dirname(__file__)

db_file = os.path.join(current_dir, "catalogs.db")
conn = sqlite3.connect(db_file, check_same_thread=False)
c = conn.cursor()


def select(catalog_name, key):
    c.execute(f"SELECT value FROM {catalog_name} WHERE key = ?", (pickle.dumps(key),))
    if ds := c.fetchone():
        return pickle.loads(ds[0])


def select_all(catalog_name):
    c.execute(f"SELECT key, value FROM {catalog_name}")
    return {pickle.loads(k): pickle.loads(v) for k, v in c.fetchall()}


def catalog_code(catalog_name, key, index=None):
    code = key
    if isinstance(key, tuple):
        code = key[0]

    if ds := select(catalog_name, key):
        if index is not None:
            ds = ds[index]
    return Code(code, ds)


def moneda_decimales(moneda):
    return select('C756_c_Moneda', moneda)[1]


def codigo_postal_uso_horario(codigo_postal):
    return select('C756_c_CodigoPostal', codigo_postal)[4]


def split_at_upper(word: str):
    def split_at_upper_itr(word: str):
        piu = None
        for w in word:
            niu = w.isupper()
            if piu == False:
                if niu:
                    yield " "

            if piu is None:
                yield w.upper()
            else:
                yield w
            piu = niu

    return "".join(split_at_upper_itr(word))


def trans(k):
    c.execute(f"SELECT value FROM Translations WHERE key = ?", (k,))
    if res := c.fetchone():
        return res[0]

    return split_at_upper(k)
