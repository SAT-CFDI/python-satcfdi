import filecmp
import inspect
import os
import uuid
from collections import defaultdict
from datetime import datetime
from pprint import PrettyPrinter

from satcfdi.xelement import XElement

from satcfdi.models import Signer
from satcfdi.cfdi import CFDI
from satcfdi.models.certificate_store import CertificateStore
from satcfdi.create.cfd.tfd11 import TimbreFiscalDigital

module = 'satcfdi'
current_dir = os.path.dirname(__file__)


def stamp_v11(cfdi: CFDI, signer: Signer, date: datetime = None):
    timbre = TimbreFiscalDigital(
        proveedor=signer,
        uuid=str(uuid.uuid4()),
        sello_cfd=cfdi["Sello"],
        fecha_timbrado=date,
        leyenda=None,
    )
    if not cfdi.get("Complemento"):
        cfdi["Complemento"] = {}

    cfdi["Complemento"]["TimbreFiscalDigital"] = timbre


SAT_Certificate_Store_Pruebas = CertificateStore.create(os.path.join(current_dir, "SATCertsPruebas.zip"))


def get_signer(rfc: str, get_csd=False):
    if len(rfc) == 13:
        tp = "Personas Fisicas"
    elif len(rfc) == 12:
        tp = "Personas Morales"
    else:
        tp = ""

    if get_csd:
        app = "_csd"
    else:
        app = ""

    rfc = rfc.lower()

    return Signer.load(
        certificate=open(os.path.join(current_dir, f'csd/{tp}/{rfc}{app}.cer'), 'rb').read(),
        key=open(os.path.join(current_dir, f'csd/{tp}/{rfc}{app}.key'), 'rb').read(),
        password=open(os.path.join(current_dir, f'csd/{tp}/{rfc}{app}.txt'), 'rb').read()
    )


def get_rfc_pac(self):
    return "SAT970701NN3"


def _uuid():
    return uuid.UUID("6d7434a6-e3f2-47ad-9e4c-08849946afa0")


def verify_result(data, filename):
    calle_frame = inspect.stack()[1]
    caller_file = inspect.getmodule(calle_frame[0]).__file__
    caller_file = os.path.splitext(os.path.basename(caller_file))[0]

    if isinstance(data, bytes):
        ap = 'b'
    else:
        ap = ''
    filename_base, filename_ext = os.path.splitext(filename)

    full_path = os.path.join(current_dir, caller_file, filename_base)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    try:
        with open(full_path + filename_ext, 'r' + ap, encoding=None if ap else 'utf-8') as f:
            if f.read() == data:
                os.remove(full_path + ".diff" + filename_ext)
                return True
        with open(full_path + ".diff" + filename_ext, 'w' + ap, encoding=None if ap else 'utf-8', newline=None if ap else '\n') as f:
            f.write(data)
        return False
    except FileNotFoundError:
        with open(full_path + filename_ext, 'w' + ap, encoding=None if ap else 'utf-8', newline=None if ap else '\n') as f:
            f.write(data)
        return True


class XElementPrettyPrinter(PrettyPrinter):
    _dispatch = PrettyPrinter._dispatch.copy()
    _dispatch[XElement.__repr__] = PrettyPrinter._pprint_dict
    _dispatch[defaultdict.__repr__] = PrettyPrinter._pprint_dict


def compare_directories(dir1, dir2):
    # Check if both paths are directories
    if not (os.path.isdir(dir1) and os.path.isdir(dir2)):
        return False

    # Use filecmp to compare directories
    dcmp = filecmp.dircmp(dir1, dir2)

    # Check for common files that are different
    if dcmp.diff_files:
        for f in dcmp.diff_files:
            if f.endswith(".xlsx"):
                continue
            else:
                print(f"Files that are different: {dcmp.diff_files} in {dir2}")
                return False

    # Check for files present in one directory but not in the other
    if dcmp.left_only or dcmp.right_only:
        print(f"Files present only in one directory: {dcmp.left_only + dcmp.right_only} in {dir2}")
        return False

    # Check for subdirectories that are not present in both directories
    if dcmp.subdirs:
        for subdir in dcmp.subdirs:
            subdir1 = os.path.join(dir1, subdir)
            subdir2 = os.path.join(dir2, subdir)
            if not compare_directories(subdir1, subdir2):
                return False

    return True


if __name__ == "__main__":
    import os

    for f in os.listdir("cfdi//cfdv32"):
        print(repr('cfdv32//' + f) + ",")
