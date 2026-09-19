"""Mitad Python de la red de contrato cruzado (Fase 2).

Vigila `model/contrato.json`: que este sincronizado con `dominio/contrato.py` y
que sus constantes sean coherentes entre si. La otra mitad vive en
`front/app/src/dominio/__tests__/contratoCompartido.test.js`, que lee este mismo
fichero y lo compara con `contrato.js`.

Si este test falla, el arreglo es ejecutar `scripts/exportar_contrato.py` **y
revisar el JS**, no borrar el fichero: una constante que cambia en un solo lado
es un dataset contaminado unos dias despues.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from signia_modelo.dominio import contrato

RAIZ = Path(__file__).resolve().parents[1]

#: Constantes sin las que el contrato deja de tener sentido. Blindan los
#: nombres: renombrar una en Python rompe aqui, no tres fases despues.
CLAVES_CRITICAS = ("SCHEMA", "T", "F", "N_MANOS", "N_LANDMARKS", "N_DIMS", "IDX_MUNECA")


def _cargar_exportador():
    """Importa `scripts/exportar_contrato.py` sin convertir `scripts/` en paquete."""
    spec = importlib.util.spec_from_file_location(
        "exportar_contrato", RAIZ / "scripts" / "exportar_contrato.py"
    )
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo


EXPORTADOR = _cargar_exportador()


@pytest.fixture(scope="module")
def exportado() -> dict:
    ruta = EXPORTADOR.DESTINO
    assert ruta.is_file(), "falta contrato.json: ejecuta scripts/exportar_contrato.py"
    with ruta.open(encoding="utf-8") as fichero:
        return json.load(fichero)


@pytest.fixture(scope="module")
def valores(exportado) -> dict:
    return exportado["constantes"]


class TestSincronia:
    """El fichero en disco tiene que ser el que produce el codigo de hoy."""

    def test_coincide_con_el_codigo_actual(self, exportado):
        assert exportado == EXPORTADOR.contrato_exportado(), (
            "contrato.json quedo desfasado respecto a dominio/contrato.py; "
            "ejecuta scripts/exportar_contrato.py y actualiza tambien contrato.js"
        )

    def test_declara_de_donde_sale(self, exportado):
        assert exportado["generado_por"] == EXPORTADOR.GENERADO_POR

    def test_viaja_la_version_del_preprocesado(self, exportado):
        assert exportado["version_preprocesado"] == contrato.VERSION_PREPROCESADO


class TestCobertura:
    """Nada relevante puede quedarse fuera del export ni cambiar de nombre."""

    @pytest.mark.parametrize("clave", CLAVES_CRITICAS)
    def test_esta_la_constante_critica(self, clave, valores):
        assert clave in valores

    def test_las_compartidas_existen(self, exportado, valores):
        for clave in exportado["compartidas_con_js"]:
            assert clave in valores, f"{clave} se declaro compartida pero no se exporta"

    def test_el_valor_exportado_es_el_del_modulo(self, valores):
        """El export no puede reescribir un valor por el camino."""
        for clave, valor in valores.items():
            en_codigo = getattr(contrato, clave)
            esperado = list(en_codigo) if isinstance(en_codigo, tuple) else en_codigo
            assert valor == esperado

    def test_no_se_exportan_tipos_ni_funciones(self, valores):
        assert "Final" not in valores
        for valor in valores.values():
            assert isinstance(valor, (bool, int, float, str, list))


class TestCoherenciaInterna:
    """Las relaciones entre constantes, escritas como aserciones.

    Son las que el codigo da por supuestas en silencio: si alguien toca una
    sin tocar las demas, el tensor sale con otra forma y el grafo ONNX falla
    con un error de dimensiones que no dice nada.
    """

    def test_hay_una_ranura_por_lado_canonico(self, valores):
        assert len(valores["LADOS_CANONICOS"]) == valores["N_MANOS"]

    def test_la_forma_son_todos_los_landmarks_menos_la_muneca(self, valores):
        esperado = (valores["N_LANDMARKS"] - 1) * valores["N_DIMS"]
        assert valores["VALORES_FORMA"] == esperado

    def test_los_bloques_suman_los_valores_por_mano(self, valores):
        bloques = ("VALORES_PRESENCIA", "VALORES_POSICION", "VALORES_ESCALA", "VALORES_FORMA")
        assert sum(valores[bloque] for bloque in bloques) == valores["VALORES_POR_MANO"]

    def test_las_features_son_las_dos_manos(self, valores):
        assert valores["F"] == valores["VALORES_POR_MANO"] * valores["N_MANOS"]

    def test_los_indices_de_landmark_estan_en_rango(self, valores):
        for clave in ("IDX_MUNECA", "IDX_NUDILLO_MEDIO"):
            assert 0 <= valores[clave] < valores["N_LANDMARKS"]

    def test_la_muneca_y_el_nudillo_son_puntos_distintos(self, valores):
        """Si coincidieran, la escala seria siempre 0 y la forma, infinita."""
        assert valores["IDX_MUNECA"] != valores["IDX_NUDILLO_MEDIO"]

    def test_el_rango_del_score_no_esta_invertido(self, valores):
        assert valores["SCORE_MINIMO"] < valores["SCORE_MAXIMO"]

    def test_la_ventana_temporal_tiene_frames(self, valores):
        assert valores["T"] >= 1

    def test_el_epsilon_de_la_escala_es_positivo(self, valores):
        assert valores["EPS_ESCALA"] > 0

    def test_los_tipos_de_muestra_son_distintos(self, valores):
        assert valores["TIPO_AISLADA"] != valores["TIPO_FRASE"]
