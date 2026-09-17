"""Agregar el dataset por clase y por tipo, sin juzgarlo."""

from __future__ import annotations

import pytest

from signia_modelo.aplicacion.inspeccion import resumir
from signia_modelo.dominio.entidades import Lado
from tests import factorias

IZQ, DER = Lado.IZQUIERDA, Lado.DERECHA


def aisladas(etiqueta: str, cuantas: int, *, sesion: str = "s1", n_frames: int = 30):
    """`cuantas` muestras de la misma sena y la misma sesion."""
    return [
        factorias.muestra(n_frames, etiqueta=etiqueta, sesion=sesion) for _ in range(cuantas)
    ]


class TestAgrupacionPorClase:
    def test_cuenta_las_muestras_de_cada_sena(self):
        resumen = resumir([*aisladas("hola", 3), *aisladas("reposo", 2)])
        assert resumen.n_clases == 2
        assert resumen.clase("hola").n_muestras == 3
        assert resumen.clase("reposo").n_muestras == 2

    def test_las_clases_salen_en_orden_alfabetico(self):
        """Orden estable: el informe no puede cambiar entre dos ejecuciones."""
        resumen = resumir([*aisladas("tu", 1), *aisladas("como", 1), *aisladas("hola", 1)])
        assert resumen.etiquetas == ("como", "hola", "tu")

    def test_mayusculas_y_espacios_no_crean_clases_fantasma(self):
        resumen = resumir([*aisladas("Hola", 2), *aisladas(" hola ", 1)])
        assert resumen.etiquetas == ("hola",)
        assert resumen.clase("hola").n_muestras == 3

    def test_una_clase_que_no_existe_no_esta(self):
        assert resumir(aisladas("hola", 1)).clase("adios") is None

    def test_clases_salvo_excluye_la_indicada(self):
        resumen = resumir([*aisladas("hola", 1), *aisladas("reposo", 1)])
        assert [c.etiqueta for c in resumen.clases_salvo("reposo")] == ["hola"]

    def test_el_dataset_vacio_se_reconoce(self):
        resumen = resumir([])
        assert resumen.esta_vacio
        assert resumen.n_muestras == 0


class TestMetricasAgregadas:
    def test_las_sesiones_no_se_repiten(self):
        resumen = resumir([*aisladas("hola", 2, sesion="s1"), *aisladas("hola", 3, sesion="s2")])
        assert resumen.clase("hola").sesiones == ("s1", "s2")

    def test_la_media_de_frames_es_la_de_las_muestras(self):
        muestras = [*aisladas("hola", 1, n_frames=20), *aisladas("hola", 1, n_frames=40)]
        assert resumir(muestras).clase("hola").media_de_frames == pytest.approx(30.0)

    def test_la_media_de_segundos_usa_los_fps_de_cada_muestra(self):
        assert resumir(aisladas("hola", 2, n_frames=60)).clase(
            "hola"
        ).media_de_segundos == pytest.approx(2.0)

    def test_sin_fps_la_duracion_media_es_desconocida(self):
        muestra = factorias.muestra(10, etiqueta="hola")
        sin_fps = type(muestra)(
            frames=muestra.frames, sesion=muestra.sesion, fps_aprox=None, etiqueta="hola"
        )
        assert resumir([sin_fps]).clase("hola").media_de_segundos is None

    def test_cuenta_las_muestras_bimanuales(self):
        una_mano = factorias.muestra(10, etiqueta="hola", lados=(DER,))
        dos_manos = factorias.muestra(10, etiqueta="hola", lados=(IZQ, DER))
        assert resumir([una_mano, dos_manos, dos_manos]).clase("hola").muestras_bimanuales == 2

    def test_la_proporcion_con_mano_es_del_conjunto_de_la_clase(self):
        con_mano = factorias.muestra(10, etiqueta="hola", lados=(DER,))
        sin_mano = factorias.muestra(10, etiqueta="hola", lados=())
        assert resumir([con_mano, sin_mano]).clase("hola").proporcion_con_mano == pytest.approx(
            0.5
        )

    def test_las_sesiones_del_dataset_juntan_aisladas_y_frases(self):
        resumen = resumir(
            [
                *aisladas("hola", 1, sesion="s1"),
                factorias.frase(30, sesion="s2"),
            ]
        )
        assert resumen.sesiones == ("s1", "s2")


class TestFrases:
    def test_las_frases_no_cuentan_como_clases(self):
        """Principio 6: la unidad de entrenamiento es la sena, nunca la frase."""
        resumen = resumir([factorias.frase(30, etiquetas=("hola", "tu"))])
        assert resumen.n_clases == 0
        assert resumen.frases.n_frases == 1

    def test_recoge_el_glosario_usado_ordenado(self):
        resumen = resumir(
            [
                factorias.frase(30, etiquetas=("hola", "tu")),
                factorias.frase(30, etiquetas=("tu", "como")),
            ]
        )
        assert resumen.frases.glosas_usadas == ("como", "hola", "tu")

    def test_distingue_las_secuencias_repetidas(self):
        repetida = ("hola", "tu")
        resumen = resumir([factorias.frase(30, etiquetas=repetida) for _ in range(3)])
        assert resumen.frases.n_frases == 3
        assert resumen.frases.ordenes_distintos == 1

    def test_el_mismo_orden_invertido_cuenta_como_otra_secuencia(self):
        resumen = resumir(
            [
                factorias.frase(30, etiquetas=("hola", "tu")),
                factorias.frase(30, etiquetas=("tu", "hola")),
            ]
        )
        assert resumen.frases.ordenes_distintos == 2

    def test_la_media_de_glosas_por_frase(self):
        resumen = resumir(
            [
                factorias.frase(30, etiquetas=("hola",)),
                factorias.frase(30, etiquetas=("hola", "tu", "como")),
            ]
        )
        assert resumen.frases.media_de_glosas == pytest.approx(2.0)

    def test_sin_frases_el_conjunto_de_evaluacion_esta_vacio(self):
        frases = resumir(aisladas("hola", 1)).frases
        assert frases.n_frases == 0
        assert frases.glosas_usadas == ()
        assert frases.media_de_glosas == 0.0
