"""📼 Base comun de toda muestra cruda: frames + sesion de grabacion."""

from __future__ import annotations

from dataclasses import dataclass

from ..contrato import SCHEMA
from ..errores import ErrorDeContrato
from .frame import Frame


@dataclass(frozen=True, slots=True)
class Muestra:
    """Secuencia de frames crudos grabada de una vez.

    Base comun de `MuestraAislada` (unidad de ENTRENAMIENTO) y `MuestraFrase`
    (conjunto de EVALUACION). El preprocesado solo necesita esta parte, por eso
    trabaja sobre `Muestra` y no sobre las subclases (LSP).
    """

    frames: tuple[Frame, ...]
    sesion: str
    fps_aprox: float | None = None
    schema: int = SCHEMA

    def __post_init__(self) -> None:
        object.__setattr__(self, "frames", tuple(self.frames))
        if self.schema != SCHEMA:
            raise ErrorDeContrato(f"schema {self.schema} no soportado (esperado {SCHEMA})")
        if not self.frames:
            raise ErrorDeContrato("una muestra necesita al menos un frame")
        # Sin sesion no hay split honesto en la evaluacion (plan, Fase 4)
        if not self.sesion:
            raise ErrorDeContrato("la muestra necesita una sesion identificada")
        if self.fps_aprox is not None and self.fps_aprox <= 0:
            raise ErrorDeContrato(f"fps_aprox invalido: {self.fps_aprox}")

    @property
    def tipo(self) -> str:  # pragma: no cover - lo redefinen las subclases
        """Tipo de muestra del contrato (`aislada` o `frase`)."""
        raise NotImplementedError

    @property
    def n_frames(self) -> int:
        """Numero de frames grabados, antes de remuestrear."""
        return len(self.frames)

    @property
    def glosas(self) -> tuple[str, ...]:
        """Etiquetas de la muestra, siempre como secuencia.

        Permite tratar aisladas y frases con el mismo codigo (LSP) sin
        preguntar por el tipo.
        """
        raise NotImplementedError
