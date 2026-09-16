"""Fixtures de conformidad: la red que impide la deriva entre Python y JS.

Estos ficheros los lee tambien el test de JS del front. Si este test falla
despues de tocar el preprocesado, no se "arregla" regenerando los fixtures sin
pensar: significa que los tensores han cambiado y que hay que reentrenar y
actualizar el remuestreo de JS a la vez.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest

from signia_modelo.aplicacion.preprocess import construir_entrada
from signia_modelo.aplicacion.remuestreo import indices_remuestreo
from signia_modelo.dominio.contrato import (
    N_DIMS,
    N_LANDMARKS,
    N_MANOS,
    T,
    VERSION_PREPROCESADO,
)
from signia_modelo.infra.json_contrato import muestra_desde_dict

RAIZ = Path(__file__).resolve().parents[1]
CARPETA = RAIZ / "tests" / "fixtures"
TOLERANCIA = 1e-5


def _cargar_generador():
    """Importa `scripts/generar_fixtures.py` sin convertirlo en paquete."""
    spec = importlib.util.spec_from_file_location(
        "generar_fixtures", RAIZ / "scripts" / "generar_fixtures.py"
    )
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo


GENERADOR = _cargar_generador()
FIXTURES = sorted(CARPETA.glob("*.json"))


def test_hay_fixtures():
    assert FIXTURES, "faltan los fixtures: ejecuta scripts/generar_fixtures.py"


def test_estan_todos_los_casos():
    """Ningun caso limite puede desaparecer en silencio del disco."""
    assert {f.stem for f in FIXTURES} == set(GENERADOR.casos())


@pytest.fixture(params=FIXTURES, ids=lambda p: p.stem)
def fixture(request):
    with request.param.open(encoding="utf-8") as fh:
        return json.load(fh)


class TestCadaFixture:
    def test_declara_la_version_del_preprocesado(self, fixture):
        assert fixture["version_preprocesado"] == VERSION_PREPROCESADO
        assert fixture["T"] == T

    def test_la_muestra_cruda_sigue_siendo_valida(self, fixture):
        assert muestra_desde_dict(fixture["muestra"]).n_frames > 0

    def test_los_indices_coinciden(self, fixture):
        muestra = muestra_desde_dict(fixture["muestra"])
        assert indices_remuestreo(muestra.n_frames, T) == fixture["esperado"]["indices"]

    def test_el_tensor_coincide(self, fixture):
        muestra = muestra_desde_dict(fixture["muestra"])
        entrada = construir_entrada(muestra)

        esperado_lm = np.asarray(fixture["esperado"]["lm"], dtype=np.float32).reshape(
            T, N_MANOS, N_LANDMARKS, N_DIMS
        )
        esperado_presencia = np.asarray(
            fixture["esperado"]["presencia"], dtype=np.float32
        ).reshape(T, N_MANOS)

        assert np.max(np.abs(entrada.lm - esperado_lm)) < TOLERANCIA
        assert np.array_equal(entrada.presencia, esperado_presencia)

    def test_el_tamano_del_tensor_es_el_del_contrato(self, fixture):
        assert len(fixture["esperado"]["indices"]) == T
        assert len(fixture["esperado"]["presencia"]) == T * N_MANOS
        assert len(fixture["esperado"]["lm"]) == T * N_MANOS * N_LANDMARKS * N_DIMS


def test_el_generador_es_reproducible(tmp_path):
    """Regenerar sin tocar nada tiene que dar exactamente lo mismo."""
    for nombre, muestra in GENERADOR.casos().items():
        recien = GENERADOR.fixture(nombre, muestra)
        with (CARPETA / f"{nombre}.json").open(encoding="utf-8") as fh:
            en_disco = json.load(fh)
        assert recien == en_disco, (
            f"el fixture {nombre} no coincide con lo que genera el codigo actual; "
            "si el cambio es intencionado hay que reentrenar y tocar tambien el JS"
        )
