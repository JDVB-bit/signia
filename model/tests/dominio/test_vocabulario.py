"""La etiqueta canonica y la clase `reposo`, que es la unica que el codigo nombra."""

from __future__ import annotations

import pytest

from signia_modelo.dominio.etiquetas import normalizar_etiqueta
from signia_modelo.dominio.reposo import ETIQUETA_REPOSO, es_reposo


class TestNormalizarEtiqueta:
    @pytest.mark.parametrize("escrita", ["hola", "HOLA", "  Hola  ", "hOlA\n"])
    def test_todas_las_formas_son_la_misma_clase(self, escrita):
        assert normalizar_etiqueta(escrita) == "hola"

    def test_no_toca_los_espacios_de_dentro(self):
        """Una glosa de dos palabras es legitima; solo se limpian los bordes."""
        assert normalizar_etiqueta(" Buenos Dias ") == "buenos dias"

    def test_el_texto_vacio_sigue_vacio(self):
        assert normalizar_etiqueta("   ") == ""


class TestReposo:
    @pytest.mark.parametrize("escrita", ["reposo", "Reposo", " REPOSO "])
    def test_reconoce_la_clase_separadora(self, escrita):
        assert es_reposo(escrita)

    @pytest.mark.parametrize("otra", ["hola", "reposar", "reposo_largo", ""])
    def test_no_confunde_otras_clases(self, otra):
        assert not es_reposo(otra)

    def test_la_etiqueta_esta_normalizada(self):
        """Si estuviera en mayusculas, `es_reposo` no podria reconocerla."""
        assert normalizar_etiqueta(ETIQUETA_REPOSO) == ETIQUETA_REPOSO
