"""🎯 Muestra de una sola sena: la unica unidad de entrenamiento."""

from __future__ import annotations

from dataclasses import dataclass

from ..contrato import TIPO_AISLADA
from ..errores import ErrorDeContrato
from .muestra import Muestra


@dataclass(frozen=True, slots=True)
class MuestraAislada(Muestra):
    """Una sola sena. **Es la unica unidad de entrenamiento** (principio 6)."""

    etiqueta: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.etiqueta:
            raise ErrorDeContrato("una muestra aislada necesita etiqueta")

    @property
    def tipo(self) -> str:
        return TIPO_AISLADA

    @property
    def glosas(self) -> tuple[str, ...]:
        return (self.etiqueta,)
