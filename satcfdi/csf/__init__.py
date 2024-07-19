import warnings
from datetime import datetime

import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

from .. import __version__
from ..catalogs import select_all
from ..exceptions import ResponseError
from ..models import Code
from ..sat_requests_utils import SSLAdapter

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def retrieve(rfc: str, id_cif: str):
    data = _request_constancia(rfc, id_cif)
    return _parse_response(data)


def url(rfc: str, id_cif: str):
    return f"https://siat.sat.gob.mx/app/qr/faces/pages/mobile/validadorqr.jsf?D1=10&D2=1&D3={id_cif}_{rfc}"


def _request_constancia(rfc: str, id_cif: str):
    with requests.Session() as s:
        s.mount('https://', SSLAdapter())
        res = s.get(
            url=url(rfc, id_cif),
            headers={
                "User-Agent": __version__.__user_agent__,
            }
        )
        if res.ok:
            return res.content
        else:
            raise ResponseError(res)


def _find_regimen(regimen):
    regimen = regimen.rstrip('.').lower()
    for k, v in select_all('C756_c_RegimenFiscal').items():
        if regimen.endswith(v.lower()):
            return Code(k, v)
    return Code(None, regimen)


def _parse_response(data):
    _REGIMENES = "Regimenes"
    html = BeautifulSoup(data, 'html.parser')
    gc_v = html.find_all(name="td", attrs={"role": "gridcell", "style": "text-align:left;"})
    if not gc_v:
        raise ValueError("'rfc' or 'id_cif' is invalid")
    gc_k = html.find_all(name="span", attrs={"style": "font-weight: bold;"})
    result = {_REGIMENES: []}

    for k, v in zip(gc_k, gc_v):
        k = k.text.rstrip(":")
        v = v.text
        if k.startswith("Fecha ") and v:
            v = datetime.strptime(v, "%d-%m-%Y").date()

        if k == 'Régimen':
            result[_REGIMENES].append({
                'RegimenFiscal': _find_regimen(v),
            })
        elif k == 'Fecha de alta':
            result[_REGIMENES][-1][k] = v
        else:
            result[k] = v

    return result
