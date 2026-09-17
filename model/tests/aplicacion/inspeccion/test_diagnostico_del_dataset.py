"""Los criterios de la Fase 2, aplicados: que bloquea, que solo avisa y que no.

Los tests describen el criterio en lenguaje de dataset ("reposo necesita el
doble que la clase mas poblada"), no el valor concreto: si manana subimos el
minimo a 50 muestras, estos tests siguen valiendo.
"""

from __future__ import annotations

import itertools

import pytest

from signia_modelo.aplicacion.inspeccion import (
    CodigoDeAviso,
    Gravedad,
    diagnosticar,
    hay_bloqueos,
    identificador,
    resumir,
)
from signia_modelo.dominio.criterios_dataset import (
    FACTOR_MINIMO_DE_REPOSO,
    FRAMES_MINIMOS_POR_MUESTRA,
    FRASES_MINIMAS,
    MUESTRAS_MINIMAS_POR_CLASE,
)
from signia_modelo.dominio.entidades import Lado
from signia_modelo.dominio.reposo import ETIQUETA_REPOSO
from tests import factorias

DER = Lado.DERECHA

#: Muestras de reposo suficientes para no disparar su propio aviso.
REPOSO_SUFICIENTE = int(MUESTRAS_MINIMAS_POR_CLASE * FACTOR_MINIMO_DE_REPOSO)


def aisladas(etiqueta: str, cuantas: int, *, sesion: str = "s1", n_frames: int = 30, lados=(DER,)):
    return [
        factorias.muestra(n_frames, etiqueta=etiqueta, sesion=sesion, lados=lados)
        for _ in range(cuantas)
    ]


