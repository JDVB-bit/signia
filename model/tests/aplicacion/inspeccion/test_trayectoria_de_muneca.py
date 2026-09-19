"""El recorrido de la muneca: lo que se mira para saber si la sena tiene sentido."""

from __future__ import annotations

import pytest

from signia_modelo.aplicacion.inspeccion import lado_mas_presente, trayectoria_de_muneca
from signia_modelo.dominio.contrato import IDX_MUNECA
from signia_modelo.dominio.entidades import Frame, Lado, MuestraAislada
from tests import factorias

IZQ, DER = Lado.IZQUIERDA, Lado.DERECHA


def muestra_con(lados_por_frame, **kwargs) -> MuestraAislada:
    return MuestraAislada(
        frames=tuple(
            factorias.frame(t, lados, **kwargs) for t, lados in enumerate(lados_por_frame)
        ),
        sesion="2026-09-20-test-trayectoria",
        fps_aprox=30.0,
        etiqueta="hola",
    )


class TestEleccionDeLaMano:
    def test_elige_la_que_aparece_en_mas_frames(self):
        muestra = muestra_con([(DER,), (DER,), (IZQ,)])
        assert lado_mas_presente(muestra) is DER

    def test_ante_un_empate_gana_el_primer_lado_canonico(self):
        """Deterministico: dos ejecuciones dibujan la misma mano."""
        muestra = muestra_con([(IZQ,), (DER,)])
        assert lado_mas_presente(muestra) is Lado.canonicos()[0]

    def test_se_puede_pedir_una_mano_concreta(self):
        muestra = muestra_con([(DER,), (DER,), (IZQ,)])
        assert trayectoria_de_muneca(muestra, IZQ).lado is IZQ

    def test_sin_pedir_nada_usa_la_mas_presente(self):
        muestra = muestra_con([(IZQ,), (IZQ,), (DER,)])
        assert trayectoria_de_muneca(muestra).lado is IZQ


class TestPuntos:
    def test_hay_un_punto_por_frame(self):
        muestra = muestra_con([(DER,), (), (DER,)])
        assert trayectoria_de_muneca(muestra).n_frames == muestra.n_frames

    def test_los_frames_sin_esa_mano_quedan_como_hueco(self):
        """El hueco en el trazo es informacion: no se rellena con nada."""
        trazo = trayectoria_de_muneca(muestra_con([(DER,), (), (DER,)]), DER)
        assert trazo.puntos[1] is None
        assert len(trazo.presentes) == 2

    def test_el_punto_es_la_muneca_de_esa_mano(self):
        muestra = muestra_con([(DER,)], desplazamiento=(0.3, 0.7))
        x, y, _z = muestra.frames[0].mano(DER).lm[IDX_MUNECA]
        assert trayectoria_de_muneca(muestra, DER).puntos[0] == pytest.approx((x, y))

    def test_sigue_el_desplazamiento_de_la_mano(self):
        frames = [
            factorias.frame(t, (DER,), desplazamiento=(t / 10, 0.5)) for t in range(3)
        ]
        muestra = MuestraAislada(frames=tuple(frames), sesion="s", etiqueta="hola")
        xs = [punto[0] for punto in trayectoria_de_muneca(muestra, DER).presentes]
        assert xs == sorted(xs)

    def test_una_mano_que_no_sale_da_una_trayectoria_vacia(self):
        trazo = trayectoria_de_muneca(muestra_con([(DER,), (DER,)]), IZQ)
        assert trazo.esta_vacia
        assert trazo.presentes == ()

    def test_una_muestra_sin_ninguna_mano_no_rompe(self):
        muestra = MuestraAislada(
            frames=tuple(Frame(t) for t in range(3)), sesion="s", etiqueta="reposo"
        )
        assert trayectoria_de_muneca(muestra).esta_vacia
