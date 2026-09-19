"""🚨 Traduce los errores del dominio a respuestas HTTP, en un solo sitio.

Las rutas no llevan `try/except`: dejan subir `ErrorDeContrato` y aqui se
convierte en un **422** con el mensaje tal cual. Ese mensaje ya es accionable
-dice la posicion de la muestra y que le falta-, asi que reescribirlo solo
perderia informacion.

Es 422 y no 400 a proposito: el JSON esta bien formado, lo que no cumple es el
contrato de datos. Es la misma familia de error que usa FastAPI cuando falla
la validacion de un modelo.
"""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from signia_modelo.dominio.errores import ErrorDeContrato

#: Clave del cuerpo de error, la misma que usa FastAPI en sus 422.
CLAVE_DETALLE = "detail"


def registrar(app: FastAPI) -> None:
    """Engancha los manejadores a la aplicacion."""

    @app.exception_handler(ErrorDeContrato)
    async def _contrato_incumplido(_: Request, error: ErrorDeContrato) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={CLAVE_DETALLE: str(error)},
        )
