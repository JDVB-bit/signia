"""Los criterios de calidad del dataset (Fase 2): coherentes entre si y con el contrato."""

from __future__ import annotations

import pytest

from signia_modelo.dominio.contrato import T
from signia_modelo.dominio.criterios_dataset import (
    FACTOR_MINIMO_DE_REPOSO,
    FRACCION_MINIMA_DE_SECUENCIAS_DISTINTAS,
    FRACCION_MINIMA_DE_T,
    FRAMES_MINIMOS_POR_MUESTRA,
    FRASES_MINIMAS,
    GLOSAS_MINIMAS_POR_FRASE,
    MUESTRAS_MINIMAS_POR_CLASE,
    PROPORCION_MINIMA_DE_FRAMES_CON_MANO,
    SESIONES_MINIMAS,
)


class TestCriteriosDelDataset:
    """Los criterios tienen que ser coherentes entre si y con el contrato."""

    def test_reposo_exige_mas_que_una_clase_normal(self):
        assert FACTOR_MINIMO_DE_REPOSO > 1

    def test_los_frames_minimos_salen_de_la_ventana_del_modelo(self):
        """Derivado de T a proposito: no es un numero copiado del front."""
        assert FRAMES_MINIMOS_POR_MUESTRA == int(T * FRACCION_MINIMA_DE_T)

    def test_una_muestra_minima_no_llega_a_la_ventana(self):
        assert FRAMES_MINIMOS_POR_MUESTRA < T

    @pytest.mark.parametrize(
        "fraccion",
        [PROPORCION_MINIMA_DE_FRAMES_CON_MANO, FRACCION_MINIMA_DE_SECUENCIAS_DISTINTAS],
    )
    def test_las_proporciones_son_fracciones(self, fraccion):
        assert 0 < fraccion <= 1

    def test_una_frase_combina_al_menos_dos_senas(self):
        """Con una sola glosa no hay transicion entre senas que medir."""
        assert GLOSAS_MINIMAS_POR_FRASE >= 2

    @pytest.mark.parametrize(
        "criterio",
        [MUESTRAS_MINIMAS_POR_CLASE, FRASES_MINIMAS, SESIONES_MINIMAS],
    )
    def test_los_minimos_son_positivos(self, criterio):
        assert criterio > 0
