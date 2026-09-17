"""El lienzo ASCII: el encuadre fijo, el tiempo en el caracter y ningun punto fuera."""

from __future__ import annotations

import pytest

from signia_modelo.infra.lienzo_ascii import (
    ALTO_POR_DEFECTO,
    ANCHO_POR_DEFECTO,
    BORDE_VERTICAL,
    CARACTERES_DEL_TIEMPO,
    VACIO,
    dibujar,
    leyenda,
)

#: Filas del dibujo sin contar los dos bordes horizontales.
BORDES_HORIZONTALES = 2


def celdas(lineas: list[str]) -> list[str]:
    """El interior del marco, sin los bordes verticales."""
    return [linea.strip(BORDE_VERTICAL) for linea in lineas[1:-1]]


class TestMarco:
    def test_tiene_el_tamano_pedido(self):
        lineas = dibujar([], ancho=10, alto=4)
        assert len(lineas) == 4 + BORDES_HORIZONTALES
        assert all(len(linea) == 10 + BORDES_HORIZONTALES for linea in lineas)

    def test_el_tamano_por_defecto_cabe_en_una_terminal(self):
        lineas = dibujar([(0.5, 0.5)])
        assert len(lineas[0]) == ANCHO_POR_DEFECTO + BORDES_HORIZONTALES
        assert len(lineas) == ALTO_POR_DEFECTO + BORDES_HORIZONTALES

    @pytest.mark.parametrize("ancho,alto", [(0, 4), (4, 0), (-1, 4)])
    def test_rechaza_un_lienzo_imposible(self, ancho, alto):
        with pytest.raises(ValueError, match="lienzo invalido"):
            dibujar([], ancho=ancho, alto=alto)

    def test_un_lienzo_sin_puntos_queda_en_blanco(self):
        assert set("".join(celdas(dibujar([], ancho=8, alto=3)))) == {VACIO}


class TestColocacionDeLosPuntos:
    def test_el_origen_va_arriba_a_la_izquierda(self):
        """En coordenadas de imagen, y=0 es el borde superior."""
        interior = celdas(dibujar([(0.0, 0.0)], ancho=5, alto=3))
        assert interior[0][0] != VACIO

    def test_el_maximo_va_abajo_a_la_derecha(self):
        interior = celdas(dibujar([(1.0, 1.0)], ancho=5, alto=3))
        assert interior[-1][-1] != VACIO

    def test_el_centro_va_al_centro(self):
        interior = celdas(dibujar([(0.5, 0.5)], ancho=5, alto=5))
        assert interior[2][2] != VACIO

    @pytest.mark.parametrize("punto", [(-1.0, 0.5), (2.0, 0.5), (0.5, -3.0), (0.5, 9.9)])
    def test_lo_que_se_sale_del_encuadre_se_acota(self, punto):
        """MediaPipe puede dar coordenadas fuera de [0,1]; el dibujo no revienta."""
        interior = celdas(dibujar([punto], ancho=6, alto=4))
        assert any(caracter != VACIO for fila in interior for caracter in fila)

    def test_los_huecos_no_se_dibujan(self):
        interior = celdas(dibujar([None, None], ancho=6, alto=3))
        assert set("".join(interior)) == {VACIO}

    def test_el_dominio_es_fijo_y_no_hace_auto_zoom(self):
        """Dos senas hechas en sitios distintos tienen que salir en sitios distintos."""
        arriba = celdas(dibujar([(0.5, 0.1)], ancho=9, alto=9))
        abajo = celdas(dibujar([(0.5, 0.9)], ancho=9, alto=9))
        assert arriba != abajo


class TestTiempo:
    def test_el_primer_punto_es_el_caracter_mas_tenue(self):
        interior = celdas(dibujar([(0.0, 0.0), (1.0, 1.0)], ancho=4, alto=2))
        assert interior[0][0] == CARACTERES_DEL_TIEMPO[0]

    def test_el_ultimo_punto_es_el_mas_denso(self):
        interior = celdas(dibujar([(0.0, 0.0), (1.0, 1.0)], ancho=4, alto=2))
        assert interior[-1][-1] == CARACTERES_DEL_TIEMPO[-1]

    def test_un_punto_solo_se_dibuja_como_final(self):
        interior = celdas(dibujar([(0.0, 0.0)], ancho=4, alto=2))
        assert interior[0][0] == CARACTERES_DEL_TIEMPO[-1]

    def test_si_dos_puntos_caen_en_la_misma_celda_gana_el_mas_tardio(self):
        """Asi se ve hacia donde iba la mano, no de donde venia."""
        interior = celdas(dibujar([(0.5, 0.5), (0.5, 0.5)], ancho=3, alto=3))
        assert interior[1][1] == CARACTERES_DEL_TIEMPO[-1]

    def test_la_leyenda_explica_el_gradiente(self):
        assert CARACTERES_DEL_TIEMPO[0] in leyenda()
        assert CARACTERES_DEL_TIEMPO[-1] in leyenda()
