"""Paridad torch <-> onnxruntime: aqui es donde aparecen los bugs de exportacion.

No es un test de cortesia. El navegador ejecutara el grafo con onnxruntime-web;
si el grafo exportado no calcula exactamente lo mismo que el modulo con el que
se entreno, el modelo falla en produccion y funciona en los tests.
"""

from __future__ import annotations

import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("onnx")
pytest.importorskip("onnxruntime")

from signia_modelo.aplicacion.preprocess import construir_entrada  # noqa: E402
from signia_modelo.dominio.contrato import F, N_DIMS, N_LANDMARKS, N_MANOS, T  # noqa: E402
from signia_modelo.dominio.entidades import Lado  # noqa: E402
from signia_modelo.infra.exportacion_onnx import exportar, salida_onnx  # noqa: E402
from signia_modelo.infra.normalizacion_torch import (  # noqa: E402
    NOMBRE_SALIDA,
    NOMBRES_ENTRADA,
    Normalizacion,
)
from tests import factorias  # noqa: E402

pytestmark = [pytest.mark.torch, pytest.mark.onnx]

TOLERANCIA = 1e-5


def entrada_de(muestra):
    e = construir_entrada(muestra)
    return e.lm[None, ...], e.presencia[None, ...]


@pytest.fixture(scope="module")
def grafo(tmp_path_factory):
    lm, presencia = entrada_de(factorias.muestra(30))
    return exportar(
        Normalizacion(),
        (torch.from_numpy(lm), torch.from_numpy(presencia)),
        tmp_path_factory.mktemp("artefactos") / "normalizacion.onnx",
        nombres_entrada=NOMBRES_ENTRADA,
        nombre_salida=NOMBRE_SALIDA,
    )


def comparar(grafo, muestra):
    lm, presencia = entrada_de(muestra)
    with torch.no_grad():
        esperado = Normalizacion()(
            torch.from_numpy(lm), torch.from_numpy(presencia)
        ).numpy()
    obtenido = salida_onnx(grafo, {"lm": lm, "presencia": presencia})
    assert obtenido.shape == esperado.shape
    assert np.max(np.abs(obtenido - esperado)) < TOLERANCIA


def test_el_grafo_se_exporta(grafo):
    assert grafo.is_file() and grafo.stat().st_size > 0


@pytest.mark.parametrize(
    "lados",
    [(Lado.DERECHA,), (Lado.IZQUIERDA,), (Lado.IZQUIERDA, Lado.DERECHA), ()],
    ids=["derecha", "izquierda", "dos_manos", "sin_manos"],
)
def test_paridad_con_torch(grafo, lados):
    comparar(grafo, factorias.muestra(40, lados=lados))


@pytest.mark.parametrize("n_frames", [1, 12, 48, 120])
def test_paridad_con_secuencias_de_cualquier_duracion(grafo, n_frames):
    comparar(grafo, factorias.muestra(n_frames))


def test_el_eje_temporal_es_dinamico(grafo):
    """El modo continuo alimentara ventanas mas cortas que T."""
    lm = np.zeros((1, 12, N_MANOS, N_LANDMARKS, N_DIMS), dtype=np.float32)
    presencia = np.zeros((1, 12, N_MANOS), dtype=np.float32)
    assert salida_onnx(grafo, {"lm": lm, "presencia": presencia}).shape == (1, 12, F)


def test_el_lote_es_dinamico(grafo):
    """El entrenamiento evalua por lotes; el navegador, de uno en uno."""
    lm = np.zeros((4, T, N_MANOS, N_LANDMARKS, N_DIMS), dtype=np.float32)
    presencia = np.ones((4, T, N_MANOS), dtype=np.float32)
    assert salida_onnx(grafo, {"lm": lm, "presencia": presencia}).shape == (4, T, F)
