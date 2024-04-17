import json
import os
import types
from pprint import pprint
from unittest import mock

import pytest

from satcfdi.csf import retrieve, _parse_response, _find_regimen
from tests.utils import verify_result

current_dir = os.path.dirname(__file__)
current_filename = os.path.splitext(os.path.basename(__file__))[0]
test_dir = os.path.join(current_dir, current_filename)
module = 'satcfdi'

generacion = [
    'persona_fisica.html',
]


@pytest.mark.parametrize('file', generacion)
def test_get_constancia(file):
    with open(os.path.join(current_dir, 'csf', file), 'rb') as f:
        data = f.read()

    with mock.patch(f'requests.sessions.Session.get') as mk:
        mk.return_value.content = data

        res = retrieve('RFC', 'ID_CIF')

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename=f"{file}.json")
        assert verify

    verify = verify_result(data=json.dumps(res, indent=2, default=str, ensure_ascii=False), filename=f"{file}_res.json")
    assert verify


generacion_invalid = [
    'invalid.html'
]


@pytest.mark.parametrize('file', generacion_invalid)
def test_get_constancia_invalid(file):
    with open(os.path.join(current_dir, 'csf', file), 'rb') as f:
        data = f.read()

    def req(*args, **kwargs):
        a = types.SimpleNamespace()
        a.content = data
        a.ok = True
        return a

    with mock.patch(f'requests.sessions.Session.get', req) as mk:

        with pytest.raises(ValueError) as excinfo:
            res = retrieve('RFC', 'ID_CIF')


@pytest.mark.parametrize('file', generacion)
def test_parse_response(file):
    # html = BeautifulSoup(res.text, 'html.parser')
    with open(os.path.join(current_dir, 'csf', file), 'rb') as f:
        data = f.read()

    res = _parse_response(data)
    pprint(res)


def test_regimen_name():
    res = _find_regimen('Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas.')
    assert res == '625'

    res = _find_regimen('Régimen de los ingresos por intereses')
    assert res == '614'

    res = _find_regimen('NotFound')
    assert res == None
