import os
import pickle
import sqlite3

from ..models import Code

current_dir = os.path.dirname(__file__)

db_file = os.path.join(current_dir, "catalogs.db")
conn = sqlite3.connect(db_file)
c = conn.cursor()


def select(catalog_name, key):
    c.execute(f"SELECT value FROM {catalog_name} WHERE key = ?", (pickle.dumps(key),))
    if ds := c.fetchone():
        return pickle.loads(ds[0])


def select_all(catalog_name):
    c.execute(f"SELECT key, value FROM {catalog_name}")
    return {pickle.loads(k): pickle.loads(v) for k, v in c.fetchall()}


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
    c.execute(f"SELECT value FROM TTranslations WHERE key = ?", (k,))
    if res := c.fetchone():
        res = res[0]

    if res is None:
        res = split_at_upper(k)
    return res


def catalog_code(catalog_name, key, index=None):
    code = key
    if isinstance(key, tuple):
        code = key[0]

    if ds := select(catalog_name, key):
        if index is not None:
            ds = ds[index]
    return Code(code, ds)

    # else:
    #     logger.error("Key Not found: %s %s", catalog_name, " ".join(args))


def moneda_decimales(moneda):
    return select('Tae00f1168e4dd44ad14f604041a8e80bcade7279', moneda)[1]


def codigo_postal_uso_horario(codigo_postal):
    return select('T1c22cc9094f6f89d8589f52d827f368d767db6b0', codigo_postal)[4]
