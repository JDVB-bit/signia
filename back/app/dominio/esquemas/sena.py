"""🔤 Lo que devuelve `GET /senas`: el vocabulario que hay HOY en el dataset."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SenaDelVocabulario(BaseModel):
    """Una clase del dataset y cuantas muestras tiene."""

    etiqueta: str = Field(description="Glosa, en su forma canonica")
    muestras: int = Field(description="Muestras aisladas grabadas de esa sena")


class VocabularioDelDataset(BaseModel):
    """El vocabulario completo.

    `n_clases` sale de contar carpetas, nunca de una constante: es el mismo
    principio que sostiene el "vocabulario abierto" del plan.
    """

    n_clases: int = Field(description="Cuantas senas distintas hay grabadas")
    senas: list[SenaDelVocabulario] = Field(description="Cada sena y su recuento")
