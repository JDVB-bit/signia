"""🩺 Lo que devuelve `GET /salud`: con que contrato habla este servicio."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EstadoDelServicio(BaseModel):
    """Estado del servicio y version del contrato que acepta.

    El front puede comprobar con esto que no esta hablando con un backend de
    otra version del preprocesado antes de subir nada.
    """

    estado: str = Field(description="'ok' si el servicio responde")
    schema_de_datos: int = Field(description="Version del formato de muestra que acepta")
    version_preprocesado: str = Field(description="Version del preprocesado del modelo")
    dataset_escribible: bool = Field(description="Si se puede guardar en la raiz de datos")
