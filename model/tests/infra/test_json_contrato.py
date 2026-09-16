"""La frontera del sistema: lo que entra en JSON se valida o no entra."""

from __future__ import annotations

import json

import pytest

from signia_modelo.dominio.contrato import N_LANDMARKS, SCHEMA
from signia_modelo.dominio.entidades import MuestraAislada, MuestraFrase
from signia_modelo.dominio.errores import ErrorDeContrato
from signia_modelo.infra.json_contrato import (
    cargar_muestra,
    guardar_muestra,
    muestra_a_dict,
    muestra_desde_dict,
)
from tests import factorias

PUNTOS = [[0.0, 0.0, 0.0]] * N_LANDMARKS


def dict_minimo(**extra):
    base = {
        "schema": SCHEMA,
        "etiqueta": "hola",
        "sesion": "2026-09-20-snt-01",
        "fps_aprox": 30,
        "frames": [
            {"t": 0, "manos": [{"lado": "derecha", "score": 0.98, "lm": PUNTOS}]}
        ],
    }
    base.update(extra)
    return base


class TestLectura:
    def test_lee_una_aislada(self):
        m = muestra_desde_dict(dict_minimo())
        assert isinstance(m, MuestraAislada)
        assert m.etiqueta == "hola"
        assert m.sesion == "2026-09-20-snt-01"
        assert m.frames[0].manos[0].score == pytest.approx(0.98)

    def test_el_tipo_por_defecto_es_aislada(self):
        assert muestra_desde_dict(dict_minimo()).tipo == "aislada"

    def test_lee_una_frase(self):
        d = dict_minimo(tipo="frase", etiquetas=["hola", "como"])
        d.pop("etiqueta")
        m = muestra_desde_dict(d)
        assert isinstance(m, MuestraFrase)
        assert m.glosas == ("hola", "como")

    def test_acepta_frames_sin_manos(self):
        d = dict_minimo(frames=[{"t": 0}, {"t": 1, "manos": []}])
        assert muestra_desde_dict(d).n_frames == 2

    def test_score_por_defecto_si_falta(self):
        d = dict_minimo(frames=[{"t": 0, "manos": [{"lado": "derecha", "lm": PUNTOS}]}])
        assert muestra_desde_dict(d).frames[0].manos[0].score == 1.0


class TestValidacion:
    def test_rechaza_lo_que_no_es_objeto(self):
        with pytest.raises(ErrorDeContrato, match="objeto JSON"):
            muestra_desde_dict([1, 2, 3])

    def test_rechaza_schema_desconocido(self):
        with pytest.raises(ErrorDeContrato, match="schema"):
            muestra_desde_dict(dict_minimo(schema=99))

    def test_rechaza_sin_frames(self):
        d = dict_minimo()
        d.pop("frames")
        with pytest.raises(ErrorDeContrato, match="frames"):
            muestra_desde_dict(d)

    def test_rechaza_aislada_sin_etiqueta(self):
        d = dict_minimo()
        d.pop("etiqueta")
        with pytest.raises(ErrorDeContrato, match="etiqueta"):
            muestra_desde_dict(d)

    def test_rechaza_frase_sin_etiquetas(self):
        with pytest.raises(ErrorDeContrato, match="etiquetas"):
            muestra_desde_dict(dict_minimo(tipo="frase"))

    def test_rechaza_tipo_desconocido(self):
        with pytest.raises(ErrorDeContrato, match="tipo de muestra desconocido"):
            muestra_desde_dict(dict_minimo(tipo="video"))

    def test_rechaza_lado_invalido(self):
        d = dict_minimo(frames=[{"t": 0, "manos": [{"lado": "left", "lm": PUNTOS}]}])
        with pytest.raises(ErrorDeContrato, match="lado invalido"):
            muestra_desde_dict(d)

    def test_el_error_situa_el_frame_y_la_mano(self):
        d = dict_minimo(
            frames=[
                {"t": 0, "manos": []},
                {"t": 1, "manos": [{"lado": "derecha", "lm": [[0, 0, 0]] * 3}]},
            ]
        )
        with pytest.raises(ErrorDeContrato, match="frame 1, mano 0"):
            muestra_desde_dict(d)

    def test_rechaza_lm_que_no_es_lista(self):
        d = dict_minimo(frames=[{"t": 0, "manos": [{"lado": "derecha", "lm": "x"}]}])
        with pytest.raises(ErrorDeContrato, match="'lm' debe ser una lista"):
            muestra_desde_dict(d)


class TestEscrituraYRoundTrip:
    @pytest.mark.parametrize("fabrica", [factorias.muestra, factorias.frase])
    def test_ida_y_vuelta_conserva_la_muestra(self, fabrica):
        original = fabrica()
        copia = muestra_desde_dict(muestra_a_dict(original))
        assert copia == original

    def test_el_dict_es_serializable_a_json(self, muestra_aislada):
        texto = json.dumps(muestra_a_dict(muestra_aislada))
        assert muestra_desde_dict(json.loads(texto)) == muestra_aislada

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
