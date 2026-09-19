"""`GET /salud`: responde y dice con que version del contrato habla."""

from __future__ import annotations

from signia_modelo.dominio.contrato import SCHEMA, VERSION_PREPROCESADO

RUTA = "/salud"
OK = 200


class TestSalud:
    def test_responde_ok(self, cliente):
        respuesta = cliente.get(RUTA)
        assert respuesta.status_code == OK
        assert respuesta.json()["estado"] == "ok"

    def test_publica_la_version_del_contrato(self, cliente):
        """El front puede comprobarla ANTES de subir 40 muestras mal guardadas."""
        datos = cliente.get(RUTA).json()
        assert datos["schema_de_datos"] == SCHEMA
        assert datos["version_preprocesado"] == VERSION_PREPROCESADO

    def test_dice_si_el_dataset_es_escribible(self, cliente):
        assert cliente.get(RUTA).json()["dataset_escribible"] is True

    def test_no_necesita_que_el_dataset_exista_de_antes(self, cliente, raiz_de_datos):
        """Arrancar en una maquina limpia tiene que funcionar."""
        assert not raiz_de_datos.exists()
        assert cliente.get(RUTA).json()["dataset_escribible"] is True
        assert raiz_de_datos.exists()
