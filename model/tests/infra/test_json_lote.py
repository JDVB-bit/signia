"""El sobre del lote: se valida aparte de las muestras y dice DONDE falla."""

from __future__ import annotations

import pytest

from signia_modelo.dominio.contrato import SCHEMA
from signia_modelo.dominio.errores import ErrorDeContrato
from signia_modelo.infra.json_contrato import muestra_a_dict
from signia_modelo.infra.json_lote import lote_desde_muestras, muestras_desde_lote
from tests import factorias


def lote(*muestras) -> dict:
    return {"schema": SCHEMA, "muestras": [muestra_a_dict(m) for m in muestras]}


class TestLoteValido:
    def test_devuelve_las_muestras_en_orden(self):
        primera = factorias.muestra(10, etiqueta="hola")
        segunda = factorias.muestra(10, etiqueta="tu")
        muestras = muestras_desde_lote(lote(primera, segunda))
        assert [m.glosas[0] for m in muestras] == ["hola", "tu"]

    def test_acepta_aisladas_y_frases_en_el_mismo_lote(self):
        muestras = muestras_desde_lote(lote(factorias.muestra(10), factorias.frase(20)))
        assert [m.tipo for m in muestras] == ["aislada", "frase"]

    def test_las_muestras_llegan_ya_validadas(self):
        """Si existe la entidad, cumple el contrato: nadie tiene que revalidar."""
        muestra = muestras_desde_lote(lote(factorias.muestra(7)))[0]
        assert muestra.n_frames == 7


class TestSobreInvalido:
    @pytest.mark.parametrize("basura", [None, [], "hola", 3])
    def test_rechaza_lo_que_no_es_un_objeto(self, basura):
        with pytest.raises(ErrorDeContrato, match="objeto JSON"):
            muestras_desde_lote(basura)

    @pytest.mark.parametrize("schema", [None, 0, 2, "1"])
    def test_rechaza_un_schema_de_lote_distinto(self, schema):
        with pytest.raises(ErrorDeContrato, match="schema de lote"):
            muestras_desde_lote({"schema": schema, "muestras": []})

    def test_rechaza_un_lote_sin_la_lista(self):
        with pytest.raises(ErrorDeContrato, match="muestras"):
            muestras_desde_lote({"schema": SCHEMA})

    def test_rechaza_un_lote_vacio(self):
        """Enviar cero muestras es un error del cliente, no un exito silencioso."""
        with pytest.raises(ErrorDeContrato, match="ninguna muestra"):
            muestras_desde_lote({"schema": SCHEMA, "muestras": []})


class TestErrorSituado:
    def test_dice_la_posicion_de_la_muestra_que_falla(self):
        """Con 40 muestras en un fichero, "muestra invalida" no serviria."""
        datos = lote(factorias.muestra(5), factorias.muestra(5))
        del datos["muestras"][1]["etiqueta"]
        with pytest.raises(ErrorDeContrato, match="muestra 1 del lote"):
            muestras_desde_lote(datos)

    def test_conserva_el_motivo_original(self):
        datos = lote(factorias.muestra(5))
        datos["muestras"][0]["frames"][0]["manos"][0]["lado"] = "left"
        with pytest.raises(ErrorDeContrato, match="lado invalido"):
            muestras_desde_lote(datos)


class TestRoundTrip:
    def test_el_sobre_es_reversible(self):
        originales = [factorias.muestra(10, etiqueta="hola"), factorias.frase(20)]
        recuperadas = muestras_desde_lote(lote_desde_muestras(originales))
        assert recuperadas == originales

    def test_el_sobre_generado_declara_el_schema(self):
        assert lote_desde_muestras([factorias.muestra(5)])["schema"] == SCHEMA
