"""🗣️ Muestra de varias senas seguidas: solo evalua y calibra, nunca entrena."""

from __future__ import annotations

from dataclasses import dataclass

from ..contrato import TIPO_FRASE
from ..errores import ErrorDeContrato
from .muestra import Muestra


@dataclass(frozen=True, slots=True)
class MuestraFrase(Muestra):
    """Varias senas seguidas. **Nunca entrena**: mide WER y calibra umbrales."""

    etiquetas: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, "etiquetas", tuple(self.etiquetas))
        if not self.etiquetas:
            raise ErrorDeContrato("una frase necesita su secuencia de etiquetas")
        if any(not etiqueta for etiqueta in self.etiquetas):
            raise ErrorDeContrato("hay una etiqueta vacia en la frase")

    @property
    def tipo(self) -> str:
        return TIPO_FRASE

    @property
    def glosas(self) -> tuple[str, ...]:
        return self.etiquetas
