import inspect
import json
from unittest import mock

from satcfdi.apis.banxico import SieAPIRest
from tests.utils import verify_result


def test_banxico():
    bmx_token = "xxx"

    api = SieAPIRest(
        bmx_token=bmx_token
    )

    value = {
        "bmx": {
            "series": [
                {
                    "idSerie": "SF343410",
                    "titulo": "Tipo de Cambio Cierre de Jornada",
                    "datos": [
                        {
                            "fecha": "11/11/2022",
                            "dato": "19.4920"
                        }
                    ]
                }
            ]
        }
    }
    with mock.patch(f'requests.request') as mk:
        mk.return_value.status_code = 200
        mk.return_value.json = mock.Mock(
            return_value=value
        )

        res = api.datos_oportuno_series_using_get(
            id_series='SF343410'
        )

        assert res == value

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2)
        verify = verify_result(data=args, filename=f"{inspect.stack()[0][3]}.json")
        assert verify
