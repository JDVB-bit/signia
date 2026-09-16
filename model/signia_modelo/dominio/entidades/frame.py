"""🎞️ Un instante de la grabacion con 0, 1 o 2 manos."""

from __future__ import annotations

from dataclasses import dataclass

from ..errores import ErrorDeContrato
from .lado import Lado
from .mano import Mano


@dataclass(frozen=True, slots=True)
class Frame:
    """Un instante de la grabacion: 0, 1 o 2 manos.

    La ausencia de mano es informacion y no se rellena aqui; el relleno con
    ceros solo ocurre al construir el tensor (capa de aplicacion).
    """

    t: int
    manos: tuple[Mano, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "manos", tuple(self.manos))
        if self.t < 0:
            raise ErrorDeContrato(f"t negativo: {self.t}")

    def mano(self, lado: Lado) -> Mano | None:
        """Mano de ese lado, o `None` si no la hay.

        MediaPipe puede reportar dos manos con el mismo `handedness` (falso
        positivo). La regla, deterministica y unica en todo el proyecto: gana
        la de mayor `score`; a igualdad, la primera en aparecer.
        """
        candidatas = [mano for mano in self.manos if mano.lado is lado]
        if not candidatas:
            return None
        # max() conserva la primera ante empate: eso ya cumple la regla de desempate
        return max(candidatas, key=lambda mano: mano.score)
