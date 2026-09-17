"""El informe: un texto por cada codigo de aviso y ninguna plantilla sin rellenar."""

from __future__ import annotations

import pytest

from signia_modelo.aplicacion.inspeccion import (
    Aviso,
    CodigoDeAviso,
    Gravedad,
    diagnosticar,
    resumir,
)
from signia_modelo.infra.informe_de_dataset import (
    MARCAS,
    SIN_DATO,
    TEXTOS_DE_AVISO,
    contar,
    describir,
    informe,
    lineas_de_clases,
    lineas_de_diagnostico,
    lineas_de_frases,
)
from tests import factorias

ENCABEZADO = "Dataset SignIA en /tmp/datos"


def dataset_pequeno() -> list:
    return [
        factorias.muestra(30, etiqueta="hola", sesion="s1"),
        factorias.muestra(20, etiqueta="hola", sesion="s2"),
        factorias.muestra(30, etiqueta="reposo", sesion="s1"),
        factorias.frase(60, etiquetas=("hola", "tu"), sesion="s1"),
    ]


class TestTextosDeAviso:
    """Ningun codigo puede quedarse sin frase: seria un KeyError en consola."""

    @pytest.mark.parametrize("codigo", list(CodigoDeAviso))
    def test_todo_codigo_tiene_texto(self, codigo):
        assert codigo in TEXTOS_DE_AVISO

    @pytest.mark.parametrize("gravedad", list(Gravedad))
    def test_toda_gravedad_tiene_marca(self, gravedad):
        assert gravedad in MARCAS

    @pytest.mark.parametrize("codigo", list(CodigoDeAviso))
    def test_la_plantilla_se_rellena_entera(self, codigo):
        """Sin llaves sueltas: si sobra un campo, se ve en el texto final."""
        texto = describir(Aviso(codigo, Gravedad.ATENCION, "hola", 1, 2))
        assert "{" not in texto and "}" not in texto

    def test_el_texto_lleva_la_marca_de_gravedad_delante(self):
        aviso = Aviso(CodigoDeAviso.SIN_REPOSO, Gravedad.BLOQUEA, "reposo")
        assert describir(aviso).startswith(MARCAS[Gravedad.BLOQUEA])

    def test_un_aviso_sin_numeros_tambien_se_describe(self):
        aviso = Aviso(CodigoDeAviso.DATASET_VACIO, Gravedad.BLOQUEA, "dataset")
        assert describir(aviso)

    def test_las_proporciones_se_muestran_en_porcentaje(self):
        aviso = Aviso(CodigoDeAviso.MUESTRA_CON_POCA_MANO, Gravedad.ATENCION, "hola #1", 0.2, 0.5)
        assert "20%" in describir(aviso)


class TestTablaDeClases:
    def test_hay_una_fila_por_clase_mas_la_cabecera(self):
        lineas = lineas_de_clases(resumir(dataset_pequeno()))
        assert len(lineas) == 1 + 2

    def test_las_columnas_quedan_alineadas(self):
        """Mismo ancho en todas las filas: es lo que hace legible la tabla."""
        lineas = lineas_de_clases(resumir(dataset_pequeno()))
        assert len({len(linea.rstrip()) for linea in lineas}) <= len(lineas)

    def test_cada_etiqueta_aparece_en_su_fila(self):
        lineas = lineas_de_clases(resumir(dataset_pequeno()))
        assert any("hola" in linea for linea in lineas)
        assert any("reposo" in linea for linea in lineas)

    def test_sin_clases_lo_dice_en_vez_de_dejar_un_hueco(self):
        assert "no hay" in lineas_de_clases(resumir([]))[0]

    def test_una_duracion_desconocida_no_se_inventa(self):
        muestra = factorias.muestra(10, etiqueta="hola")
        sin_fps = type(muestra)(
            frames=muestra.frames, sesion="s1", fps_aprox=None, etiqueta="hola"
        )
        assert SIN_DATO in lineas_de_clases(resumir([sin_fps]))[1]


class TestBloqueDeFrases:
    def test_resume_cantidad_y_variedad(self):
        linea = lineas_de_frases(resumir(dataset_pequeno()))[0]
        assert "frases: 1" in linea
        assert "secuencias distintas: 1" in linea

    def test_lista_el_glosario_usado(self):
        lineas = lineas_de_frases(resumir(dataset_pequeno()))
        assert "hola, tu" in lineas[1]

    def test_sin_frases_lo_dice(self):
        assert "no hay" in lineas_de_frases(resumir([]))[0]


class TestDiagnostico:
    def test_lo_que_bloquea_va_primero(self):
        avisos = [
            Aviso(CodigoDeAviso.CLASE_SIN_FRASES, Gravedad.ATENCION, "tu"),
            Aviso(CodigoDeAviso.SIN_REPOSO, Gravedad.BLOQUEA, "reposo"),
        ]
        lineas = lineas_de_diagnostico(avisos)
        assert MARCAS[Gravedad.BLOQUEA] in lineas[0]

    def test_sin_avisos_lo_celebra_explicitamente(self):
        assert "Sin avisos" in lineas_de_diagnostico([])[0]


class TestInformeCompleto:
    def test_empieza_por_el_encabezado(self):
        resumen = resumir(dataset_pequeno())
        lineas = informe(resumen, diagnosticar(resumen), encabezado=ENCABEZADO)
        assert lineas[0] == ENCABEZADO

    def test_trae_las_tres_secciones(self):
        resumen = resumir(dataset_pequeno())
        texto = "\n".join(informe(resumen, diagnosticar(resumen), encabezado=ENCABEZADO))
        assert "Senas aisladas" in texto
        assert "Frases completas" in texto
        assert "Diagnostico" in texto

    def test_dice_cuantos_avisos_hay(self):
        resumen = resumir(dataset_pequeno())
        avisos = diagnosticar(resumen)
        texto = "\n".join(informe(resumen, avisos, encabezado=ENCABEZADO))
        assert f"({len(avisos)} avisos)" in texto

    def test_la_nota_de_alcance_sale_debajo_del_encabezado(self):
        resumen = resumir(dataset_pequeno())
        lineas = informe(resumen, (), encabezado=ENCABEZADO, nota="solo una clase")
        assert lineas[1] == "solo una clase"

    def test_sin_nota_no_se_cuela_una_linea_en_blanco(self):
        resumen = resumir(dataset_pequeno())
        assert informe(resumen, (), encabezado=ENCABEZADO)[1] == ""

    @pytest.mark.parametrize(
        "cantidad,esperado", [(0, "0 clases"), (1, "1 clase"), (2, "2 clases")]
    )
    def test_el_informe_concuerda_en_numero(self, cantidad, esperado):
        assert contar(cantidad, "clase", "clases") == esperado

    def test_acepta_un_generador_de_avisos(self):
        """El script puede pasar lo que devuelva el diagnostico, sin materializar."""
        resumen = resumir([])
        lineas = informe(resumen, (a for a in diagnosticar(resumen)), encabezado=ENCABEZADO)
        assert any("No hay ninguna muestra" in linea for linea in lineas)

    def test_todo_el_informe_es_ascii(self):
        """La consola de Windows tumbaria la ejecucion con un emoji mal codificado."""
        resumen = resumir(dataset_pequeno())
        texto = "\n".join(informe(resumen, diagnosticar(resumen), encabezado=ENCABEZADO))
        assert texto.isascii()
