"""Medir una muestra: cuanta mano hay dentro y cuanto dura."""

from __future__ import annotations

import pytest

from signia_modelo.aplicacion.inspeccion import medir
from signia_modelo.dominio.entidades import Frame, Lado, MuestraAislada
from tests import factorias

IZQ, DER = Lado.IZQUIERDA, Lado.DERECHA


def muestra_con(lados_por_frame, *, fps: float | None = 30.0) -> MuestraAislada:
    """Muestra a medida: un frame por elemento, con esas manos dentro."""
    return MuestraAislada(
        frames=tuple(factorias.frame(t, lados) for t, lados in enumerate(lados_por_frame)),
        sesion="2026-09-20-test-metricas",
        fps_aprox=fps,
        etiqueta="hola",
    )


class TestPresenciaDeManos:
    def test_cuenta_los_frames_con_alguna_mano(self):
        metricas = medir(muestra_con([(DER,), (), (IZQ,), ()]))
        assert metricas.frames_con_alguna_mano == 2
        assert metricas.frames_sin_manos == 2

    def test_cuenta_los_frames_con_las_dos(self):
        metricas = medir(muestra_con([(IZQ, DER), (DER,), (IZQ, DER)]))
        assert metricas.frames_con_las_dos_manos == 2

    def test_cuenta_por_lado_en_el_orden_canonico(self):
        metricas = medir(muestra_con([(DER,), (DER,), (IZQ,)]))
        izquierda, derecha = metricas.frames_por_lado
        assert (izquierda, derecha) == (1, 2)

    def test_una_muestra_sin_manos_no_tiene_presencia(self):
        muestra = MuestraAislada(
            frames=tuple(Frame(t) for t in range(5)),
            sesion="s",
            fps_aprox=30.0,
            etiqueta="reposo",
        )
        metricas = medir(muestra)
        assert metricas.frames_con_alguna_mano == 0
        assert metricas.proporcion_con_mano == 0.0

    def test_dos_manos_del_mismo_lado_cuentan_una_vez(self):
        """MediaPipe reporta duplicados; `Frame.mano()` ya elige una sola."""
        frame = Frame(0, manos=(factorias.mano(DER, score=0.9), factorias.mano(DER, score=0.4)))
        muestra = MuestraAislada(frames=(frame,), sesion="s", etiqueta="hola")
        metricas = medir(muestra)
        assert metricas.frames_por_lado == (0, 1)
        assert metricas.frames_con_las_dos_manos == 0


class TestBimanualidad:
    def test_es_bimanual_si_lo_es_en_la_mitad_de_los_frames(self):
        metricas = medir(muestra_con([(IZQ, DER), (IZQ, DER), (DER,), (DER,)]))
        assert metricas.usa_las_dos_manos

    def test_un_frame_suelto_con_dos_manos_no_la_hace_bimanual(self):
        """La otra mano pasando por el encuadre no convierte la sena en bimanual."""
        metricas = medir(muestra_con([(DER,), (DER,), (DER,), (IZQ, DER)]))
        assert not metricas.usa_las_dos_manos


class TestDuracion:
    def test_los_segundos_salen_de_los_fps(self):
        metricas = medir(muestra_con([(DER,)] * 60, fps=30.0))
        assert metricas.segundos == pytest.approx(2.0)

    def test_sin_fps_no_se_inventa_la_duracion(self):
        assert medir(muestra_con([(DER,)] * 10, fps=None)).segundos is None

    def test_la_proporcion_con_mano_es_una_fraccion(self):
        metricas = medir(muestra_con([(DER,), (), (DER,), ()]))
        assert metricas.proporcion_con_mano == pytest.approx(0.5)
