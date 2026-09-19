"""✅ Lo que devuelve `POST /muestras`: que entro exactamente."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RespuestaDeImportacion(BaseModel):
    """Resultado de guardar un lote.

    Devuelve el conteo por etiqueta -y no solo un "ok"- para que el front
    pueda confirmar en pantalla que subio lo que el usuario acababa de grabar.
    """

    guardadas: int = Field(description="Muestras que entraron en el dataset")
    identificadores: list[str] = Field(description="Identificador de cada muestra guardada")
    por_etiqueta: dict[str, int] = Field(description="Cuantas muestras de cada glosa")
