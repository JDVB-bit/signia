"""✋ Lado de la mano (izquierda / derecha) segun el `handedness` de MediaPipe."""

from __future__ import annotations

from enum import Enum

from ..contrato import LADOS_CANONICOS
from ..errores import ErrorDeContrato


class Lado(str, Enum):
    """Mano real del usuario, derivada del `handedness` de MediaPipe.

    Cuidado: el video se muestra espejado en pantalla; `Lado` se refiere a la
    mano real, no a la que aparece a la izquierda de la imagen.
    """

    IZQUIERDA = "izquierda"
    DERECHA = "derecha"

    @classmethod
    def canonicos(cls) -> tuple["Lado", ...]:
        """Los lados en el orden de las ranuras del tensor, nunca el de deteccion.

        Vive aqui para que ese orden se escriba una sola vez: lo usan el
        preprocesado, las metricas del dataset y cualquier recorrido de manos.
        """
        return tuple(cls(valor) for valor in LADOS_CANONICOS)

    @classmethod
    def desde_texto(cls, valor: str) -> "Lado":
        """Convierte el texto del JSON en `Lado` o lanza un error accionable."""
        try:
            return cls(valor)
        except ValueError as exc:
            validos = ", ".join(lado.value for lado in cls)
            raise ErrorDeContrato(f"lado invalido: {valor!r} (validos: {validos})") from exc
