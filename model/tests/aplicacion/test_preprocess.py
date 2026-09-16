"""El tensor crudo: ranuras fijas, presencia honesta y cero normalizacion."""

from __future__ import annotations

import numpy as np
import pytest

from signia_modelo.aplicacion.preprocess import RANURAS, apilar_frames, construir_entrada
from signia_modelo.dominio.contrato import N_DIMS, N_LANDMARKS, N_MANOS, T
from signia_modelo.dominio.entidades import Frame, Lado, MuestraAislada
from tests import factorias

IZQ, DER = 0, 1


def test_ranuras_en_orden_canonico():
    assert RANURAS == (Lado.IZQUIERDA, Lado.DERECHA)


def test_forma_y_tipo_del_tensor(muestra_aislada):
    entrada = construir_entrada(muestra_aislada)
    assert entrada.lm.shape == (T, N_MANOS, N_LANDMARKS, N_DIMS)
    assert entrada.presencia.shape == (T, N_MANOS)
    assert entrada.lm.dtype == np.float32
    assert entrada.presencia.dtype == np.float32


def test_una_sola_mano_deja_la_otra_ranura_en_cero(muestra_aislada):
    entrada = construir_entrada(muestra_aislada)  # solo mano derecha
    assert np.all(entrada.presencia[:, DER] == 1.0)
    assert np.all(entrada.presencia[:, IZQ] == 0.0)
    assert np.all(entrada.lm[:, IZQ] == 0.0)
    assert np.any(entrada.lm[:, DER] != 0.0)


def test_frame_sin_manos_tiene_presencia_cero():
    muestra = MuestraAislada(
        frames=(Frame(0), factorias.frame(1), Frame(2)),
        sesion="s",
        etiqueta="reposo",
    )
    entrada = construir_entrada(muestra, destino=3)
    assert entrada.presencia.tolist() == [[0.0, 0.0], [0.0, 1.0], [0.0, 0.0]]


def test_la_ranura_no_depende_del_orden_de_deteccion():
    """MediaPipe devuelve las manos en el orden que quiere; el `lado` manda."""
    izq = factorias.mano(Lado.IZQUIERDA, desplazamiento=(0.1, 0.1))
    der = factorias.mano(Lado.DERECHA, desplazamiento=(0.9, 0.9))
    a = apilar_frames([Frame(0, (izq, der))])
    b = apilar_frames([Frame(0, (der, izq))])
    assert np.array_equal(a.lm, b.lm)
    assert a.lm[0, IZQ, 0, 0] == pytest.approx(0.1)
    assert a.lm[0, DER, 0, 0] == pytest.approx(0.9)


def test_guarda_los_landmarks_crudos_sin_tocarlos():
    """Principio 1: aqui no se normaliza nada (salvo pasar a float32)."""
    mano = factorias.mano(Lado.DERECHA, desplazamiento=(0.42, 0.37))
    entrada = apilar_frames([Frame(0, (mano,))])
    esperado = np.asarray([list(p) for p in mano.lm], dtype=np.float32)
    assert np.array_equal(entrada.lm[0, DER], esperado)


def test_respeta_un_destino_distinto_de_t(muestra_aislada):
    entrada = construir_entrada(muestra_aislada, destino=16)
    assert entrada.lm.shape[0] == 16


def test_usa_el_remuestreador_inyectado():
    """DIP: el preprocesado depende del puerto, no de la estrategia concreta."""

    class RemuestreadorFalso:
        def indices(self, n_frames, destino):
            return [n_frames - 1] * destino  # siempre el ultimo frame

    muestra = MuestraAislada(
        frames=(Frame(0), Frame(1), factorias.frame(2)),
        sesion="s",
        etiqueta="hola",
    )
    entrada = construir_entrada(muestra, remuestreador=RemuestreadorFalso(), destino=4)
    assert entrada.presencia.tolist() == [[0.0, 1.0]] * 4


def test_el_orden_temporal_se_conserva():
    frames = tuple(
        factorias.frame(t, desplazamiento=(t / 10, 0.0)) for t in range(10)
    )
    muestra = MuestraAislada(frames=frames, sesion="s", etiqueta="hola")
    entrada = construir_entrada(muestra, destino=10)
    xs = entrada.lm[:, DER, 0, 0]
    assert np.all(np.diff(xs) > 0)
