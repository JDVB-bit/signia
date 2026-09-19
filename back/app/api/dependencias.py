"""🔗 Lo que las rutas piden por inyeccion, en vez de construirlo ellas.

Dos motivos, los dos de diseno y no de comodidad:

1. **DIP** — las rutas dependen del puerto `RepositorioMuestras`, no del
   adaptador de disco. Cambiar disco por otra cosa no las toca.
2. **Tests honestos** — la suite sustituye el repositorio por uno sobre
   `tmp_path`, asi que ningun test puede escribir en el dataset real.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request
from signia_modelo.dominio.puertos import RepositorioMuestras

from ..config import Ajustes
from ..infra.repositorio_en_disco import repositorio_de


def ajustes_de_la_app(peticion: Request) -> Ajustes:
    """Los ajustes con los que se creo ESTA aplicacion.

    Se leen del estado de la app y no de la cache del entorno: si no, dos
    instancias creadas con configuraciones distintas -el servidor y un test-
    compartirian la del proceso y `crear_app(configuracion)` seria mentira.
    """
    return peticion.app.state.ajustes


#: Los ajustes de la aplicacion que atiende la peticion.
AjustesInyectados = Annotated[Ajustes, Depends(ajustes_de_la_app)]


def repositorio(configuracion: AjustesInyectados) -> RepositorioMuestras:
    """El dataset, detras de su puerto."""
    return repositorio_de(configuracion.datos_dir)


#: Atajo para las firmas de las rutas, que asi se leen de un vistazo.
RepositorioInyectado = Annotated[RepositorioMuestras, Depends(repositorio)]
