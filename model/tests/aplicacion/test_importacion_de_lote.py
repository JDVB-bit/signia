"""Importar un lote: se guarda todo, en orden, y se informa de que entro."""

from __future__ import annotations

from signia_modelo.aplicacion.importacion_de_lote import importar_lote
from signia_modelo.dominio.contrato import TIPO_AISLADA
from tests import factorias


class EscritorDeMentira:
    """Doble del puerto `EscritorMuestras`: recuerda, no escribe.

    Existe para probar el caso de uso **sin disco**. Que se pueda es la prueba
    de que la dependencia es del puerto y no del sistema de ficheros.
    """

    def __init__(self) -> None:
        self.guardadas = []

    def guardar(self, muestra) -> str:
        self.guardadas.append(muestra)
        return f"id-{len(self.guardadas)}"


class TestImportacion:
    def test_guarda_todas_las_muestras(self):
        escritor = EscritorDeMentira()
        lote = [factorias.muestra(10, etiqueta="hola") for _ in range(3)]
        resultado = importar_lote(lote, escritor)
        assert resultado.n_muestras == 3
        assert len(escritor.guardadas) == 3

    def test_respeta_el_orden_del_lote(self):
        escritor = EscritorDeMentira()
        importar_lote(
            [factorias.muestra(5, etiqueta="hola"), factorias.muestra(5, etiqueta="tu")],
            escritor,
        )
        assert [m.glosas[0] for m in escritor.guardadas] == ["hola", "tu"]

    def test_devuelve_los_identificadores_del_repositorio(self):
        resultado = importar_lote([factorias.muestra(5)] * 2, EscritorDeMentira())
        assert resultado.identificadores == ("id-1", "id-2")

    def test_un_lote_vacio_no_guarda_nada(self):
        escritor = EscritorDeMentira()
        assert importar_lote([], escritor).n_muestras == 0
        assert escritor.guardadas == []

    def test_no_descarta_duplicados(self):
        """Dos grabaciones de la misma sena en la misma sesion son dato legitimo."""
        repetida = factorias.muestra(10, etiqueta="hola", sesion="s1")
        resultado = importar_lote([repetida, repetida], EscritorDeMentira())
        assert resultado.n_muestras == 2


class TestConteoPorEtiqueta:
    def test_cuenta_las_muestras_de_cada_clase(self):
        lote = [
            factorias.muestra(5, etiqueta="hola"),
            factorias.muestra(5, etiqueta="hola"),
            factorias.muestra(5, etiqueta="reposo"),
        ]
        resultado = importar_lote(lote, EscritorDeMentira())
        assert resultado.por_etiqueta == {"hola": 2, "reposo": 1}

    def test_normaliza_las_etiquetas(self):
        lote = [factorias.muestra(5, etiqueta="Hola"), factorias.muestra(5, etiqueta=" hola ")]
        resultado = importar_lote(lote, EscritorDeMentira())
        assert resultado.por_etiqueta == {"hola": 2}

    def test_una_frase_cuenta_en_todas_sus_glosas(self):
        lote = [factorias.frase(20, etiquetas=("hola", "tu"))]
        assert importar_lote(lote, EscritorDeMentira()).por_etiqueta == {"hola": 1, "tu": 1}

    def test_sale_en_orden_alfabetico(self):
        lote = [factorias.muestra(5, etiqueta=e) for e in ("tu", "hola", "reposo")]
        claves = list(importar_lote(lote, EscritorDeMentira()).por_etiqueta)
        assert claves == sorted(claves)


class TestSobreElDatasetReal:
    def test_lo_importado_se_puede_volver_a_leer(self, repo_vacio):
        """La prueba de que el ciclo grabar -> importar -> inspeccionar cierra."""
        lote = [factorias.muestra(10, etiqueta="hola"), factorias.frase(20)]
        importar_lote(lote, repo_vacio)

        assert repo_vacio.contar() == {"hola": 1}
        assert len(list(repo_vacio.listar())) == 2

    def test_dos_importaciones_no_se_pisan(self, repo_vacio):
        muestra = factorias.muestra(10, etiqueta="hola", sesion="2026-09-20-local")
        primera = importar_lote([muestra], repo_vacio)
        segunda = importar_lote([muestra], repo_vacio)
        assert primera.identificadores != segunda.identificadores
        assert len(repo_vacio.rutas(tipo=TIPO_AISLADA, etiqueta="hola")) == 2
