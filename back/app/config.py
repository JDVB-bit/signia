"""⚙️ Configuracion del servicio: todo por variables de entorno, sin ficheros.

Regla del plan (independencia del despliegue): el codigo no sabe si corre en
un portatil, en una VM o en un contenedor. Lo unico que cambia entre ellos son
estas variables, y todas tienen un valor por defecto que funciona en local.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

#: Variables de entorno reconocidas.
ENV_DATOS_DIR = "DATOS_DIR"
ENV_ORIGENES = "SIGNIA_ORIGENES_CORS"

#: El front en desarrollo (ver `.claude/launch.json`).
ORIGENES_POR_DEFECTO = ("http://localhost:5173", "http://127.0.0.1:5173")

#: Separador de la lista de origenes en la variable de entorno.
SEPARADOR_DE_ORIGENES = ","


@dataclass(frozen=True, slots=True)
class Ajustes:
    """Lo que el servicio necesita saber de su entorno."""

    datos_dir: str | None
    origenes_cors: tuple[str, ...]


def _origenes(crudo: str | None) -> tuple[str, ...]:
    """Lista separada por comas -> tupla, ignorando espacios y vacios."""
    if not crudo:
        return ORIGENES_POR_DEFECTO
    troceados = (origen.strip() for origen in crudo.split(SEPARADOR_DE_ORIGENES))
    return tuple(origen for origen in troceados if origen)


@lru_cache
def ajustes() -> Ajustes:
    """Ajustes del proceso. Se cachean: el entorno no cambia en caliente.

    `datos_dir` puede quedarse en `None`: entonces manda el valor por defecto
    del propio paquete del modelo, que es quien define donde vive el dataset.
    """
    return Ajustes(
        datos_dir=os.environ.get(ENV_DATOS_DIR),
        origenes_cors=_origenes(os.environ.get(ENV_ORIGENES)),
    )
