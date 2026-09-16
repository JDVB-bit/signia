"""La normalizacion que viaja dentro del grafo ONNX.

Se comprueba lo que el modelo necesita que sea cierto: la forma es invariante a
donde y a que distancia se hace la sena, mientras que la posicion y la escala se
conservan como senal aparte.
"""

from __future__ import annotations

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from signia_modelo.aplicacion.preprocess import apilar_frames  # noqa: E402
from signia_modelo.dominio.contrato import (  # noqa: E402
    F,
    IDX_MUNECA,
    IDX_NUDILLO_MEDIO,
    VALORES_FORMA,
    VALORES_POR_MANO,
)
from signia_modelo.dominio.entidades import Frame, Lado  # noqa: E402
from signia_modelo.infra.normalizacion_torch import Normalizacion  # noqa: E402
from tests import factorias  # noqa: E402

pytestmark = pytest.mark.torch

IZQ, DER = 0, 1
# Desglose de los 64 valores de una mano (ver contrato.md).
PRESENCIA = 0
POSICION = slice(1, 3)
ESCALA = 3
FORMA = slice(4, 4 + VALORES_FORMA)


def features(frames, modulo=None):
    """Frames -> tensor (T, 128) normalizado, con lote de 1."""
    entrada = apilar_frames(frames)
    modulo = modulo or Normalizacion()
    with torch.no_grad():
        salida = modulo(
            torch.from_numpy(entrada.lm).unsqueeze(0),
            torch.from_numpy(entrada.presencia).unsqueeze(0),
        )
    return salida[0].numpy()


def bloque(salida, ranura):
    inicio = ranura * VALORES_POR_MANO
    return salida[..., inicio : inicio + VALORES_POR_MANO]


class TestForma:
    def test_forma_de_salida(self):
        frames = [factorias.frame(t) for t in range(7)]
        assert features(frames).shape == (7, F)

    def test_acepta_lotes(self):
        entrada = apilar_frames([factorias.frame(t) for t in range(5)])
        lm = torch.from_numpy(entrada.lm)
        presencia = torch.from_numpy(entrada.presencia)
        lote = Normalizacion()(lm.repeat(3, 1, 1, 1, 1), presencia.repeat(3, 1, 1))
        assert lote.shape == (3, 5, F)
        assert torch.allclose(lote[0], lote[2])


class TestManoAusente:
    def test_la_mano_ausente_sale_en_ceros(self):
        salida = features([factorias.frame(0, (Lado.DERECHA,))])
        assert np.all(bloque(salida, IZQ) == 0.0)
        assert np.any(bloque(salida, DER) != 0.0)

    def test_frame_sin_manos_sale_entero_en_ceros(self):
        assert np.all(features([Frame(0)]) == 0.0)

    def test_el_primer_valor_es_la_presencia(self):
        salida = features([factorias.frame(0, (Lado.DERECHA,))])
        assert bloque(salida, DER)[..., PRESENCIA] == 1.0
        assert bloque(salida, IZQ)[..., PRESENCIA] == 0.0


class TestBloques:
    def test_la_posicion_es_la_de_la_muneca_en_el_encuadre(self):
        mano = factorias.mano(Lado.DERECHA, desplazamiento=(0.3, 0.7))
        salida = features([Frame(0, (mano,))])
        esperado = np.asarray(mano.lm[IDX_MUNECA][:2], dtype=np.float32)
        assert np.allclose(bloque(salida, DER)[0, POSICION], esperado, atol=1e-6)

    def test_la_escala_es_la_distancia_muneca_nudillo(self):
        mano = factorias.mano(Lado.DERECHA)
        muneca = np.asarray(mano.lm[IDX_MUNECA][:2])
        nudillo = np.asarray(mano.lm[IDX_NUDILLO_MEDIO][:2])
        salida = features([Frame(0, (mano,))])
        esperado = float(np.linalg.norm(nudillo - muneca))
        assert bloque(salida, DER)[0, ESCALA] == pytest.approx(esperado, abs=1e-6)

    def test_la_forma_tiene_60_valores(self):
        salida = features([factorias.frame(0)])
        assert bloque(salida, DER)[0, FORMA].shape == (VALORES_FORMA,)

    def test_el_orden_de_las_ranuras_es_izquierda_derecha(self):
        izq = factorias.mano(Lado.IZQUIERDA, desplazamiento=(0.1, 0.1))
        der = factorias.mano(Lado.DERECHA, desplazamiento=(0.9, 0.9))
        salida = features([Frame(0, (der, izq))])
        assert bloque(salida, IZQ)[0, POSICION] == pytest.approx([0.1, 0.1], abs=1e-6)
        assert bloque(salida, DER)[0, POSICION] == pytest.approx([0.9, 0.9], abs=1e-6)


class TestInvariancias:
    def test_la_forma_no_cambia_al_mover_la_mano(self):
        """La misma sena a la izquierda o a la derecha del encuadre."""
        cerca = features([Frame(0, (factorias.mano(desplazamiento=(0.2, 0.2)),))])
        lejos = features([Frame(0, (factorias.mano(desplazamiento=(0.8, 0.5)),))])
        assert np.allclose(
            bloque(cerca, DER)[0, FORMA], bloque(lejos, DER)[0, FORMA], atol=1e-5
        )

    def test_la_posicion_si_cambia_al_mover_la_mano(self):
        """En LSE donde se hace la sena es significado: no se puede perder."""
        a = features([Frame(0, (factorias.mano(desplazamiento=(0.2, 0.2)),))])
        b = features([Frame(0, (factorias.mano(desplazamiento=(0.8, 0.5)),))])
        assert not np.allclose(
            bloque(a, DER)[0, POSICION], bloque(b, DER)[0, POSICION]
        )

    def test_la_forma_no_cambia_al_acercarse_a_la_camara(self):
        cerca = features([Frame(0, (factorias.mano(escala=2.5),))])
        lejos = features([Frame(0, (factorias.mano(escala=0.4),))])
        assert np.allclose(
            bloque(cerca, DER)[0, FORMA], bloque(lejos, DER)[0, FORMA], atol=1e-4
        )

    def test_la_escala_si_cambia_al_acercarse(self):
        cerca = features([Frame(0, (factorias.mano(escala=2.0),))])
        lejos = features([Frame(0, (factorias.mano(escala=1.0),))])
        assert bloque(cerca, DER)[0, ESCALA] == pytest.approx(
            2 * bloque(lejos, DER)[0, ESCALA], rel=1e-4
        )


class TestRobustez:
    def test_mano_degenerada_no_produce_nan(self):
        """Si MediaPipe colapsa todos los puntos, no puede salir NaN del grafo."""
        plana = factorias.mano(escala=0.0)
        salida = features([Frame(0, (plana,))])
        assert np.all(np.isfinite(salida))
        assert bloque(salida, DER)[0, ESCALA] == 0.0

    def test_no_tiene_parametros_entrenables(self):
        assert list(Normalizacion().parameters()) == []
