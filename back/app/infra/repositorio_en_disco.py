"""🗂️ Construye el repositorio del dataset que usa la API.

El adaptador ya existe y esta testeado en el paquete del modelo
(`signia_modelo.infra.repo_ficheros`). El backend **no lo reescribe**: lo
construye con la configuracion del entorno y lo expone. Ese es todo el trabajo
de este modulo, y por eso es tan corto.

El dia que el dataset viva en almacenamiento de objetos, cambia este fichero y
ningun otro.
"""

from __future__ import annotations

from pathlib import Path

from signia_modelo.dominio.puertos import RepositorioMuestras
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco


def repositorio_de(datos_dir: str | None) -> RepositorioMuestras:
    """Repositorio del dataset en la raiz indicada (o la de por defecto)."""
    return RepositorioMuestrasEnDisco(datos_dir)


def es_escribible(raiz: Path) -> bool:
    """¿Se puede escribir el dataset en esa raiz?

    Se comprueba creando la carpeta: un disco lleno o un permiso mal puesto
    tiene que salir en `/salud`, no al subir la primera tanda de 40 muestras.
    """
    try:
        raiz.mkdir(parents=True, exist_ok=True)
    except OSError:
        return False
    return True
