"""Persistencia de una muestra en disco: ida y vuelta y errores que nombran el fichero."""

from __future__ import annotations

import json

import pytest

from signia_modelo.dominio.errores import ErrorDeContrato
from signia_modelo.infra.ficheros_json import cargar_muestra, guardar_muestra


class TestFicherosJson:
    def test_guardar_y_cargar_desde_disco(self, tmp_path, muestra_frase):
        ruta = tmp_path / "sub" / "frase.json"
        guardar_muestra(ruta, muestra_frase)
        assert cargar_muestra(ruta) == muestra_frase

    def test_json_corrupto_menciona_la_ruta(self, tmp_path):
        ruta = tmp_path / "roto.json"
        ruta.write_text("{no es json", encoding="utf-8")
        with pytest.raises(ErrorDeContrato, match="roto.json"):
            cargar_muestra(ruta)

    def test_error_de_contrato_menciona_la_ruta(self, tmp_path):
        ruta = tmp_path / "malo.json"
        ruta.write_text(json.dumps({"schema": 99}), encoding="utf-8")
        with pytest.raises(ErrorDeContrato, match="malo.json"):
            cargar_muestra(ruta)
