"""Las entidades se validan a si mismas: si existe la instancia, cumple el contrato."""

from __future__ import annotations

import dataclasses

import pytest

from signia_modelo.dominio.contrato import N_LANDMARKS, SCHEMA, TIPO_AISLADA, TIPO_FRASE
from signia_modelo.dominio.entidades import Frame, Lado, Mano, MuestraAislada, MuestraFrase
from signia_modelo.dominio.errores import ErrorDeContrato
from tests import factorias


class TestLado:
    def test_desde_texto_valido(self):
        assert Lado.desde_texto("derecha") is Lado.DERECHA

    def test_desde_texto_invalido(self):
        with pytest.raises(ErrorDeContrato, match="lado invalido"):
            Lado.desde_texto("left")

    def test_los_canonicos_van_en_el_orden_de_las_ranuras(self):
        """Invertir esto mandaria cada mano a la ranura de la otra."""
        assert Lado.canonicos() == (Lado.IZQUIERDA, Lado.DERECHA)

    def test_hay_un_canonico_por_lado(self):
        assert len(Lado.canonicos()) == len(tuple(Lado))


class TestMano:
    def test_normaliza_a_tuplas_de_float(self):
        m = Mano(Lado.DERECHA, 1.0, [[0, 1, 2]] * N_LANDMARKS)
        assert isinstance(m.lm, tuple)
        assert m.lm[0] == (0.0, 1.0, 2.0)

    def test_acepta_lado_como_texto(self):
        assert Mano("izquierda", 0.5, [(0, 0, 0)] * N_LANDMARKS).lado is Lado.IZQUIERDA

    @pytest.mark.parametrize("n", [0, 20, 22])
    def test_rechaza_numero_de_landmarks_incorrecto(self, n):
        with pytest.raises(ErrorDeContrato, match="landmarks"):
            Mano(Lado.DERECHA, 1.0, [(0, 0, 0)] * n)

    def test_rechaza_punto_sin_las_tres_coordenadas(self):
        puntos = [(0, 0, 0)] * N_LANDMARKS
        puntos[7] = (0, 0)
        with pytest.raises(ErrorDeContrato, match="landmark 7"):
            Mano(Lado.DERECHA, 1.0, puntos)

    @pytest.mark.parametrize("score", [-0.1, 1.5])
    def test_rechaza_score_fuera_de_rango(self, score):
        with pytest.raises(ErrorDeContrato, match="score"):
            Mano(Lado.DERECHA, score, [(0, 0, 0)] * N_LANDMARKS)

    def test_es_inmutable(self):
        m = factorias.mano()
        with pytest.raises(dataclasses.FrozenInstanceError):
            m.score = 0.1


class TestFrame:
    def test_sin_manos_devuelve_none(self):
        assert Frame(0).mano(Lado.DERECHA) is None

    def test_devuelve_la_mano_del_lado_pedido(self):
        f = factorias.frame(0, (Lado.IZQUIERDA, Lado.DERECHA))
        assert f.mano(Lado.IZQUIERDA).lado is Lado.IZQUIERDA
        assert f.mano(Lado.DERECHA).lado is Lado.DERECHA

    def test_con_dos_manos_del_mismo_lado_gana_la_de_mayor_score(self):
        floja = factorias.mano(Lado.DERECHA, score=0.4)
        buena = factorias.mano(Lado.DERECHA, score=0.95, desplazamiento=(0.1, 0.1))
        assert Frame(0, (floja, buena)).mano(Lado.DERECHA) is buena
        assert Frame(0, (buena, floja)).mano(Lado.DERECHA) is buena

    def test_rechaza_t_negativo(self):
        with pytest.raises(ErrorDeContrato, match="t negativo"):
            Frame(-1)


class TestMuestra:
    def test_aislada_expone_tipo_y_glosas(self, muestra_aislada):
        assert muestra_aislada.tipo == TIPO_AISLADA
        assert muestra_aislada.glosas == ("hola",)
        assert muestra_aislada.n_frames == 30

    def test_frase_expone_tipo_y_glosas(self, muestra_frase):
        assert muestra_frase.tipo == TIPO_FRASE
        assert muestra_frase.glosas == ("hola", "como", "estar", "tu")

    def test_rechaza_muestra_sin_frames(self):
        with pytest.raises(ErrorDeContrato, match="al menos un frame"):
            MuestraAislada(frames=(), sesion="s", etiqueta="hola")

    def test_rechaza_muestra_sin_sesion(self):
        with pytest.raises(ErrorDeContrato, match="sesion"):
            MuestraAislada(frames=(Frame(0),), sesion="", etiqueta="hola")

    def test_rechaza_schema_desconocido(self):
        with pytest.raises(ErrorDeContrato, match="schema"):
            MuestraAislada(
                frames=(Frame(0),), sesion="s", etiqueta="hola", schema=SCHEMA + 1
            )

    def test_rechaza_fps_no_positivo(self):
        with pytest.raises(ErrorDeContrato, match="fps"):
            MuestraAislada(frames=(Frame(0),), sesion="s", fps_aprox=0, etiqueta="hola")

    def test_aislada_sin_etiqueta(self):
        with pytest.raises(ErrorDeContrato, match="etiqueta"):
            MuestraAislada(frames=(Frame(0),), sesion="s")

    def test_frase_sin_etiquetas(self):
        with pytest.raises(ErrorDeContrato, match="etiquetas"):
            MuestraFrase(frames=(Frame(0),), sesion="s", etiquetas=())

    def test_frase_con_etiqueta_vacia(self):
        with pytest.raises(ErrorDeContrato, match="vacia"):
            MuestraFrase(frames=(Frame(0),), sesion="s", etiquetas=("hola", ""))
