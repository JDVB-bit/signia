"""🛡️ Saneado de textos del usuario (etiquetas, sesiones) para usarlos como rutas."""

from __future__ import annotations

import re

from ..dominio.errores import ErrorDeContrato

#: Todo lo que NO sea letra, digito, guion o guion bajo se sustituye.
_CARACTERES_NO_SEGUROS = re.compile(r"[^a-zA-Z0-9_-]+")

#: Sustituto de cada tramo de caracteres no seguros.
_SEPARADOR = "_"


def sanear(texto: str) -> str:
    """Convierte una etiqueta o sesion en un segmento de ruta seguro.

    Cierra el paso a `../` y a separadores: la etiqueta viene del usuario y
    acaba siendo un nombre de carpeta.
    """
    limpio = _CARACTERES_NO_SEGUROS.sub(_SEPARADOR, texto.strip().lower()).strip(_SEPARADOR)
    if not limpio:
        raise ErrorDeContrato(f"nombre no utilizable como ruta: {texto!r}")
    return limpio
