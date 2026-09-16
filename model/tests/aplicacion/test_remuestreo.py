"""El remuestreo es la unica pieza duplicada en JS: se testea con sana paranoia."""

from __future__ import annotations

import pytest

from signia_modelo.aplicacion.remuestreo import (
    REMUESTREADOR_POR_DEFECTO,
    RemuestreadorPorIndices,
    indices_remuestreo,
)
from signia_modelo.dominio.contrato import T
from signia_modelo.dominio.errores import ErrorDeRemuestreo
from signia_modelo.dominio.puertos import Remuestreador


@pytest.mark.parametrize("n", [1, 2, 17, 47, 48, 49, 200])
def test_siempre_devuelve_destino_indices(n):
    assert len(indices_remuestreo(n, T)) == T


@pytest.mark.parametrize("n", [1, 5, 48, 300])
def test_indices_dentro_del_rango_y_no_decrecientes(n):
    idx = indices_remuestreo(n, T)
    assert all(0 <= i < n for i in idx)
    assert idx == sorted(idx)


@pytest.mark.parametrize("n", [2, 5, 48, 300])
def test_conserva_los_extremos(n):
    """Si se perdiera el primer o el ultimo frame se recortaria la sena."""
    idx = indices_remuestreo(n, T)
    assert idx[0] == 0
    assert idx[-1] == n - 1


def test_secuencia_de_longitud_exacta_es_la_identidad():
    assert indices_remuestreo(T, T) == list(range(T))


def test_secuencia_de_un_frame_repite_ese_frame():
    assert indices_remuestreo(1, T) == [0] * T


def test_secuencia_corta_repite_frames_sin_saltarse_ninguno():
    idx = indices_remuestreo(5, T)
    assert set(idx) == {0, 1, 2, 3, 4}


def test_secuencia_larga_se_reparte_uniformemente():
    idx = indices_remuestreo(95, T)
    saltos = {b - a for a, b in zip(idx, idx[1:])}
    assert saltos <= {2, 3}  # ~2 frames de paso, sin tirones


def test_redondeo_hacia_arriba_como_math_round_de_js():
    """`round()` de Python redondea al par (0.5 -> 0) y Math.round no (0.5 -> 1).

    Si esto cambiara, el navegador y el entrenamiento verian tensores distintos
    y el fallo seria silencioso. Caso minimo donde ambos difieren.
    """
    assert indices_remuestreo(3, 5) == [0, 1, 1, 2, 2]


def test_destino_uno():
    assert indices_remuestreo(10, 1) == [0]


def test_rechaza_secuencia_vacia():
    with pytest.raises(ErrorDeRemuestreo, match="vacia"):
        indices_remuestreo(0, T)


@pytest.mark.parametrize("destino", [0, -1])
def test_rechaza_destino_invalido(destino):
    with pytest.raises(ErrorDeRemuestreo, match="destino"):
        indices_remuestreo(10, destino)


def test_la_implementacion_por_defecto_cumple_el_puerto():
    assert isinstance(REMUESTREADOR_POR_DEFECTO, Remuestreador)
    assert isinstance(RemuestreadorPorIndices(), Remuestreador)


def test_es_deterministico():
    assert indices_remuestreo(77, T) == indices_remuestreo(77, T)
