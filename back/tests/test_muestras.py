"""`POST /muestras`: lo que sube el front acaba en el dataset, o no sube nada."""

from __future__ import annotations

import pytest
from signia_modelo.dominio.contrato import SCHEMA

from tests import factorias

RUTA = "/muestras"
CREADO = 201
CONTRATO_INCUMPLIDO = 422


class TestLoteValido:
    def test_responde_201(self, cliente, lote):
        respuesta = cliente.post(RUTA, json=lote([factorias.muestra()]))
        assert respuesta.status_code == CREADO

    def test_las_muestras_quedan_en_el_dataset(self, cliente, lote, repo):
        """La prueba de que el bucle grabar -> subir -> entrenar cierra."""
        cliente.post(RUTA, json=lote([factorias.muestra("hola"), factorias.muestra("hola")]))
        assert repo.contar() == {"hola": 2}

    def test_informa_de_lo_que_entro_por_etiqueta(self, cliente, lote):
        cuerpo = lote([factorias.muestra("hola"), factorias.muestra("reposo")])
        datos = cliente.post(RUTA, json=cuerpo).json()
        assert datos["guardadas"] == 2
        assert datos["por_etiqueta"] == {"hola": 1, "reposo": 1}

    def test_devuelve_un_identificador_por_muestra(self, cliente, lote):
        datos = cliente.post(RUTA, json=lote([factorias.muestra()] * 3)).json()
        assert len(set(datos["identificadores"])) == 3

    def test_acepta_frases_ademas_de_senas_sueltas(self, cliente, lote, repo):
        cliente.post(RUTA, json=lote([factorias.frase(("hola", "tu"))]))
        assert [m.tipo for m in repo.listar()] == ["frase"]

    def test_dos_envios_se_acumulan(self, cliente, lote, repo):
        cliente.post(RUTA, json=lote([factorias.muestra("hola")]))
        cliente.post(RUTA, json=lote([factorias.muestra("hola")]))
        assert repo.contar() == {"hola": 2}


class TestLoteRechazado:
    def test_un_sobre_sin_schema_no_pasa(self, cliente, lote):
        cuerpo = lote([factorias.muestra()])
        del cuerpo["schema"]
        assert cliente.post(RUTA, json=cuerpo).status_code == CONTRATO_INCUMPLIDO

    def test_un_lote_vacio_no_pasa(self, cliente):
        """Subir cero muestras es un error del cliente, no un exito silencioso."""
        respuesta = cliente.post(RUTA, json={"schema": SCHEMA, "muestras": []})
        assert respuesta.status_code == CONTRATO_INCUMPLIDO

    def test_una_muestra_invalida_tumba_el_lote_entero(self, cliente, lote, repo):
        """Media tanda guardada seria peor que ninguna: nadie sabria cual falta."""
        cuerpo = lote([factorias.muestra("hola"), factorias.muestra("tu")])
        del cuerpo["muestras"][1]["etiqueta"]

        assert cliente.post(RUTA, json=cuerpo).status_code == CONTRATO_INCUMPLIDO
        assert repo.contar() == {}

    def test_el_error_dice_que_muestra_fallo(self, cliente, lote):
        cuerpo = lote([factorias.muestra(), factorias.muestra()])
        cuerpo["muestras"][1]["frames"][0]["manos"][0]["lado"] = "left"
        detalle = cliente.post(RUTA, json=cuerpo).json()["detail"]
        assert "muestra 1 del lote" in detalle
        assert "lado invalido" in detalle

    @pytest.mark.parametrize("basura", [{}, {"schema": SCHEMA}, {"muestras": []}, []])
    def test_rechaza_cuerpos_que_no_son_un_lote(self, cliente, basura):
        assert cliente.post(RUTA, json=basura).status_code == CONTRATO_INCUMPLIDO

    def test_un_schema_futuro_se_rechaza_con_su_motivo(self, cliente, lote):
        cuerpo = lote([factorias.muestra()])
        cuerpo["schema"] = SCHEMA + 1
        respuesta = cliente.post(RUTA, json=cuerpo)
        assert respuesta.status_code == CONTRATO_INCUMPLIDO
        assert "schema de lote" in respuesta.json()["detail"]
