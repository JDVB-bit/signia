"""🛰️ La aplicacion FastAPI: monta las rutas y nada mas.

Se construye con una **fabrica** (`crear_app`) en vez de un objeto global: asi
los tests pueden levantar una instancia limpia con otros ajustes, sin variables
de entorno pegajosas entre casos.

Alcance de hoy (Fase 5, primera mitad): recibir muestras y decir que hay. El
entrenamiento (`POST /entrenamientos`), el artefacto (`GET /modelos/activo`) y
la redaccion con LLM (`POST /redactar`) llegan cuando exista `train.py` — un
endpoint que lanza un entrenamiento que no existe no se puede ni probar.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import manejador_de_errores, muestras, salud, senas
from .config import Ajustes, ajustes

#: Metadatos de la documentacion automatica (`/docs`).
TITULO = "SignIA API"
DESCRIPCION = "Recibe las muestras grabadas en Entrenamiento y publica el vocabulario."
VERSION = "0.1.0"

#: Metodos y cabeceras que el front necesita para subir un lote.
METODOS_PERMITIDOS = ("GET", "POST")
CABECERAS_PERMITIDAS = ("Content-Type",)

#: Rutas montadas, en el orden en que aparecen en `/docs`.
ENRUTADORES = (salud.enrutador, muestras.enrutador, senas.enrutador)


def crear_app(configuracion: Ajustes | None = None) -> FastAPI:
    """Construye la aplicacion con esos ajustes (o los del entorno)."""
    configuracion = configuracion or ajustes()
    app = FastAPI(title=TITULO, description=DESCRIPCION, version=VERSION)
    # Las rutas los leen de aqui: dos apps con configuraciones distintas no se pisan
    app.state.ajustes = configuracion

    # El front corre en otro puerto, asi que sin CORS el navegador bloquea el POST
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(configuracion.origenes_cors),
        allow_methods=list(METODOS_PERMITIDOS),
        allow_headers=list(CABECERAS_PERMITIDAS),
    )

    manejador_de_errores.registrar(app)
    for enrutador in ENRUTADORES:
        app.include_router(enrutador)
    return app


#: Instancia que sirve uvicorn (`uvicorn app.main:app`).
app = crear_app()