def dataset_sano() -> list:
    """Un dataset que cumple todos los criterios: la referencia en verde.

    Dos senas mas `reposo`, dos sesiones cada una, y frases que combinan las
    dos senas en ordenes distintos.
    """
    muestras = []
    for etiqueta in ("hola", "tu"):
        for sesion in ("s1", "s2"):
            muestras += aisladas(etiqueta, MUESTRAS_MINIMAS_POR_CLASE // 2, sesion=sesion)
    for sesion in ("s1", "s2"):
        muestras += aisladas(ETIQUETA_REPOSO, REPOSO_SUFICIENTE // 2, sesion=sesion)

    for numero, secuencia in enumerate(_secuencias_distintas(FRASES_MINIMAS)):
        muestras.append(factorias.frase(40, etiquetas=secuencia, sesion=f"s{numero % 2 + 1}"))
    return muestras


def _secuencias_distintas(cuantas: int) -> list[tuple[str, ...]]:
    """Combinaciones distintas de las dos senas del vocabulario de prueba.

    Con 2 glosas y longitudes de 2 a 4 hay 28 secuencias posibles, de sobra
    para que ninguna frase se repita.
    """
    posibles = (
        secuencia
        for longitud in (2, 3, 4)
        for secuencia in itertools.product(("hola", "tu"), repeat=longitud)
    )
    return list(itertools.islice(posibles, cuantas))


def codigos(muestras) -> set[CodigoDeAviso]:
    return {aviso.codigo for aviso in diagnosticar(resumir(muestras))}


class TestDatasetSano:
    def test_no_tiene_ningun_aviso(self):
        avisos = diagnosticar(resumir(dataset_sano()))
        assert avisos == (), [aviso.codigo.value for aviso in avisos]

    def test_no_bloquea(self):
        assert not hay_bloqueos(diagnosticar(resumir(dataset_sano())))


class TestDatasetVacio:
    def test_avisa_una_sola_vez(self):
        avisos = diagnosticar(resumir([]))
        assert [aviso.codigo for aviso in avisos] == [
            CodigoDeAviso.DATASET_VACIO,
            CodigoDeAviso.POCAS_FRASES,
        ]

    def test_bloquea(self):
        assert hay_bloqueos(diagnosticar(resumir([])))


class TestCantidad:
    def test_una_clase_con_pocas_muestras_bloquea(self):
        muestras = [m for m in dataset_sano() if _no_es_de(m, "tu")]
        muestras += aisladas("tu", MUESTRAS_MINIMAS_POR_CLASE - 2, sesion="s1")
        muestras += aisladas("tu", 1, sesion="s2")
        assert CodigoDeAviso.CLASE_CON_POCAS_MUESTRAS in codigos(muestras)

    def test_justo_el_minimo_de_muestras_no_avisa(self):
        """El criterio es \"al menos\", no \"mas de\"."""
        muestras = [m for m in dataset_sano() if _no_es_de(m, "tu")]
        muestras += aisladas("tu", MUESTRAS_MINIMAS_POR_CLASE - 1, sesion="s1")
        muestras += aisladas("tu", 1, sesion="s2")
        assert CodigoDeAviso.CLASE_CON_POCAS_MUESTRAS not in codigos(muestras)

    def test_el_aviso_dice_lo_medido_y_lo_exigido(self):
        muestras = aisladas("hola", 3)
        aviso = next(
            a
            for a in diagnosticar(resumir(muestras))
            if a.codigo is CodigoDeAviso.CLASE_CON_POCAS_MUESTRAS
        )
        assert (aviso.sujeto, aviso.medido, aviso.exigido) == (
            "hola",
            3,
            MUESTRAS_MINIMAS_POR_CLASE,
        )

    def test_pocas_frases_bloquea(self):
        muestras = [m for m in dataset_sano() if m.tipo == "aislada"]
        assert CodigoDeAviso.POCAS_FRASES in codigos(muestras)


class TestReposo:
    def test_sin_reposo_bloquea(self):
        muestras = [m for m in dataset_sano() if _no_es_de(m, ETIQUETA_REPOSO)]
        assert CodigoDeAviso.SIN_REPOSO in codigos(muestras)

    def test_reposo_al_mismo_nivel_que_las_demas_no_basta(self):
        """Es el segmentador: necesita el doble que la clase mas poblada."""
        muestras = [m for m in dataset_sano() if _no_es_de(m, ETIQUETA_REPOSO)]
        for sesion in ("s1", "s2"):
            muestras += aisladas(ETIQUETA_REPOSO, MUESTRAS_MINIMAS_POR_CLASE // 2, sesion=sesion)
        assert CodigoDeAviso.REPOSO_NO_SOBRERREPRESENTADO in codigos(muestras)

    def test_se_compara_con_la_clase_mas_poblada_no_con_la_media(self):
        muestras = [m for m in dataset_sano() if _no_es_de(m, "tu")]
        muestras += aisladas("tu", REPOSO_SUFICIENTE, sesion="s1")
        muestras += aisladas("tu", 1, sesion="s2")
        assert CodigoDeAviso.REPOSO_NO_SOBRERREPRESENTADO in codigos(muestras)

    def test_un_dataset_de_solo_reposo_no_exige_factor(self):
        """Sin otras clases no hay con que comparar; falta dato, no proporcion."""
        muestras = aisladas(ETIQUETA_REPOSO, REPOSO_SUFICIENTE, sesion="s1")
        assert CodigoDeAviso.REPOSO_NO_SOBRERREPRESENTADO not in codigos(muestras)


class TestVariedad:
    def test_un_dataset_de_una_sola_sesion_bloquea(self):
        muestras = aisladas("hola", MUESTRAS_MINIMAS_POR_CLASE, sesion="unica")
        muestras += aisladas(ETIQUETA_REPOSO, REPOSO_SUFICIENTE, sesion="unica")
        avisos = diagnosticar(resumir(muestras))
        pocas = next(a for a in avisos if a.codigo is CodigoDeAviso.POCAS_SESIONES)
        assert pocas.gravedad is Gravedad.BLOQUEA

    def test_una_clase_de_una_sola_sesion_solo_avisa(self):
        muestras = [m for m in dataset_sano() if _no_es_de(m, "tu")]
        muestras += aisladas("tu", MUESTRAS_MINIMAS_POR_CLASE, sesion="s1")
        aviso = next(
            a
            for a in diagnosticar(resumir(muestras))
            if a.codigo is CodigoDeAviso.CLASE_DE_UNA_SOLA_SESION
        )
        assert (aviso.sujeto, aviso.gravedad) == ("tu", Gravedad.ATENCION)

    def test_repetir_siempre_la_misma_frase_avisa(self):
        muestras = [m for m in dataset_sano() if m.tipo == "aislada"]
        muestras += [
            factorias.frase(40, etiquetas=("hola", "tu"), sesion=f"s{n % 2 + 1}")
            for n in range(FRASES_MINIMAS)
        ]
        assert CodigoDeAviso.FRASES_POCO_VARIADAS in codigos(muestras)

    def test_grabar_cada_frase_dos_veces_es_legitimo(self):
        """La misma frase en otra sesion es dato bueno, no falta de variedad."""
        muestras = [m for m in dataset_sano() if m.tipo == "aislada"]
        distintas = _secuencias_distintas(FRASES_MINIMAS // 2)
        muestras += [
            factorias.frase(40, etiquetas=secuencia, sesion=sesion)
            for secuencia in distintas
            for sesion in ("s1", "s2")
        ]
        assert CodigoDeAviso.FRASES_POCO_VARIADAS not in codigos(muestras)

    def test_una_frase_de_una_sola_glosa_avisa(self):
        muestras = dataset_sano()
        muestras.append(factorias.frase(40, etiquetas=("hola",), sesion="s1"))
        avisos = diagnosticar(resumir(muestras))
        cortas = [a for a in avisos if a.codigo is CodigoDeAviso.FRASE_DEMASIADO_CORTA]
        assert len(cortas) == 1


class TestCalidadDeCadaMuestra:
    def test_una_muestra_casi_estatica_avisa(self):
        muestras = dataset_sano()
        muestras += aisladas("hola", 1, sesion="s1", n_frames=FRAMES_MINIMOS_POR_MUESTRA - 1)
        avisos = diagnosticar(resumir(muestras))
        cortas = [a for a in avisos if a.codigo is CodigoDeAviso.MUESTRA_DEMASIADO_CORTA]
        assert len(cortas) == 1
        assert cortas[0].gravedad is Gravedad.ATENCION

    def test_una_muestra_sin_mano_avisa(self):
        muestras = dataset_sano()
        muestras += aisladas("hola", 1, sesion="s1", lados=())
        assert CodigoDeAviso.MUESTRA_CON_POCA_MANO in codigos(muestras)

    def test_en_reposo_las_manos_bajadas_no_son_un_problema(self):
        """Ahi los frames sin mano son dato legitimo, no un fallo de deteccion."""
        muestras = dataset_sano()
        muestras += aisladas(ETIQUETA_REPOSO, 3, sesion="s1", lados=())
        assert CodigoDeAviso.MUESTRA_CON_POCA_MANO not in codigos(muestras)

    def test_el_identificador_senala_la_muestra_por_su_posicion(self):
        resumen = resumir(aisladas("hola", 3))
        assert identificador(resumen.clase("hola"), 2) == "hola #3"


class TestCoberturaEntreFrasesYClases:
    def test_una_glosa_sin_clase_entrenada_bloquea(self):
        muestras = dataset_sano()
        muestras.append(factorias.frase(40, etiquetas=("hola", "adios"), sesion="s1"))
        aviso = next(
            a
            for a in diagnosticar(resumir(muestras))
            if a.codigo is CodigoDeAviso.GLOSA_DE_FRASE_SIN_CLASE
        )
        assert (aviso.sujeto, aviso.gravedad) == ("adios", Gravedad.BLOQUEA)

    def test_una_clase_que_no_aparece_en_ninguna_frase_avisa(self):
        muestras = dataset_sano()
        for sesion in ("s1", "s2"):
            muestras += aisladas("comer", MUESTRAS_MINIMAS_POR_CLASE // 2, sesion=sesion)
        aviso = next(
            a
            for a in diagnosticar(resumir(muestras))
            if a.codigo is CodigoDeAviso.CLASE_SIN_FRASES
        )
        assert (aviso.sujeto, aviso.gravedad) == ("comer", Gravedad.ATENCION)

    def test_reposo_no_tiene_que_aparecer_en_las_frases(self):
        """`reposo` es el separador: no se transcribe como palabra."""
        assert CodigoDeAviso.CLASE_SIN_FRASES not in codigos(dataset_sano())


class TestOrdenDeLosAvisos:
    def test_es_estable_entre_ejecuciones(self):
        muestras = aisladas("hola", 2)
        primera = [a.codigo for a in diagnosticar(resumir(muestras))]
        segunda = [a.codigo for a in diagnosticar(resumir(muestras))]
        assert primera == segunda

    @pytest.mark.parametrize("gravedad", list(Gravedad))
    def test_toda_gravedad_es_reconocible(self, gravedad):
        assert gravedad.value


def _no_es_de(muestra, etiqueta: str) -> bool:
    """¿Esta muestra NO es de esa clase? (las frases nunca lo son)."""
    return muestra.tipo != "aislada" or muestra.glosas[0] != etiqueta
