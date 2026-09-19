"""El repositorio es el unico que sabe de rutas. Se comprueba que no se le escapen."""

from __future__ import annotations

import pytest

from signia_modelo.dominio.contrato import TIPO_AISLADA, TIPO_FRASE
from signia_modelo.dominio.errores import ErrorDeContrato
from signia_modelo.dominio.puertos import EscritorMuestras, LectorMuestras, RepositorioMuestras
from signia_modelo.infra.configuracion_datos import ENV_DATOS_DIR
from signia_modelo.infra.nombres_de_ruta import sanear
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco
from tests import factorias


class TestSanear:
    @pytest.mark.parametrize(
        "entrada,esperado",
        [
            ("Hola", "hola"),
            ("como estas", "como_estas"),
            ("  reposo  ", "reposo"),
            ("2026-09-20-snt-01", "2026-09-20-snt-01"),
        ],
    )
    def test_normaliza(self, entrada, esperado):
        assert sanear(entrada) == esperado

    @pytest.mark.parametrize(
        "ataque", ["../../etc", r"..\..\windows", "a/b", r"c:\datos"]
    )
    def test_neutraliza_rutas(self, ataque):
        """La etiqueta viene del usuario y acaba siendo un nombre de carpeta."""
        limpio = sanear(ataque)
        assert "/" not in limpio
        assert "\\" not in limpio
        assert ".." not in limpio

    @pytest.mark.parametrize("vacio", ["", "   ", "///", "..."])
    def test_rechaza_lo_que_no_deja_nada(self, vacio):
        with pytest.raises(ErrorDeContrato):
            sanear(vacio)


class TestPuertos:
    def test_cumple_los_puertos_del_dominio(self, repo_vacio):
        assert isinstance(repo_vacio, LectorMuestras)
        assert isinstance(repo_vacio, EscritorMuestras)
        assert isinstance(repo_vacio, RepositorioMuestras)


class TestGuardarYListar:
    def test_guardar_y_recuperar_una_aislada(self, repo_vacio):
        muestra = factorias.muestra()
        repo_vacio.guardar(muestra)
        assert list(repo_vacio.listar(tipo=TIPO_AISLADA)) == [muestra]

    def test_guardar_y_recuperar_una_frase(self, repo_vacio):
        frase = factorias.frase()
        repo_vacio.guardar(frase)
        assert list(repo_vacio.listar(tipo=TIPO_FRASE)) == [frase]

    def test_la_estructura_en_disco_es_la_del_plan(self, repo_vacio):
        repo_vacio.guardar(factorias.muestra(etiqueta="Hola"))
        repo_vacio.guardar(factorias.frase())
        assert (repo_vacio.raiz / "crudo" / "aisladas" / "hola").is_dir()
        assert (repo_vacio.raiz / "crudo" / "frases").is_dir()

    def test_identificadores_distintos_en_la_misma_sesion(self, repo_vacio):
        ids = {repo_vacio.guardar(factorias.muestra()) for _ in range(3)}
        assert len(ids) == 3
        assert len(repo_vacio.rutas(tipo=TIPO_AISLADA)) == 3

    def test_no_mezcla_etiquetas(self, repo_vacio):
        repo_vacio.guardar(factorias.muestra(etiqueta="hola"))
        repo_vacio.guardar(factorias.muestra(etiqueta="reposo"))
        repo_vacio.guardar(factorias.muestra(etiqueta="reposo"))
        assert repo_vacio.contar() == {"hola": 1, "reposo": 2}

    def test_listar_sin_filtro_devuelve_todo(self, repo_vacio):
        repo_vacio.guardar(factorias.muestra())
        repo_vacio.guardar(factorias.frase())
        assert len(list(repo_vacio.listar())) == 2

    def test_filtrar_por_etiqueta_no_arrastra_las_frases(self, repo_vacio):
        """Una etiqueta nombra una clase de aisladas; las frases no tienen etiqueta."""
        repo_vacio.guardar(factorias.muestra(etiqueta="hola"))
        repo_vacio.guardar(factorias.frase())
        muestras = list(repo_vacio.listar(etiqueta="hola"))
        assert [m.tipo for m in muestras] == ["aislada"]

    def test_filtrar_por_tipo_frase_ignora_la_etiqueta(self, repo_vacio):
        repo_vacio.guardar(factorias.muestra(etiqueta="hola"))
        repo_vacio.guardar(factorias.frase())
        assert len(list(repo_vacio.listar(tipo="frase"))) == 1

    def test_repositorio_vacio_no_falla(self, repo_vacio):
        assert list(repo_vacio.listar()) == []
        assert repo_vacio.etiquetas() == []
        assert repo_vacio.contar() == {}

    def test_las_etiquetas_salen_del_dataset_y_en_orden_estable(self, repo_vacio):
        """`n_clases` se deriva de aqui; nunca se escribe en el codigo."""
        for etiqueta in ("reposo", "hola", "tu"):
            repo_vacio.guardar(factorias.muestra(etiqueta=etiqueta))
        assert repo_vacio.etiquetas() == ["hola", "reposo", "tu"]

    def test_orden_de_lectura_estable(self, repo_vacio):
        for _ in range(5):
            repo_vacio.guardar(factorias.muestra())
        assert repo_vacio.rutas() == repo_vacio.rutas()


class TestConfiguracion:
    def test_toma_la_raiz_de_la_variable_de_entorno(self, tmp_path, monkeypatch):
        """Independencia del despliegue: configuracion por entorno."""
        monkeypatch.setenv(ENV_DATOS_DIR, str(tmp_path / "datos"))
        repo = RepositorioMuestrasEnDisco()
        repo.guardar(factorias.muestra())
        assert (tmp_path / "datos" / "crudo").is_dir()

    def test_el_argumento_gana_a_la_variable_de_entorno(self, tmp_path, monkeypatch):
        monkeypatch.setenv(ENV_DATOS_DIR, str(tmp_path / "ignorada"))
        repo = RepositorioMuestrasEnDisco(tmp_path / "elegida")
        repo.guardar(factorias.muestra())
        assert not (tmp_path / "ignorada").exists()
        assert (tmp_path / "elegida" / "crudo").is_dir()

    def test_carpeta_de_tipo_desconocido(self, repo_vacio):
        with pytest.raises(ErrorDeContrato, match="tipo de muestra desconocido"):
            repo_vacio.carpeta_de("video")

    def test_aislada_sin_etiqueta_no_tiene_carpeta(self, repo_vacio):
        with pytest.raises(ErrorDeContrato, match="etiqueta"):
            repo_vacio.carpeta_de(TIPO_AISLADA)
