# !/usr/bin/env python3

"""Implements the client for Series."""

# pylint: skip-file
# pydocstyle: add-ignore=D105,D107,D401

from typing import Dict, Optional

import requests
import requests.auth

from .. import __version__
from ..exceptions import ResponseError


class SieAPIRest:
    """
    SIE-BANXICO API
    API de consulta de series de tiempo del Banco de México
    version: 1.4.3-hotfix1
    """

    def __init__(
            self,
            bmx_token: str,
            url_prefix: str = "https://www.banxico.org.mx") -> None:
        self.headers = {
            'Bmx-Token': bmx_token,
            'Accept': 'application/json',
            "User-Agent": __version__.__user_agent__
        }
        self.url_prefix = url_prefix

    def _request(self, method, path, params=None):
        print(f"{self.url_prefix}/{path}")

        resp = requests.request(
            method=method,
            url=f"{self.url_prefix}/{path}",
            headers=self.headers,
            params=params
        )

        if resp.status_code == 200:
            return resp.json()

        raise ResponseError(resp.text)

    def metadatos_series_using_get(
            self,
            id_series: str,
    ) -> str:
        """
        Series metadata
        Send a get request to SieAPIRest/service/v1/series/{idSeries}.

        :param id_series: idSeries
        :return: OK
        """
        return self._request(
            method="get",
            path=f"SieAPIRest/service/v1/series/{id_series}"
        )

    def datos_series_using_get(
            self,
            id_series: str,
            decimales: Optional[str] = None,
            incremento: Optional[str] = None,
    ) -> str:
        """
        Series data
        Send a get request to SieAPIRest/service/v1/series/{idSeries}/datos.

        :param id_series: idSeries
        :param decimales: 'sinCeros' to remove trailing zeros to the right of the decimal point.
        :param incremento: 'PorcObsAnt', 'PorcAnual', 'PorcAcumAnual'.
        :return: OK
        """
        params = {}  # type: Dict[str, str]
        if decimales is not None:
            params['decimales'] = decimales
        if incremento is not None:
            params['incremento'] = incremento

        return self._request(
            method='get',
            path=f"SieAPIRest/service/v1/series/{id_series}/datos",
            params=params
        )

    def datos_oportuno_series_using_get(
            self,
            id_series: str,
            decimales: Optional[str] = None,
            incremento: Optional[str] = None,
    ) -> str:
        """
        Last data
        Send a get request to SieAPIRest/service/v1/series/{idSeries}/datos/oportuno.

        :param id_series: idSeries
        :param decimales: 'sinCeros' to remove trailing zeros to the right of the decimal point.
        :param incremento: 'PorcObsAnt', 'PorcAnual', 'PorcAcumAnual'.
        :return: OK
        """
        params = {}  # type: Dict[str, str]
        if decimales is not None:
            params['decimales'] = decimales
        if incremento is not None:
            params['incremento'] = incremento

        return self._request(
            method='get',
            path=f"SieAPIRest/service/v1/series/{id_series}/datos/oportuno",
            params=params,
        )

    def obten_rango_datos_series_using_get(
            self,
            id_series: str,
            fecha_inicial: str,
            fecha_final: str,
            decimales: Optional[str] = None,
            incremento: Optional[str] = None,
    ) -> str:
        """
        Data range
        Send a get request to SieAPIRest/service/v1/series/{idSeries}/datos/{fechaInicial}/{fechaFinal}.

        :param id_series: idSeries
        :param fecha_inicial: fechaInicial
        :param fecha_final: fechaFinal
        :param decimales: 'sinCeros' to remove trailing zeros to the right of the decimal point.
        :param incremento: 'PorcObsAnt', 'PorcAnual', 'PorcAcumAnual'.
        :return: OK
        """
        params = {}  # type: Dict[str, str]
        if decimales is not None:
            params['decimales'] = decimales
        if incremento is not None:
            params['incremento'] = incremento

        return self._request(
            method='get',
            path=f"SieAPIRest/service/v1/series/{id_series}/datos/{fecha_inicial}/{fecha_final}",
            params=params,
        )

    def metadatos_series_versionadas_using_get(
            self,
            id_series: str,
    ) -> str:
        """
        Series versions metadata
        Send a get request to SieAPIRest/service/v1/series/{idSeries}/versiones.

        :param id_series: idSeries
        :return: OK
        """
        return self._request(
            method='get',
            path=f"SieAPIRest/service/v1/series/{id_series}/versiones",
        )

    def datos_series_versionadas_using_get(
            self,
            id_series: str,
            id_version: str,
            decimales: Optional[str] = None,
            incremento: Optional[str] = None,
    ) -> str:
        """
        Series data
        Send a get request to SieAPIRest/service/v1/series/{idSeries}/versiones/{idVersion}/datos.

        :param id_series: idSeries
        :param id_version: idVersion
        :param decimales: 'sinCeros' to remove trailing zeros to the right of the decimal point.
        :param incremento: 'PorcObsAnt', 'PorcAnual', 'PorcAcumAnual'.
        :return: OK
        """
        params = {}  # type: Dict[str, str]
        if decimales is not None:
            params['decimales'] = decimales
        if incremento is not None:
            params['incremento'] = incremento

        return self._request(
            method='get',
            path=f"SieAPIRest/service/v1/series/{id_series}/versiones/{id_version}/datos",
            params=params,
        )
