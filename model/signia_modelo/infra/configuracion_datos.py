"""⚙️ Donde vive el dataset: configuracion por variable de entorno con default local."""

from __future__ import annotations

import os
from pathlib import Path

#: Variable de entorno con la raiz de datos (independencia del despliegue).
ENV_DATOS_DIR = "DATOS_DIR"

#: Raiz usada en desarrollo local cuando la variable no esta definida.
RAIZ_POR_DEFECTO = Path("data")


def raiz_de_datos(explicita: Path | str | None = None) -> Path:
    """Raiz del dataset: el argumento explicito gana a la variable de entorno."""
    if explicita is not None:
        return Path(explicita)
    return Path(os.environ.get(ENV_DATOS_DIR, RAIZ_POR_DEFECTO))
