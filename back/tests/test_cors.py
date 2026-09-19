"""CORS: sin esto el navegador bloquea el POST del front, que corre en otro puerto."""

from __future__ import annotations

from tests.conftest import ORIGEN_DE_PRUEBA

CABECERA_ORIGEN = "access-control-allow-origin"
OK = 200


class TestCors:
    def test_el_origen_del_front_esta_permitido(self, cliente):
        respuesta = cliente.get("/salud", headers={"Origin": ORIGEN_DE_PRUEBA})
        assert respuesta.headers.get(CABECERA_ORIGEN) == ORIGEN_DE_PRUEBA

    def test_un_origen_desconocido_no_recibe_permiso(self, cliente):
        respuesta = cliente.get("/salud", headers={"Origin": "https://otra-web.example"})
        assert CABECERA_ORIGEN not in respuesta.headers

    def test_el_preflight_del_post_pasa(self, cliente):
        respuesta = cliente.options(
            "/muestras",
            headers={
                "Origin": ORIGEN_DE_PRUEBA,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        assert respuesta.status_code == OK
